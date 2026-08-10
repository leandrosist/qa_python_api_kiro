import requests


class BookingClient:
    """Service Object encapsulando as chamadas HTTP para os endpoints de booking."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    # ------------------------------------------------------------------
    # POST /booking
    # ------------------------------------------------------------------
    def create_booking(self, booking_data: dict) -> requests.Response:
        """Cria uma nova reserva.

        Args:
            booking_data: Dicionário com os dados da reserva.

        Returns:
            requests.Response: Resposta da API.
        """
        url = f"{self.base_url}/booking"
        return self.session.post(url, json=booking_data, timeout=10)

    # ------------------------------------------------------------------
    # GET /booking  (listagem com filtros opcionais)
    # ------------------------------------------------------------------
    def get_bookings(
        self,
        firstname: str | None = None,
        lastname: str | None = None,
        checkin: str | None = None,
        checkout: str | None = None,
    ) -> requests.Response:
        """Lista IDs de reservas com filtros opcionais por nome e/ou datas.

        Args:
            firstname: Filtro pelo primeiro nome do hóspede.
            lastname: Filtro pelo sobrenome do hóspede.
            checkin: Filtro por data de check-in (YYYY-MM-DD).
            checkout: Filtro por data de check-out (YYYY-MM-DD).

        Returns:
            requests.Response: Resposta da API contendo lista de bookingids.
        """
        url = f"{self.base_url}/booking"
        params: dict[str, str] = {}
        if firstname is not None:
            params["firstname"] = firstname
        if lastname is not None:
            params["lastname"] = lastname
        if checkin is not None:
            params["checkin"] = checkin
        if checkout is not None:
            params["checkout"] = checkout
        return self.session.get(url, params=params, timeout=10)

    # ------------------------------------------------------------------
    # GET /booking/{id}
    # ------------------------------------------------------------------
    def get_booking(self, booking_id: int) -> requests.Response:
        """Busca uma reserva pelo ID.

        Args:
            booking_id: Identificador da reserva.

        Returns:
            requests.Response: Resposta da API.
        """
        url = f"{self.base_url}/booking/{booking_id}"
        return self.session.get(url, timeout=10)

    # ------------------------------------------------------------------
    # PUT /booking/{id}
    # ------------------------------------------------------------------
    def update_booking(self, booking_id: int, booking_data: dict, token: str) -> requests.Response:
        """Atualiza uma reserva existente.

        Args:
            booking_id: Identificador da reserva.
            booking_data: Dicionário com os novos dados da reserva.
            token: Token de autenticação obtido via AuthClient.

        Returns:
            requests.Response: Resposta da API.
        """
        url = f"{self.base_url}/booking/{booking_id}"
        headers = {"Cookie": f"token={token}"}
        return self.session.put(url, json=booking_data, headers=headers, timeout=10)

    # ------------------------------------------------------------------
    # DELETE /booking/{id}
    # ------------------------------------------------------------------
    def delete_booking(self, booking_id: int, token: str) -> requests.Response:
        """Deleta uma reserva pelo ID.

        Args:
            booking_id: Identificador da reserva.
            token: Token de autenticação obtido via AuthClient.

        Returns:
            requests.Response: Resposta da API.
        """
        url = f"{self.base_url}/booking/{booking_id}"
        headers = {"Cookie": f"token={token}"}
        return self.session.delete(url, headers=headers, timeout=10)
