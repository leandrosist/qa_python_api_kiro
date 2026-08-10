Feature: Listagem e Filtro de Reservas - GET /booking
  Como consumidor da API Restful-Booker
  Quero filtrar reservas por nome e/ou datas
  Para localizar reservas específicas sem precisar do ID

  Background:
    Given que o sistema está acessível
    And que existe uma reserva de referência para os filtros
      | firstname | lastname  | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Carlos    | Drummond  | 250        | true        | 2030-03-10 | 2030-03-15 | Late checkout   |

  @smoke
  Scenario: Listar todas as reservas sem filtros
    When eu envio uma requisição GET para listar todas as reservas
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar reservas pelo primeiro nome
    When eu envio uma requisição GET para listar reservas filtrando apenas por firstname "Carlos"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar reservas pelo sobrenome
    When eu envio uma requisição GET para listar reservas filtrando por lastname "Drummond"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar reservas pelo nome completo (firstname e lastname)
    When eu envio uma requisição GET para listar reservas filtrando por nome completo com firstname "Carlos" e lastname "Drummond"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar reservas por data de checkin
    When eu envio uma requisição GET para listar reservas filtrando por checkin "2030-03-10"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar reservas por data de checkout
    When eu envio uma requisição GET para listar reservas filtrando por checkout "2030-03-15"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista de IDs válidos
    And a lista deve conter o ID da reserva de referência

  @regression
  Scenario: Filtrar por nome inexistente deve retornar lista vazia
    When eu envio uma requisição GET para listar reservas filtrando apenas por firstname "NomeQueNaoExiste99"
    Then a resposta deve ter status 200
    And a resposta deve ser uma lista vazia de IDs