from pydantic import BaseModel, Field


class BookingDates(BaseModel):
    """Datas de check-in e check-out da reserva."""

    checkin: str = Field(..., examples=["2024-01-01"], description="Data de check-in no formato YYYY-MM-DD")
    checkout: str = Field(..., examples=["2024-01-10"], description="Data de check-out no formato YYYY-MM-DD")


class Booking(BaseModel):
    """Dados completos de uma reserva."""

    firstname: str = Field(..., examples=["John"], description="Primeiro nome do hóspede")
    lastname: str = Field(..., examples=["Doe"], description="Sobrenome do hóspede")
    totalprice: int = Field(..., gt=0, examples=[150], description="Preço total em inteiro")
    depositpaid: bool = Field(..., examples=[True], description="Se o depósito foi pago")
    bookingdates: BookingDates = Field(..., description="Datas de check-in e check-out")
    additionalneeds: str | None = Field(default=None, examples=["Breakfast"], description="Necessidades adicionais")


class BookingResponse(BaseModel):
    """Resposta da API ao criar uma nova reserva."""

    bookingid: int = Field(..., description="ID da reserva criada")
    booking: Booking = Field(..., description="Dados da reserva criada")
