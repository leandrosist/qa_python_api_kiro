import os
from dotenv import load_dotenv
from clients.auth_client import AuthClient
from clients.booking_client import BookingClient


def before_all(context) -> None:
    """Carrega as variáveis do .env e inicializa os clients no contexto do Behave."""
    load_dotenv()

    base_url = os.environ["BASE_URL"]
    auth_user = os.environ["AUTH_USER"]
    auth_pass = os.environ["AUTH_PASS"]

    context.auth_client = AuthClient(base_url=base_url, username=auth_user, password=auth_pass)
    context.booking_client = BookingClient(base_url=base_url)
