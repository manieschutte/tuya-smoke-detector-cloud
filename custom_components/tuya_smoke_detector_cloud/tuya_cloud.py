"""Async Tuya OpenAPI client using HMAC-SHA256 signing."""
from __future__ import annotations
import hashlib, hmac, time, uuid
from typing import Any
from urllib.parse import urlencode
from aiohttp import ClientError, ClientSession
from .const import TUYA_API_BASE

class TuyaApiError(Exception):
    """Tuya API failure."""

class TuyaCloudClient:
    """Token and device-status client for Tuya OpenAPI."""
    def __init__(self, session: ClientSession, client_id: str, client_secret: str) -> None:
        self._session, self._client_id, self._secret = session, client_id, client_secret
        self._access_token = self._refresh_token = None
        self._expires = 0.0
    @staticmethod
    def _url(path: str, params=None) -> str:
        return f"{path}?{urlencode(sorted(params.items()))}" if params else path
    def _sign(self, method, url, body, timestamp, token, nonce):
        digest = hashlib.sha256(body).hexdigest()
        string_to_sign = f"{method}\n{digest}\n\n{url}"
        message = f"{self._client_id}{token or ''}{timestamp}{nonce}{string_to_sign}"
        return hmac.new(self._secret.encode(), message.encode(), hashlib.sha256).hexdigest().upper()
    async def _request(self, method, path, *, params=None, token=None) -> Any:
        url = self._url(path, params); timestamp = str(int(time.time() * 1000)); nonce = uuid.uuid4().hex
        headers = {"client_id": self._client_id, "sign": self._sign(method,url,b"",timestamp,token,nonce), "sign_method":"HMAC-SHA256", "t":timestamp, "nonce":nonce, "lang":"en"}
        if token: headers["access_token"] = token
        try:
            async with self._session.request(method, TUYA_API_BASE + url, headers=headers, timeout=20) as response:
                payload = await response.json(content_type=None); status = response.status
        except (ClientError, TimeoutError, ValueError) as err:
            raise TuyaApiError("Unable to communicate with Tuya Cloud") from err
        if status >= 400 or not isinstance(payload,dict) or not payload.get("success"):
            msg = payload.get("msg","Tuya API request failed") if isinstance(payload,dict) else "Invalid response"
            raise TuyaApiError(f"Tuya API error: {msg}")
        return payload.get("result")
    def _save_token(self, result):
        if not isinstance(result,dict) or not result.get("access_token"): raise TuyaApiError("Tuya did not return an access token")
        self._access_token=result["access_token"]; self._refresh_token=result.get("refresh_token")
        self._expires=time.time()+int(result.get("expire_time",3600))
    async def async_ensure_token(self):
        if self._access_token and time.time() < self._expires-60: return
        if self._refresh_token:
            try: result=await self._request("GET",f"/v1.0/token/{self._refresh_token}")
            except TuyaApiError: self._refresh_token=None
            else: self._save_token(result); return
        self._save_token(await self._request("GET","/v1.0/token",params={"grant_type":"1"}))
    async def async_get_device_status(self, device_id: str) -> dict[str,Any]:
        await self.async_ensure_token()
        result=await self._request("GET",f"/v1.0/iot-03/devices/{device_id}/status",token=self._access_token)
        if not isinstance(result,list): raise TuyaApiError("Unexpected device status response")
        return {item.get("code"):item.get("value") for item in result if isinstance(item,dict)}
