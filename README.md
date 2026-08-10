# QA Python API — Framework de Automação de Testes

Framework de automação de testes de API desenvolvido em Python, cobrindo os endpoints da [Restful-Booker API](https://restful-booker.herokuapp.com). O projeto segue a abordagem BDD (Behavior-Driven Development) com Behave, valida contratos de resposta com Pydantic v2 e gera relatórios visuais com Allure Framework.

---

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Behave](https://img.shields.io/badge/Behave-1.2.6-00A86B?style=flat)
![Requests](https://img.shields.io/badge/Requests-2.32-FF6F00?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat&logo=pydantic&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-2.13-brightgreen?style=flat)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat&logo=githubactions&logoColor=white)
![Kiro IDE](https://img.shields.io/badge/Kiro%20IDE-AI%20Dev-8A2BE2?style=flat)

| Ferramenta | Versão | Finalidade |
|---|---|---|
| Python | 3.10+ | Linguagem base do framework |
| Behave | 1.2.6 | Runner BDD (Gherkin + Steps) |
| Requests | 2.32.3 | Chamadas HTTP para a API |
| Pydantic v2 | 2.8.2 | Validação de contratos de resposta |
| python-dotenv | 1.0.1 | Gerenciamento de variáveis de ambiente |
| allure-behave | 2.13.5 | Geração de relatórios Allure |
| GitHub Actions | — | Pipeline de CI/CD |
| Kiro IDE | — | Ambiente de desenvolvimento com IA |

---

## Estrutura do Projeto

```
qa_python_api_kiro/
│
├── .env                          # Variáveis de ambiente (não versionado)
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências do projeto
├── README.md                     # Esta documentação
│
├── clients/                      # Service Objects — encapsulam as chamadas HTTP
│   ├── __init__.py
│   ├── auth_client.py            # AuthClient: POST /auth → retorna token
│   └── booking_client.py        # BookingClient: CRUD de reservas
│
├── schemas/                      # Modelos Pydantic para validação de contrato
│   ├── __init__.py
│   └── booking_schema.py        # BookingDates, Booking, BookingResponse
│
├── features/                     # Testes BDD com Behave
│   ├── environment.py            # Hooks Behave: before_all (setup global)
│   ├── booking.feature           # Cenários em Gherkin
│   └── steps/                    # Implementação dos passos Gherkin
│       ├── __init__.py
│       └── booking_steps.py     # @given, @when, @then
│
└── .github/
    └── workflows/
        └── api-tests.yml         # Pipeline GitHub Actions (CI/CD)
```

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/downloads)
- **Allure CLI** *(opcional, para visualizar relatórios localmente)* — [Instruções](https://allurereport.org/docs/install/)

Verifique as versões instaladas:

```bash
python --version
git --version
```

---

## Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/qa_python_api_kiro.git
cd qa_python_api_kiro
```

### 2. Criar e ativar o ambiente virtual

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
BASE_URL=https://restful-booker.herokuapp.com
AUTH_USER=admin
AUTH_PASS=password123
```

> O arquivo `.env` já está listado no `.gitignore` e **não deve ser versionado**.

---

## Execução dos Testes

### Rodar todos os testes

```bash
python -m behave
```

### Rodar por tags

Execute apenas os testes marcados como `@smoke` (cenário de criação de reserva):

```bash
python -m behave --tags=@smoke
```

Execute apenas os testes de `@regression`:

```bash
python -m behave --tags=@regression
```

Combine múltiplas tags (AND):

```bash
python -m behave --tags=@smoke,@regression
```

### Rodar com saída detalhada no terminal

```bash
python -m behave --no-capture -v
```

### Rodar gerando relatório Allure

**Passo 1** — Executar os testes e salvar os resultados:

```bash
python -m behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

**Passo 2** — Gerar e abrir o relatório HTML *(requer Allure CLI instalada)*:

```bash
allure serve allure-results
```

> O comando `allure serve` gera o relatório e abre automaticamente no navegador padrão.

---

## Integração Contínua (CI/CD)

O pipeline está configurado em `.github/workflows/api-tests.yml` e é disparado automaticamente nos seguintes eventos:

| Evento | Branch | Descrição |
|---|---|---|
| `push` | `main`, `develop` | Executa os testes a cada novo commit |
| `pull_request` | `main`, `develop` | Executa os testes em todo PR aberto |
| `workflow_dispatch` | qualquer | Execução manual via GitHub Actions UI |

### O que a pipeline faz

1. Faz checkout do código
2. Configura o Python 3.12
3. Instala as dependências via `pip install -r requirements.txt`
4. Executa o Behave com o formatter do Allure:
   ```bash
   python -m behave -f allure_behave.formatter:AllureFormatter -o allure-results
   ```
5. Faz upload dos resultados brutos (`allure-results/`) como artefato
6. Gera o relatório HTML do Allure
7. Faz upload do relatório HTML (`allure-report/`) como artefato

Os artefatos ficam disponíveis por **30 dias** na aba **Actions** do repositório no GitHub.

### Variáveis de ambiente no CI

As credenciais são injetadas diretamente pelo bloco `env` do workflow, sem necessidade de GitHub Secrets para este projeto público:

```yaml
env:
  BASE_URL: https://restful-booker.herokuapp.com
  AUTH_USER: admin
  AUTH_PASS: password123
```

> Para projetos em ambientes protegidos, mova esses valores para **GitHub Secrets** e referencie-os como `${{ secrets.AUTH_USER }}`.

---

## Cenários de Teste

| Cenário | Tag | Endpoint | Método |
|---|---|---|---|
| Criar uma nova reserva com sucesso | `@smoke` | `/booking` | POST |
| Consultar a reserva criada pelo ID | `@regression` | `/booking/{id}` | GET |
| Atualizar a reserva com autenticação | `@regression` | `/booking/{id}` | PUT |
| Deletar a reserva criada | `@regression` | `/booking/{id}` | DELETE |

---

## Contribuindo

1. Crie uma branch a partir de `develop`: `git checkout -b feature/nome-da-feature`
2. Implemente as mudanças seguindo os padrões do projeto
3. Garanta que todos os testes passam localmente antes de abrir o PR
4. Abra um Pull Request descrevendo as alterações
