---
inclusion: always
---
<!------------------------------------------------------------------------------------
   Add rules to this file or a short description and have Kiro refine them for you.
   
   Learn about inclusion modes: https://kiro.dev/docs/steering/#inclusion-modes
-------------------------------------------------------------------------------------> 

# Tech Stack - Automação de API

- **Linguagem:** Python 3.11+
- **Runner BDD:** Behave
- **HTTP Client:** Requests
- **Validação de Schema:** Pydantic (v2)
- **Variáveis de Ambiente:** python-dotenv (`.env`)
- **Relatório:** Allure Framework (`allure-behave` + GitHub Pages)
- **CI/CD:** GitHub Actions com deploy direto via `actions/deploy-pages`