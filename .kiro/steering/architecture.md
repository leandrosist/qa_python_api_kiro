# Arquitetura e Padrões de Projeto

Toda nova funcionalidade deve seguir estritamente o padrão Service Object:

1. **`clients/`**: Encapsula todas as chamadas HTTP (`requests`). Nenhuma asserção deve ficar dentro das classes de client.
2. **`schemas/`**: Modelos Pydantic v2 para validar o payload de envio e a resposta das requisições.
3. **`features/`**: Arquivos `.feature` contendo os cenários em BDD (Gherkin).
4. **`features/steps/`**: Conecta os passos do Gherkin aos clientes HTTP e valida os contratos com Pydantic.
5. **`features/environment.py`**: Gerencia o contexto do Behave (`context`) e inicializa variáveis do `.env`.