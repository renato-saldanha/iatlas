# IAtlas API Documentation

## 📋 Visão Geral

A API do IAtlas é uma REST API construída com FastAPI que fornece funcionalidades de análise de texto e PDF usando IA (Gemini via LangChain). A API suporta autenticação via JWT e oferece três tipos de análise: resumo, perguntas e respostas, e explicação de termos.

**Base URL:** `https://study-ai-backend.fly.dev` (produção) ou `http://localhost:8000` (desenvolvimento)

**Versão:** 1.0.0

---

## 🔐 Autenticação

A API utiliza autenticação baseada em JWT (JSON Web Tokens). A maioria dos endpoints requer um token de autenticação no header da requisição.

### Como obter um token

1. **Registro de usuário** (`POST /api/auth/register`)
2. **Login** (`POST /api/auth/login`)
3. **Login com Google** (`POST /api/auth/google-login`)

### Uso do token

Após obter o token, inclua-o no header de todas as requisições autenticadas:

```
Authorization: Bearer <seu-token-jwt>
```

**Validade do token:** 24 horas

---

## 📚 Endpoints

### 🔑 Autenticação

#### `POST /api/auth/register`

Registra um novo usuário com email e senha.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "senhaSegura123",
  "full_name": "Nome Completo"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-do-usuario",
    "email": "usuario@example.com",
    "full_name": "Nome Completo",
    "auth_provider": "credentials",
    "created_at": "2026-01-06T10:00:00Z"
  }
}
```

**Erros:**
- `400 Bad Request`: Email já existe ou dados inválidos
- `422 Unprocessable Entity`: Validação de schema falhou

---

#### `POST /api/auth/login`

Autentica um usuário existente com email e senha.

**Request Body:**
```json
{
  "email": "usuario@example.com",
  "password": "senhaSegura123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-do-usuario",
    "email": "usuario@example.com",
    "full_name": "Nome Completo",
    "auth_provider": "credentials",
    "created_at": "2026-01-06T10:00:00Z"
  }
}
```

**Erros:**
- `401 Unauthorized`: Credenciais inválidas
- `404 Not Found`: Usuário não encontrado

---

#### `POST /api/auth/google-login`

Autentica ou cria um usuário usando Google OAuth.

**Request Body:**
```json
{
  "email": "usuario@gmail.com",
  "full_name": "Nome do Google",
  "google_id": "google-user-id"
}
```

**Response (200 OK ou 201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-do-usuario",
    "email": "usuario@gmail.com",
    "full_name": "Nome do Google",
    "auth_provider": "google",
    "created_at": "2026-01-06T10:00:00Z"
  }
}
```

---

#### `GET /api/auth/me`

Retorna informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-do-usuario",
  "email": "usuario@example.com",
  "full_name": "Nome Completo",
  "auth_provider": "credentials",
  "is_active": true,
  "created_at": "2026-01-06T10:00:00Z",
  "updated_at": "2026-01-06T10:00:00Z"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido ou expirado

---

### 📊 Análise de Conteúdo

#### `POST /api/analyze/text`

Analisa um texto fornecido e retorna o resultado baseado no tipo de análise solicitado.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Texto a ser analisado. Deve ter entre 50 e 50.000 caracteres...",
  "analysis_type": "resume",
  "kid_mode": false,
  "age_level": null
}
```

**Parâmetros:**
- `text` (string, obrigatório): Texto a ser analisado (50-50.000 caracteres)
- `analysis_type` (string, obrigatório): Tipo de análise
  - `"resume"`: Gera um resumo do texto
  - `"qa"`: Gera perguntas e respostas sobre o texto
  - `"explain"`: Explica termos e conceitos do texto
- `kid_mode` (boolean, opcional): Se `true`, usa linguagem simplificada (padrão: `false`)
- `age_level` (integer, opcional): Nível de idade para modo criança (6-18 anos, requer `kid_mode: true`)

**Response (200 OK):**
```json
{
  "session_id": "uuid-da-sessao",
  "analysis_type": "resume",
  "result": {
    "summary": "Resumo do texto analisado...",
    "key_points": [
      "Ponto principal 1",
      "Ponto principal 2"
    ]
  },
  "tokens_used": 1250,
  "created_at": "2026-01-06T10:00:00Z"
}
```

**Exemplo com modo criança:**
```json
{
  "text": "Texto sobre fotossíntese...",
  "analysis_type": "explain",
  "kid_mode": true,
  "age_level": 10
}
```

**Erros:**
- `400 Bad Request`: Texto muito curto ou muito longo
- `401 Unauthorized`: Token inválido
- `422 Unprocessable Entity`: Validação de schema falhou
- `500 Internal Server Error`: Erro ao processar com IA

---

#### `POST /api/analyze/pdf`

Analisa um arquivo PDF enviado e retorna o resultado baseado no tipo de análise solicitado.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
- `file` (file, obrigatório): Arquivo PDF (máximo 50MB)
- `analysis_type` (string, obrigatório): Tipo de análise (`"resume"`, `"qa"`, `"explain"`)
- `kid_mode` (boolean, opcional): Modo criança (padrão: `false`)
- `age_level` (integer, opcional): Nível de idade (6-18, requer `kid_mode: true`)

**Response (200 OK):**
```json
{
  "session_id": "uuid-da-sessao",
  "analysis_type": "qa",
  "result": {
    "questions": [
      {
        "question": "Qual é o tema principal do documento?",
        "answer": "O tema principal é...",
        "difficulty": "medium"
      },
      {
        "question": "Quais são os pontos-chave mencionados?",
        "answer": "Os pontos-chave são...",
        "difficulty": "easy"
      }
    ]
  },
  "document_size": 1024000,
  "tokens_used": 3500,
  "created_at": "2026-01-06T10:00:00Z"
}
```

**Erros:**
- `400 Bad Request`: Arquivo muito grande ou formato inválido
- `401 Unauthorized`: Token inválido
- `422 Unprocessable Entity`: Validação falhou
- `500 Internal Server Error`: Erro ao processar PDF ou IA

---

### 📜 Histórico

#### `GET /api/history`

Lista todas as sessões de análise do usuário autenticado com paginação.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (integer, opcional): Número de registros para pular (padrão: 0)
- `limit` (integer, opcional): Número máximo de registros (padrão: 20, máximo: 100)
- `analysis_type` (string, opcional): Filtrar por tipo (`"resume"`, `"qa"`, `"explain"`)
- `order_by` (string, opcional): Ordenação (`"created_at"` ou `"tokens_used"`, padrão: `"created_at"`)
- `order_direction` (string, opcional): Direção (`"asc"` ou `"desc"`, padrão: `"desc"`)

**Exemplo de requisição:**
```
GET /api/history?skip=0&limit=10&analysis_type=resume&order_by=created_at&order_direction=desc
```

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "id": "uuid-da-sessao-1",
      "analysis_type": "resume",
      "kid_mode": false,
      "document_size": null,
      "tokens_used": 1250,
      "created_at": "2026-01-06T10:00:00Z",
      "preview": "Primeiros 200 caracteres do texto original..."
    },
    {
      "id": "uuid-da-sessao-2",
      "analysis_type": "qa",
      "kid_mode": true,
      "age_level": 10,
      "document_size": 1024000,
      "tokens_used": 3500,
      "created_at": "2026-01-05T15:30:00Z",
      "preview": "Primeiros 200 caracteres do texto original..."
    }
  ],
  "total": 45,
  "skip": 0,
  "limit": 10
}
```

**Erros:**
- `401 Unauthorized`: Token inválido

---

#### `GET /api/history/{session_id}`

Retorna detalhes completos de uma sessão de análise específica.

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `session_id` (string, obrigatório): UUID da sessão

**Response (200 OK):**
```json
{
  "id": "uuid-da-sessao",
  "user_id": "uuid-do-usuario",
  "document_text": "Texto completo original...",
  "document_size": 1024000,
  "analysis_type": "explain",
  "kid_mode": true,
  "age_level": 12,
  "results": {
    "terms": [
      {
        "term": "Fotossíntese",
        "explanation": "Processo pelo qual plantas convertem luz solar em energia...",
        "difficulty": "medium"
      },
      {
        "term": "Clorofila",
        "explanation": "Pigmento verde encontrado nas plantas...",
        "difficulty": "easy"
      }
    ]
  },
  "tokens_used": 2800,
  "created_at": "2026-01-06T10:00:00Z"
}
```

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Sessão pertence a outro usuário
- `404 Not Found`: Sessão não encontrada

---

#### `DELETE /api/history/{session_id}`

Deleta uma sessão de análise específica.

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `session_id` (string, obrigatório): UUID da sessão

**Response (204 No Content):**

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Sessão pertence a outro usuário
- `404 Not Found`: Sessão não encontrada

---

### 🏥 Health Check

#### `GET /health`

Endpoint de health check para monitoramento.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T10:00:00Z",
  "version": "1.0.0"
}
```

---

## 📝 Schemas de Dados

### User Schema
```json
{
  "id": "string (UUID)",
  "email": "string (email válido)",
  "full_name": "string (opcional)",
  "hashed_password": "string (nunca retornado na API)",
  "is_active": "boolean",
  "auth_provider": "string ('credentials' ou 'google')",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

### StudySession Schema
```json
{
  "id": "string (UUID)",
  "user_id": "string (UUID)",
  "document_text": "string (TEXT)",
  "document_size": "integer (bytes, opcional)",
  "analysis_type": "string ('resume', 'qa', 'explain')",
  "kid_mode": "boolean",
  "age_level": "integer (6-18, opcional)",
  "results": "object (JSONB)",
  "tokens_used": "integer",
  "created_at": "string (ISO 8601 datetime)"
}
```

### Analysis Result Schemas

#### Resume Result
```json
{
  "summary": "string",
  "key_points": ["string"]
}
```

#### Q&A Result
```json
{
  "questions": [
    {
      "question": "string",
      "answer": "string",
      "difficulty": "string ('easy', 'medium', 'hard')"
    }
  ]
}
```

#### Explain Result
```json
{
  "terms": [
    {
      "term": "string",
      "explanation": "string",
      "difficulty": "string ('easy', 'medium', 'hard')"
    }
  ]
}
```

---

## ⚠️ Códigos de Erro

| Código | Descrição |
|--------|-----------|
| `200` | OK - Requisição bem-sucedida |
| `201` | Created - Recurso criado com sucesso |
| `204` | No Content - Recurso deletado com sucesso |
| `400` | Bad Request - Dados inválidos na requisição |
| `401` | Unauthorized - Token ausente ou inválido |
| `403` | Forbidden - Acesso negado ao recurso |
| `404` | Not Found - Recurso não encontrado |
| `422` | Unprocessable Entity - Validação de schema falhou |
| `500` | Internal Server Error - Erro interno do servidor |

---

## 🔒 Limites e Validações

### Texto
- **Mínimo:** 50 caracteres
- **Máximo:** 50.000 caracteres

### PDF
- **Tamanho máximo:** 50 MB
- **Formato:** Apenas arquivos `.pdf`

### Modo Criança
- **age_level:** Deve estar entre 6 e 18 anos
- **Requer:** `kid_mode: true`

### Paginação
- **skip:** Mínimo 0
- **limit:** Mínimo 1, máximo 100 (padrão: 20)

---

## 📖 Exemplos de Uso

### Exemplo 1: Análise de Texto Simples

```bash
curl -X POST "https://study-ai-backend.fly.dev/api/analyze/text" \
  -H "Authorization: Bearer <seu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "A fotossíntese é o processo pelo qual plantas e outros organismos convertem luz solar em energia química...",
    "analysis_type": "resume"
  }'
```

### Exemplo 2: Análise de PDF com Modo Criança

```bash
curl -X POST "https://study-ai-backend.fly.dev/api/analyze/pdf" \
  -H "Authorization: Bearer <seu-token>" \
  -F "file=@documento.pdf" \
  -F "analysis_type=explain" \
  -F "kid_mode=true" \
  -F "age_level=10"
```

### Exemplo 3: Listar Histórico

```bash
curl -X GET "https://study-ai-backend.fly.dev/api/history?skip=0&limit=10" \
  -H "Authorization: Bearer <seu-token>"
```

### Exemplo 4: Obter Detalhes de uma Sessão

```bash
curl -X GET "https://study-ai-backend.fly.dev/api/history/uuid-da-sessao" \
  -H "Authorization: Bearer <seu-token>"
```

---

## 🚀 Rate Limiting

**Nota:** Rate limiting pode ser implementado no futuro. Atualmente não há limites rígidos, mas recomenda-se:
- Máximo 10 requisições por minuto por usuário
- Máximo 100 requisições por hora por IP

---

## 📚 Documentação Interativa

A API inclui documentação interativa gerada automaticamente pelo FastAPI:

- **Swagger UI:** `https://study-ai-backend.fly.dev/docs`
- **ReDoc:** `https://study-ai-backend.fly.dev/redoc`
- **OpenAPI Schema:** `https://study-ai-backend.fly.dev/openapi.json`

---

## 🔄 Versionamento

A API segue versionamento semântico. A versão atual é **1.0.0**.

Mudanças futuras serão documentadas em:
- Versões menores (1.0.x): Correções de bugs, sem breaking changes
- Versões maiores (1.x.0): Novas features, possíveis breaking changes
- Versões major (x.0.0): Breaking changes significativos

---

## 🛠️ Suporte e Contato

Para suporte, reportar bugs ou solicitar features:
- **GitHub Issues:** [Link do repositório]
- **Email:** [Email de suporte]

---

## 📄 Licença

[Especificar licença do projeto]

---

**Última atualização:** 2026-01-06

