import os
import requests


class AuthClient:
    """Responsável pela autenticação na API Restful-Booker."""

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_token(self) -> str:
        """Realiza POST /auth e retorna o token de autenticação.

        Returns:
            str: Token retornado pela API.

        Raises:
            RuntimeError: Se a API retornar erro ou o token não estiver presente.
        """
        url = f"{self.base_url}/auth"
        payload = {"username": self.username, "password": self.password}
        response = requests.post(url, json=payload, timeout=10)

        response.raise_for_status()
        data = response.json()

        token = data.get("token")
        if not token:
            raise RuntimeError(f"Token não retornado pela API. Resposta: {data}")

        return token
