import aiohttp
from typing import Dict, Optional, Any


class HttpClient:
    def __init__(self, headers: dict = None):
        self.headers = headers or {}

    def set_headers(self, headers: dict):
        self.headers = headers
        return self

    def add_headers(self, headers: dict):
        self.headers = {**self.headers, **headers}
        return self

    async def post(
        self,
        url: str,
        data: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        **kwargs
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data=data,
                json=json,
                headers=self.headers,
                **kwargs
            ) as response:
                responce_data = await response.text()
                if response.headers.get("Content-Type", "").startswith("application/json"):
                    response_data = await response.json()

                if response.status >= 400:
                    # TODO make custom exception with message and body
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=responce_data,
                        headers=response.headers,
                        # body=responce_data
                    )
                return response_data
                
                
