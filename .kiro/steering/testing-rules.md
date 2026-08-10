# Regras de Teste e Tagging

- Todo cenário em arquivos `.feature` deve conter tags como `@smoke` ou `@regression`.
- Testes que criam dados dinâmicos devem garantir a limpeza ou reaproveitamento via `context`.
- As asserções de contrato devem utilizar os métodos do Pydantic v2 (`model_validate`).
- Toda requisição que exige autorização deve reutilizar o token gerado no `AuthClient`.