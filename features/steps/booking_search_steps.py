from behave import given, when, then
from schemas.booking_schema import BookingListResponse, BookingResponse


# ---------------------------------------------------------------------------
# Background — reserva de referência para os cenários de filtro
# ---------------------------------------------------------------------------

@given("que existe uma reserva de referência para os filtros")
def step_create_reference_booking(context):
    """Cria a reserva de referência usada como fixture pelos cenários de filtro.

    Reutiliza o ID se já foi criado nesta execução para evitar dados duplicados.
    """
    if hasattr(context, "reference_booking_id"):
        return

    row = context.table[0]
    payload = {
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

    response = context.booking_client.create_booking(payload)
    assert response.status_code == 200, (
        f"Falha ao criar reserva de referência: {response.status_code} — {response.text}"
    )

    booking_response = BookingResponse.model_validate(response.json())
    context.reference_booking_id = booking_response.bookingid
    context.reference_booking_payload = payload


# ---------------------------------------------------------------------------
# When — variações de filtro para GET /booking
# ---------------------------------------------------------------------------

@when("eu envio uma requisição GET para listar todas as reservas")
def step_get_all_bookings(context):
    """Executa GET /booking sem filtros."""
    context.response = context.booking_client.get_bookings()


@when('eu envio uma requisição GET para listar reservas filtrando apenas por firstname "{firstname}"')
def step_get_bookings_by_firstname(context, firstname: str):
    """Executa GET /booking?firstname={firstname}."""
    context.response = context.booking_client.get_bookings(firstname=firstname)


@when('eu envio uma requisição GET para listar reservas filtrando por lastname "{lastname}"')
def step_get_bookings_by_lastname(context, lastname: str):
    """Executa GET /booking?lastname={lastname}."""
    context.response = context.booking_client.get_bookings(lastname=lastname)


@when('eu envio uma requisição GET para listar reservas filtrando por nome completo com firstname "{firstname}" e lastname "{lastname}"')
def step_get_bookings_by_full_name(context, firstname: str, lastname: str):
    """Executa GET /booking?firstname={firstname}&lastname={lastname}."""
    context.response = context.booking_client.get_bookings(
        firstname=firstname, lastname=lastname
    )


@when('eu envio uma requisição GET para listar reservas filtrando por checkin "{checkin}"')
def step_get_bookings_by_checkin(context, checkin: str):
    """Executa GET /booking?checkin={checkin}."""
    context.response = context.booking_client.get_bookings(checkin=checkin)


@when('eu envio uma requisição GET para listar reservas filtrando por checkout "{checkout}"')
def step_get_bookings_by_checkout(context, checkout: str):
    """Executa GET /booking?checkout={checkout}."""
    context.response = context.booking_client.get_bookings(checkout=checkout)


# ---------------------------------------------------------------------------
# Then — asserções de contrato e conteúdo
# ---------------------------------------------------------------------------

@then("a resposta deve ser uma lista de IDs válidos")
def step_response_is_valid_id_list(context):
    """Valida o contrato da listagem com Pydantic v2 (model_validate)."""
    data = context.response.json()
    assert isinstance(data, list), f"Esperado lista, recebido: {type(data)}"

    booking_list = BookingListResponse.model_validate_list(data)
    context.booking_list = booking_list

    # Garante que cada item tem bookingid inteiro positivo
    for item in booking_list.root:
        assert item.bookingid > 0, f"bookingid inválido: {item.bookingid}"


@then("a lista deve conter o ID da reserva de referência")
def step_list_contains_reference_id(context):
    """Verifica que o ID da reserva de referência está presente na listagem."""
    assert hasattr(context, "reference_booking_id"), (
        "ID de referência não encontrado no context. "
        "Certifique-se de que o Background criou a reserva."
    )
    assert context.booking_list.contains_id(context.reference_booking_id), (
        f"ID {context.reference_booking_id} não encontrado na lista retornada. "
        f"IDs recebidos: {[item.bookingid for item in context.booking_list.root]}"
    )


@then("a resposta deve ser uma lista vazia de IDs")
def step_response_is_empty_list(context):
    """Valida que a listagem retornou uma lista vazia."""
    data = context.response.json()
    assert isinstance(data, list), f"Esperado lista, recebido: {type(data)}"
    assert len(data) == 0, (
        f"Esperado lista vazia, mas recebeu {len(data)} item(s): {data}"
    )