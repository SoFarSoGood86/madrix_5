import asyncio
from .const import DEFAULT_PORT
import json

class MadrixAPI:
    def __init__(self, host, port=DEFAULT_PORT, protocol='http', api_key=''):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.api_key = api_key

    async def send_command(self, command: str, payload: dict | None = None):
        """High-level send command entry point.
        For HTTP, command is a path or action and payload is the JSON body.
        For other protocols, this method should be extended.
        """
        if self.protocol == 'http':
            return await self._send_command_http(command, payload)
        # Stubs for other protocols: implement using appropriate libraries/hardware.
        raise NotImplementedError(f"Protocol {self.protocol} not implemented in this integration.\n"
                                  f"Available: http. For other backends you must add the implementation.")
    async def _send_command_http(self, command: str, payload: dict | None):
        """Send an HTTP POST to the MADRIX remote HTTP API.
        Expected endpoints (convention):
        - POST http://{host}:{port}/api/command  with JSON {"command": "...", "params": {...}}
        - GET  http://{host}:{port}/api/status   returns JSON status
        These endpoints can be adapted to your MADRIX HTTP plugin or custom web server.
        """
        try:
            import aiohttp
        except Exception as exc:
            raise RuntimeError("aiohttp is required for HTTP protocol. Add it to requirements.") from exc

        url = f"http://{self.host}:{self.port}/api/command"
        json_body = {'command': command}
        if payload:
            json_body['params'] = payload
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_body, headers=headers, timeout=10) as resp:
                text = await resp.text()
                try:
                    return await resp.json()
                except Exception:
                    return text

    async def get_status(self):
        if self.protocol == 'http':
            return await self._get_status_http()
        raise NotImplementedError(f"Status polling not implemented for protocol {self.protocol}")

    async def _get_status_http(self):
        try:
            import aiohttp
        except Exception as exc:
            raise RuntimeError("aiohttp is required for HTTP protocol. Add it to requirements.") from exc
        url = f"http://{self.host}:{self.port}/api/status"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                try:
                    return await resp.json()
                except Exception:
                    return await resp.text()
