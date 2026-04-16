Este é o seu novo **README.md** estendido, projetado para ser uma vitrine tecnológica de alto impacto. Ele utiliza uma paleta de cores focada em **Laranja (Segurança/Energia)**, **Preto (Elegância/Profundidade)** e **Branco (Clareza/Pureza)**, com uma estrutura densa que detalha cada um dos 97 testes aprovados.

---

<div align="center">

<!-- Banner de Identidade -->
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png" width="100%">

<h1 style="color: #FF8C00; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 3em; font-weight: bold; margin-bottom: 0;">🛡️ APOLLO IAM ENGINE</h1>
<p style="color: #666; font-size: 1.2em; margin-top: 5px;"><i>The Iron-Clad Sovereign Identity & Policy Decision Point</i></p>

<!-- Shields de Status e Tecnologia -->
<p>
  <img src="https://img.shields.io/badge/STATUS-100%25_PASSED-FF8C00?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Status">
  <img src="https://img.shields.io/badge/SECURITY-ZERO_TRUST_mTLS-000000?style=for-the-badge&logo=shield&logoColor=white" alt="Security">
  <img src="https://img.shields.io/badge/ENGINE-RBAC_%2B_ABAC-white?style=for-the-badge&logo=auth0&logoColor=black" alt="Engine">
</p>

<p>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/JWT_RSA_256-000000?style=flat-square&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/mTLS_ECDHE-FF8C00?style=flat-square&logo=googlecloud&logoColor=white" alt="mTLS">
</p>

---

<div style="background: linear-gradient(90deg, #000000 0%, #333333 50%, #000000 100%); padding: 20px; border-radius: 10px; border: 1px solid #FF8C00;">
  <p style="color: #FF8C00; font-size: 1.1em; line-height: 1.6;">
    <b>O Apollo IAM Engine</b> não é apenas um serviço de login. É uma <b>Fortaleza de Autorização</b> baseada em mTLS e Inteligência de Políticas. Projetado para arquiteturas de microsserviços onde a confiança é verificada criptograficamente em cada requisição (Zero-Trust).
  </p>
</div>

</div>

---

## 🚀 1. Visão Geral da Arquitetura

O Apollo atua como o **PDP (Policy Decision Point)** central da organização. Ele resolve a fragmentação de permissões ao centralizar a lógica de decisão, permitindo que seus microsserviços permaneçam "burros" em relação a quem pode fazer o quê, apenas consultando o `/auth/check`.

### 🌑 Camadas de Proteção
1.  **Transporte (mTLS):** Conexão impossível sem certificado físico do cliente.
2.  **Identidade (JWT):** Assinatura assimétrica (RS256) com rotação de chaves.
3.  **Autorização RBAC:** Permissões granulares mapeadas a Roles.
4.  **Autorização ABAC:** Atributos dinâmicos (Sistema, Cargo, Filial) e Hierarquia de Níveis (`rank`).

---

## 🧪 2. Certificação de Produção: 97/97 Passos

Abaixo, detalhamos o relatório de execução da **Run ID: 20260415_213724**, onde o motor foi submetido a testes de estresse, lógica e segurança, obtendo **100% de sucesso**.

### 🛠️ FASE A: Infraestrutura & Health (Steps 1-3)
*   ✅ **Health Check:** Validação de integridade do motor e conectividade com DB.
*   ✅ **OpenAPI/Swagger:** Documentação auto-gerada validada para integração de terceiros.
*   ✅ **ReDoc:** Interface técnica de especificação consultada com sucesso.

### 🔑 FASE B: Autenticação Administrativa (Steps 4-7)
*   ✅ **Admin Login:** Geração de token de superusuário.
*   ✅ **Admin Validation:** Checagem de flags `is_superuser=True`.
*   ✅ **Negative Auth:** Bloqueio de senhas incorretas e usuários inexistentes (401 Unauthorized).

### 🖥️ FASE C: Gestão & Governança (Steps 8-15)
*   ✅ **User Inventory:** Listagem e contagem de identidades ativas.
*   ✅ **Role/Permission Mapping:** Auditoria de 19 permissões e 7 papéis pré-configurados.
*   ✅ **Audit Logs:** Verificação da trilha de auditoria imutável (Audit Trail).
*   ✅ **Tokenless Protection:** Bloqueio de acesso anônimo aos endpoints de gestão.

### 🎭 FASE D: Setup RBAC - Sistema de Cotação (Steps 16-33)
*   ✅ **Permission Factory:** Criação dinâmica de `cotacao:create`, `read`, `update`, `delete`, `approve`.
*   ✅ **Role Factory:** Instalação dos papéis `vendedor`, `gerente` e `aprovador`.
*   ✅ **Role Assignment:** Vinculação de permissões granulares a cada papel.
*   ✅ **Group Logic:** Criação do grupo organizacional `Vendas`.

### 👤 FASE E: Ciclo de Vida do Usuário (Steps 34-51)
*   ✅ **Identity Provisioning:** Criação do `usuario1` (vendedor).
*   ✅ **Role/Group Attachment:** Atribuição do usuário ao departamento de vendas.
*   ✅ **RBAC Enforcement:** Verificação de que o vendedor **não** possui privilégios de admin (403 Forbidden).
*   ✅ **Session Management:** Teste de `refresh_token` e `logout` com invalidação imediata do JWT.

### 🧬 FASE F: O Motor ABAC & /auth/check (Steps 52-97)
Esta é a joia da coroa do Apollo. O motor validou as seguintes lógicas:

| Teste de Decisão | Cenário | Resultado | Razão do Motor |
| :--- | :--- | :--- | :--- |
| **Superuser Bypass** | Admin acessando qualquer recurso | ✅ ALLOWED | `reason=superuser` |
| **Simple Role** | Vendedor acessando área de vendedor | ✅ ALLOWED | `reason=ok` |
| **Role Violation** | Vendedor tentando aprovar cotação | ❌ DENIED | `Requer role: ['aprovador']` |
| **Required All Roles** | Gerente precisa ser Aprovador E Gerente | ✅ ALLOWED | `reason=ok` |
| **Permission Check** | Checagem direta por `cotacao:create` | ✅ ALLOWED | `reason=ok` |
| **ABAC Attribute** | Sistema = 'cotacao' | ✅ ALLOWED | `reason=ok` |
| **ABAC Violation** | Tentativa de acesso ao sistema 'financeiro' | ❌ DENIED | `Atributo esperado: financeiro, atual: cotacao` |
| **Custom Entity** | Cargo = 'gerente' | ✅ ALLOWED | `reason=ok` |
| **Combined Logic** | Role + Permissão + ABAC | ✅ ALLOWED | `reason=ok` |
| **Hierarchical Rank** | Level Rank >= 10 | ❌ DENIED | `rank=0 < 10` |

---

## 📊 3. KPIs de Performance da Run

<div align="center">

| Métrica | Valor |
| :--- | :--- |
| ⏱️ **Tempo Total de Execução** | 209.62s |
| ✅ **Testes Passados** | 97 |
| ❌ **Testes Falhos** | 0 |
| 📈 **Taxa de Sucesso** | 100% |
| 🆔 **ID da Versão** | v2.4.0-production |

</div>

---

## 🛠 4. Integração com mTLS (Zero-Trust)

Para interagir com o Apollo, o cliente deve possuir o par de chaves validado pela CA interna:

```python
# Exemplo de requisição protegida
import httpx

client = httpx.Client(
    verify="ca.crt", 
    cert=("client.crt", "client.key"),
    base_url="https://localhost:8443"
)

# O Apollo valida o certificado no handshake TLS antes mesmo da aplicação
response = client.post("/auth/check", json={"permission": "cotacao:approve"})
print(response.json()['allowed'])
```

---

## 🌓 5. Painel Administrativo & Observabilidade

O Apollo não é uma caixa preta. Ele oferece:
*   **Audit Trail:** Registro de QUEM, QUANDO e PORQUE um acesso foi negado ou permitido.
*   **Dynamic Settings:** Alteração em tempo real de expiração de tokens e limites de rate-limit.
*   **Hierarchy Mapping:** Visualização clara de como as permissões fluem dos grupos para os usuários.

---

## 👨‍🔬 Arquiteto do Sistema

<div align="left">
  <img src="https://github.com/chaos4455.png" width="100px;" style="border-radius: 50%; border: 3px solid #FF8C00; float: left; margin-right: 20px;">
  <b>Elias Andrade (chaos4455)</b><br>
  <i>Principal Solutions Architect & Security Engineer</i><br>
  Especialista em infraestrutura crítica, criptografia aplicada e automação inteligente.
  <br><br>
  <a href="https://www.linkedin.com/in/itilmgf"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://github.com/chaos4455"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>
</div>

<br clear="all">

---

<div align="center">
  <p style="color: #888;">© 2026 O2 Data Solutions | Projetado para Soberania Digital</p>
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png" width="100%">
</div>
