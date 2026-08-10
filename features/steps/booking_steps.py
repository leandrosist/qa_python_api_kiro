from behave import given, when, then
from schemas.booking_schema import Booking, BookingDates, BookingResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_to_booking_dict(row) -> dict:
    """Converte uma linha da tabela Gherkin em um dicionário de reserva."""
    return {
        "firstname": row["firstname"],
        "lastname": row["lastname"],
        "totalprice": int(row["totalprice"]),
        "depositpaid": row["depositpaid"].lower() == "true",
        "bookingdates": {
            "checkin": row["checkin"],
            "checkout": row["checkout"],
        },
        "additionalneeds": row.get("additionalneeds", ""),
    }


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

@given("que o sistema está acessível")
def step_system_accessible(context):
    """Verifica que a URL base está configurada."""
    assert context.booking_client is not None, "BookingClient não foi inicializado"
    assert context.auth_client is not None, "AuthClient não foi inicializado"


# ---------------------------------------------------------------------------
# Cenário: Criar reserva
# ---------------------------------------------------------------------------

@given("que tenho os dados de uma nova reserva")
def step_have_booking_data(context):
    """Armazena os dados da reserva a partir da tabela Gherkin."""
    row = context.table[0]
    context.booking_payload = _row_to_booking_dict(row)

    # Valida o payload com Pydantic antes de enviar
    Booking(**context.booking_payload)


@when("eu envio uma requisição POST para criar a reserva")
def step_post_create_booking(context):
    """Executa POST /booking."""
    context.response = context.booking_client.create_booking(context.booking_payload)


@then("a resposta deve ter status {expected_status:d}")
def step_check_status_code(context, expected_status):
    """Valida o status HTTP da resposta."""
    actual = context.response.status_code
    assert actual == expected_status, (
        f"Status esperado {expected_status}, mas foi {actual}. Body: {context.response.text}"
    )


@then("a resposta deve conter o ID da reserva criada")
def step_response_has_booking_id(context):
    """Valida contrato com Pydantic e armazena o ID para uso nos próximos cenários."""
    booking_response = BookingResponse(**context.response.json())
    assert booking_response.bookingid > 0, "bookingid deve ser maior que zero"

    # Compartilha entre cenários via context
    context.booking_id = booking_response.bookingid
    context.created_booking = booking_response.booking


@then("os dados da reserva na resposta devem corresponder aos enviados")
def step_response_matches_payload(context):
    """Compara os dados retornados com o payload enviado."""
    booking = context.created_booking
    payload = context.booking_payload

    assert booking.firstname == payload["firstname"], f"firstname: {booking.firstname} != {payload['firstname']}"
    assert booking.lastname == payload["lastname"], f"lastname: {booking.lastname} != {payload['lastname']}"
    assert booking.totalprice == payload["totalprice"], f"totalprice: {booking.totalprice} != {payload['totalprice']}"
    assert booking.depositpaid == payload["depositpaid"], f"depositpaid: {booking.depositpaid} != {payload['depositpaid']}"
    assert booking.bookingdates.checkin == payload["bookingdates"]["checkin"]
    assert booking.bookingdates.checkout == payload["bookingdates"]["checkout"]


# ---------------------------------------------------------------------------
# Cenário: Consultar reserva
# ---------------------------------------------------------------------------

@given("que existe uma reserva criada previamente")
def step_booking_exists(context):
    """Cria uma reserva caso ainda não exista no contexto."""
    if not hasattr(context, "booking_id"):
        payload = {
            "firstname": "Alice",
            "lastname": "Test",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-08-01", "checkout": "2024-08-05"},
            "additionalneeds": "None",
        }
        response = context.booking_client.create_booking(payload)
        assert response.status_code == 200, f"Falha ao criar reserva de setup: {response.text}"
        booking_response = BookingResponse(**response.json())
        context.booking_id = booking_response.bookingid
        context.booking_payload = payload


@when("eu envio uma requisição GET para buscar a reserva pelo ID")
def step_get_booking(context):
    """Executa GET /booking/{id}."""
    context.response = context.booking_client.get_booking(context.booking_id)


@then("os dados retornados devem corresponder à reserva criada")
def step_get_response_matches(context):
    """Valida com Pydantic e compara com o payload de criação."""
    booking = Booking(**context.response.json())
    payload = context.booking_payload

    assert booking.firstname == payload["firstname"]
    assert booking.lastname == payload["lastname"]
    assert booking.totalprice == payload["totalprice"]


# ---------------------------------------------------------------------------
# Cenário: Atualizar reserva
# ---------------------------------------------------------------------------

@given("que tenho um token de autenticação válido")
def step_have_auth_token(context):
    """Obtém e armazena o token de autenticação."""
    if not hasattr(context, "auth_token"):
        context.auth_token = context.auth_client.get_token()
    assert context.auth_token, "Token de autenticação não pode ser vazio"


@when("eu envio uma requisição PUT para atualizar a reserva com novos dados")
def step_put_update_booking(context):
    """Executa PUT /booking/{id} com os dados da tabela Gherkin."""
    row = context.table[0]
    context.update_payload = _row_to_booking_dict(row)

    # Valida payload com Pydantic antes de enviar
    Booking(**context.update_payload)

    context.response = context.booking_client.update_booking(
        booking_id=context.booking_id,
        booking_data=context.update_payload,
        token=context.auth_token,
    )


@then("os dados da reserva devem refletir as atualizações enviadas")
def step_update_response_matches(context):
    """Valida com Pydantic e compara com o payload de atualização."""
    updated_booking = Booking(**context.response.json())
    payload = context.update_payload

    assert updated_booking.firstname == payload["firstname"], (
        f"firstname esperado '{payload['firstname']}', recebido '{updated_booking.firstname}'"
    )
    assert updated_booking.lastname == payload["lastname"]
    assert updated_booking.totalprice == payload["totalprice"]
    assert updated_booking.depositpaid == payload["depositpaid"]


# ---------------------------------------------------------------------------
# Cenário: Deletar reserva
# ---------------------------------------------------------------------------

@when("eu envio uma requisição DELETE para remover a reserva")
def step_delete_booking(context):
    """Executa DELETE /booking/{id}."""
    context.response = context.booking_client.delete_booking(
        booking_id=context.booking_id,
        token=context.auth_token,
    )


@then("a reserva não deve mais existir na API")
def step_booking_not_found(context):
    """Verifica que um GET subsequente retorna 404."""
    get_response = context.booking_client.get_booking(context.booking_id)
    assert get_response.status_code == 404, (
        f"Esperado 404 após deleção, mas recebeu {get_response.status_code}"
    )
