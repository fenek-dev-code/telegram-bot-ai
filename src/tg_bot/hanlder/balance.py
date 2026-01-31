from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pydantic import InstanceOf
from yookassa.payment import Payment, PaymentResponse

from src.core.service import UserService
from src.database import get_session
from src.pkg.kassa import create_payment
from src.pkg.logger import log
from src.tg_bot.buttons import CallBackData, PaymentButtons, UserButtons
from src.tg_bot.common import ReplyMessages, edit_message

router = Router()


class UpBalanceState(StatesGroup):
    count = State()
    process = State()
    succes = State()
    fail = State()


@router.callback_query(F.data == CallBackData.UP_BALANCE)
async def up_balance(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpBalanceState.count)
    await edit_message(
        callback_query,
        text=ReplyMessages.up_balance(callback_query.from_user),
        reply_markup=UserButtons.go_home(),
    )


@router.message(StateFilter(UpBalanceState.count))
async def user_send_count(message: types.Message, state: FSMContext):
    try:
        user_id: int
        count: float
        if message.from_user:
            user_id = message.from_user.id
        else:
            user_id = 0
        try:
            if message.text:
                count = float(message.text.strip(" "))
            else:
                return message.answer(
                    text="Ошибка возможно вы не верно прислали сумму повторите ещё раз"
                )
        except Exception:
            return await message.answer(
                text="Ошибка возможно вы не верно прислали сумму повторите ещё раз"
            )
        await message.answer("Ошидайте формирую форму оплаты!")

        log.info(f"Создали ссылку для оплаты для id={user_id}")
        payment = create_payment(count, user_id)
        url: str = ""
        if payment.confirmation:
            url = payment.confirmation.confirmation_url
        await state.set_state(UpBalanceState.process)

        await state.set_data({"payment": payment})
        log.info(f"Ожидаем оплаты от {user_id}")
        await message.answer(
            text=f"Сумма к оплате -> {count} RUB",
            reply_markup=PaymentButtons.check_payment_status(url),
        )
    except Exception as err:
        log.error(err)
        await message.answer("Ошибка сервера по пробуйте позже")


# TODO: Сделать отмену оплаты и оплату с транзакцией и увелечением баланса
@router.callback_query((StateFilter(UpBalanceState.process)))
async def payment_status(callback: types.CallbackQuery, state: FSMContext):
    payment: PaymentResponse | None = None
    data = await state.get_value("payment")
    if isinstance(data, PaymentResponse):
        payment = data
    else:
        return await edit_message(
            callback, "Внутренняя Ошибка сервера", reply_markup=UserButtons.go_home()
        )

    try:
        async with get_session() as session:
            service = UserService(session)
            user = await service.get_user(callback.from_user.id)
            if not user:
                return
            match callback.data:
                case CallBackData.PAYMENT_CHECK_STATUS:
                    log.info(
                        f"Проверяем оплату пользователя id={callback.from_user.id}"
                    )
                    match Payment.find_one(payment.id).status:
                        case "succeeded":
                            return await edit_message(
                                callback,
                                f"{user.username} Успешно обработан!",
                                UserButtons.go_home(),
                            )
                        case "canceled":
                            return await edit_message(
                                callback,
                                f"{user.username} платёж был отменён!",
                                UserButtons.go_home(),
                            )
                    return await edit_message(
                        callback,
                        f"{user.username} всё еще ожидаем оплаты - перейдите по сыллке и оплатите или подождите немного",
                        callback.message.reply_markup,  # type: ignore
                    )

                case CallBackData.START:
                    log.info(f"Пользователь id={callback.from_user.id} отменил оплату")
                    return await edit_message(
                        callback,
                        ReplyMessages.start_message(user),
                        UserButtons.get_home_menu(),
                    )

    except Exception as err:
        log.error(err)
