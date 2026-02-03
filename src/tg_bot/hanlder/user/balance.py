from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from yookassa.payment import Payment, PaymentResponse

from src.database.repository import Repository
from src.pkg.kassa import create_payment
from src.pkg.logger import log
from src.tg_bot.common import CommonFunc, UserKeyboards

router = Router()


class UpBalanceState(StatesGroup):
    count = State()
    process = State()


@router.callback_query(F.data == UserKeyboards.DATA_USER_UP_BALANCE)
async def up_balance(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpBalanceState.count)
    await CommonFunc.edit_message(
        callback_query,
        text="Для пополнения баланса введите сумму, например 200",
        reply_markup=UserKeyboards.back_to(UserKeyboards.DATA_USER_INFO_MENU),
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

        await state.set_data({"payment": payment, "amount": count})
        log.info(f"Ожидаем оплаты от {user_id}")
        await message.answer(
            text=f"Сумма к оплате -> {count} RUB",
            reply_markup=UserKeyboards.payment_keyboard(url),
        )
    except Exception as err:
        log.error(err)
        await message.answer("Ошибка сервера по пробуйте позже")


@router.callback_query(
    (StateFilter(UpBalanceState.process)) and F.data == UserKeyboards.DATA_CHECK_PAYMENT
)
async def payment_status(
    callback: types.CallbackQuery, state: FSMContext, repo: Repository
):
    payment: PaymentResponse | None = None
    data = await state.get_value("payment")
    amount = await state.get_value("amount")
    if not amount:
        amount = 0
    if isinstance(data, PaymentResponse):
        payment = data
    else:
        return
    user = await repo.user.get_user(callback.from_user.id)
    if not user:
        return
    log.info(f"Проверяем оплату пользователя id={callback.from_user.id}")
    pay = Payment.find_one(payment.id)
    match pay.status:
        case "succeeded":
            log.info(f"Оплата прошла успешно id={callback.from_user.id}")
            user.balance += float(amount)
            await repo.user.update_user(user.id, balance=user.balance)
            return await CommonFunc.edit_message(
                callback,
                f"{user.username} Успешно обработан!",
                UserKeyboards.back_to(UserKeyboards.DATA_HOME_MENU),
            )
        case "canceled":
            log.info(f"Пользователь id={callback.from_user.id} отменил оплату")
            return await CommonFunc.edit_message(
                callback,
                f"{user.username} платёж был отменён!",
                UserKeyboards.back_to(UserKeyboards.DATA_HOME_MENU),
            )
        case "error":
            log.info(f"Пользователь id={callback.from_user.id} не смог оплатить")
            return await CommonFunc.edit_message(
                callback,
                f"{user.username} платёж не был обработан!",
                UserKeyboards.back_to(UserKeyboards.DATA_HOME_MENU),
            )
    return await CommonFunc.edit_message(
        callback,
        f"{user.username} всё еще ожидаем оплаты - перейдите по сыллке и оплатите или подождите немного",
        callback.message.reply_markup,  # type: ignore
    )


@router.callback_query(
    (StateFilter(UpBalanceState.process))
    and F.data == UserKeyboards.DATA_CANCEL_PAYMENT
)
async def cancel_payment(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    payment: PaymentResponse | None = await state.get_value("payment")
    if payment is None:
        log.info(f"Пользователь id={callback.from_user.id} отменил оплату")
        return await CommonFunc.edit_message(
            callback,
            f"{callback.from_user.full_name} платёж не был обработан!",
            UserKeyboards.back_to(UserKeyboards.DATA_HOME_MENU),
        )

    log.info(f"Пользователь id={callback.from_user.id} отменил оплату")
    resp = Payment.cancel(payment.id)
    if resp.status == "canceled":
        log.info(f"Платёж id={payment.id} был отменён")
    elif resp.status == "error":
        log.info(f"Платёж id={payment.id} не был отменён")
    return await CommonFunc.edit_message(
        callback,
        f"{callback.from_user.full_name} платёж был отменён!",
        UserKeyboards.back_to(UserKeyboards.DATA_HOME_MENU),
    )
