Feature: Gerenciamento de Reservas - Restful Booker API
  Como consumidor da API Restful-Booker
  Quero gerenciar reservas de hotel
  Para garantir que as operações de CRUD funcionam corretamente

  Background:
    Given que o sistema está acessível

  @smoke
  Scenario: Criar uma nova reserva com sucesso
    Given que tenho os dados de uma nova reserva
      | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | John      | Doe      | 150        | true        | 2024-06-01 | 2024-06-10 | Breakfast       |
    When eu envio uma requisição POST para criar a reserva
    Then a resposta deve ter status 200
    And a resposta deve conter o ID da reserva criada
    And os dados da reserva na resposta devem corresponder aos enviados

  @regression
  Scenario: Consultar a reserva criada pelo ID
    Given que existe uma reserva criada previamente
    When eu envio uma requisição GET para buscar a reserva pelo ID
    Then a resposta deve ter status 200
    And os dados retornados devem corresponder à reserva criada

  @regression
  Scenario: Atualizar a reserva criada enviando o token de autenticação
    Given que existe uma reserva criada previamente
    And que tenho um token de autenticação válido
    When eu envio uma requisição PUT para atualizar a reserva com novos dados
      | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Jane      | Smith    | 200        | false       | 2024-07-01 | 2024-07-05 | Dinner          |
    Then a resposta deve ter status 200
    And os dados da reserva devem refletir as atualizações enviadas

  @regression
  Scenario: Deletar a reserva criada
    Given que existe uma reserva criada previamente
    And que tenho um token de autenticação válido
    When eu envio uma requisição DELETE para remover a reserva
    Then a resposta deve ter status 201
    And a reserva não deve mais existir na API
