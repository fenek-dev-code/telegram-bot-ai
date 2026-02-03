from aiohttp import ClientSession

from src.config import config
from src.pkg.logger import log


class KieAIClient:
    BASE_URL: str = "https://api.kie.ai/api/v1/"
    CREATE_TASK_ENDPOINT = "jobs/createTask"
    GET_STATUS_ENDPOINT = "jobs/recordInfo"
    CHECK_CREDITS_ENDPOINT = "chat/credit"

    def __init__(self):
        self._Token = config.HF_API_KEY

    # TODO: return credits int type
    async def get_balance(self) -> int:
        """Получение баланса"""
        response = await self._request("GET", self.CHECK_CREDITS_ENDPOINT)
        if response["code"] != 200:
            log.error(f"Failed to get balance: {response['message']}")
            raise Exception(f"Failed to get balance: {response['message']}")
        return response["data"]["resultJson"]

    async def generate_video(self, prompt: str, image_url: str) -> str:
        payload = {
            "model": "kling-2.6/image-to-video",
            "input": {
                "prompt": prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": "5",
            },
        }
        response = await self._request("POST", self.CREATE_TASK_ENDPOINT, payload)
        if response["code"] != 200:
            log.error(f"Failed to generate video: {response['message']}")
            raise Exception(f"Failed to generate video: {response['message']}")
        return response["data"]["task_id"]

    async def get_video_status(self, task_id: str) -> dict:
        """Получение статуса видео"""
        response = await self._request(
            "GET", self.GET_STATUS_ENDPOINT, params={"taskId": task_id}
        )
        if response["code"] != 200:
            log.error(f"Failed to get video status: {response['message']}")
            raise Exception(f"Failed to get video status: {response['message']}")
        return response["data"]["resultJson"]

    async def download_video(self, output_file: str, task_id: str):
        """Установка видео сгенерированного видео"""
        video_url = await self._get_video_url(task_id)
        download_url = await self._get_download_url(video_url)
        async with ClientSession() as session:
            session.headers.add("Authorization", f"Bearer {self._Token}")
            response = await session.get(download_url)
        if not response.ok:
            log.error(f"Failed to download video: {response.status}")
            raise Exception(f"Failed to download video: {response.status}")
        with open(output_file, "wb") as f:
            f.write(await response.read())

    async def _get_video_url(self, task_id: str) -> str:
        response = await self._request(
            "GET", self.GET_STATUS_ENDPOINT, params={"taskId": task_id}
        )
        if response["code"] != 200:
            log.error(f"Failed to get video status: {response['message']}")
            raise Exception(f"Failed to get video status: {response['message']}")
        return response["data"]["resultJson"]["video_url"]

    async def _get_download_url(self, file_url: str) -> str:
        response = await self._request(
            "GET", self.GET_STATUS_ENDPOINT, data={"url": file_url}
        )
        if response["code"] != 200:
            log.error(f"Failed to get video status: {response['message']}")
            raise Exception(f"Failed to get video status: {response['message']}")
        return response["data"]["resultJson"]["download_url"]

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
    ):
        async with ClientSession() as session:
            session.headers.add("Authorization", f"Bearer {self._Token}")
            session.headers.add("Content-Type", "application/json")
            try:
                async with session.request(
                    method, endpoint, json=data, params=params
                ) as response:
                    return await response.json()
            except Exception as e:
                log.error(f"Failed to make request: {e}")
                raise Exception(f"Failed to make request: {e}")
