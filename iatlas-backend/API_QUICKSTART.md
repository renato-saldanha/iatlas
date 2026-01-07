# IAtlas API - Guia de Início Rápido

## 🚀 Começando em 5 minutos

Este guia mostra como começar a usar a API do IAtlas rapidamente.

---

## 📋 Pré-requisitos

- Conta no IAtlas (registro via frontend ou API)
- Token de autenticação JWT
- Ferramenta para fazer requisições HTTP (curl, Postman, Insomnia, etc.)

---

## 🔐 Passo 1: Autenticação

### Registrar um novo usuário

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "senhaSegura123",
    "full_name": "Meu Nome"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "usuario@example.com",
    "full_name": "Meu Nome",
    "auth_provider": "credentials",
    "created_at": "2026-01-06T10:00:00Z"
  }
}
```

**Guarde o `access_token` para usar nas próximas requisições!**

### Ou fazer login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "senhaSegura123"
  }'
```

---

## 📊 Passo 2: Análise de Texto

### Exemplo 1: Resumo Simples

```bash
curl -X POST "http://localhost:8000/api/analyze/text" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "A inteligência artificial está transformando a educação. Com ferramentas como chatbots e sistemas de recomendação, os alunos podem receber ajuda personalizada 24 horas por dia. Os professores podem usar IA para criar materiais de ensino adaptativos e avaliar o progresso dos alunos de forma mais eficiente.",
    "analysis_type": "resume"
  }'
```

**Resposta esperada:**
```json
{
  "session_id": "abc-123-def-456",
  "analysis_type": "resume",
  "result": {
    "summary": "A inteligência artificial está revolucionando a educação através de chatbots, sistemas de recomendação e ferramentas adaptativas que oferecem suporte personalizado aos alunos e auxiliam professores na criação de materiais e avaliação.",
    "key_points": [
      "IA transforma educação com ferramentas personalizadas",
      "Suporte 24/7 para alunos via chatbots",
      "Materiais de ensino adaptativos para professores",
      "Avaliação mais eficiente do progresso dos alunos"
    ]
  },
  "tokens_used": 450,
  "created_at": "2026-01-06T10:05:00Z"
}
```

### Exemplo 2: Perguntas e Respostas

```bash
curl -X POST "http://localhost:8000/api/analyze/text" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "A fotossíntese é o processo pelo qual plantas, algas e algumas bactérias convertem luz solar em energia química. Durante esse processo, dióxido de carbono e água são transformados em glicose e oxigênio, usando a energia da luz solar capturada pela clorofila.",
    "analysis_type": "qa"
  }'
```

**Resposta esperada:**
```json
{
  "session_id": "xyz-789-abc-123",
  "analysis_type": "qa",
  "result": {
    "questions": [
      {
        "question": "O que é fotossíntese?",
        "answer": "Fotossíntese é o processo pelo qual plantas, algas e algumas bactérias convertem luz solar em energia química.",
        "difficulty": "easy"
      },
      {
        "question": "Quais são os produtos da fotossíntese?",
        "answer": "Os produtos da fotossíntese são glicose e oxigênio.",
        "difficulty": "medium"
      },
      {
        "question": "Qual pigmento é responsável por capturar a luz solar?",
        "answer": "A clorofila é o pigmento responsável por capturar a energia da luz solar durante a fotossíntese.",
        "difficulty": "medium"
      }
    ]
  },
  "tokens_used": 680,
  "created_at": "2026-01-06T10:10:00Z"
}
```

### Exemplo 3: Explicação de Termos (Modo Criança)

```bash
curl -X POST "http://localhost:8000/api/analyze/text" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "A fotossíntese é um processo complexo que envolve clorofila, glicose e oxigênio.",
    "analysis_type": "explain",
    "kid_mode": true,
    "age_level": 10
  }'
```

**Resposta esperada:**
```json
{
  "session_id": "kid-mode-123",
  "analysis_type": "explain",
  "result": {
    "terms": [
      {
        "term": "Fotossíntese",
        "explanation": "É como as plantas fazem sua própria comida! Elas usam a luz do sol para transformar água e gás carbônico em açúcar (glicose) e oxigênio.",
        "difficulty": "easy"
      },
      {
        "term": "Clorofila",
        "explanation": "É o pigmento verde que dá cor às folhas das plantas. É como uma 'antena' que captura a luz do sol para a fotossíntese.",
        "difficulty": "easy"
      },
      {
        "term": "Glicose",
        "explanation": "É um tipo de açúcar que as plantas produzem durante a fotossíntese. É a comida que elas usam para crescer e se manter vivas.",
        "difficulty": "easy"
      }
    ]
  },
  "tokens_used": 520,
  "created_at": "2026-01-06T10:15:00Z"
}
```

---

## 📄 Passo 3: Análise de PDF

```bash
curl -X POST "http://localhost:8000/api/analyze/pdf" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -F "file=@/caminho/para/seu/arquivo.pdf" \
  -F "analysis_type=resume" \
  -F "kid_mode=false"
```

**Com modo criança:**
```bash
curl -X POST "http://localhost:8000/api/analyze/pdf" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -F "file=@documento.pdf" \
  -F "analysis_type=explain" \
  -F "kid_mode=true" \
  -F "age_level=12"
```

---

## 📜 Passo 4: Consultar Histórico

### Listar todas as sessões

```bash
curl -X GET "http://localhost:8000/api/history" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Com paginação e filtros

```bash
curl -X GET "http://localhost:8000/api/history?skip=0&limit=5&analysis_type=resume&order_by=created_at&order_direction=desc" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Obter detalhes de uma sessão específica

```bash
curl -X GET "http://localhost:8000/api/history/abc-123-def-456" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Deletar uma sessão

```bash
curl -X DELETE "http://localhost:8000/api/history/abc-123-def-456" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## 🐍 Exemplo em Python

```python
import requests

# Configuração
BASE_URL = "http://localhost:8000"
TOKEN = "seu-token-aqui"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Análise de texto
def analyze_text(text: str, analysis_type: str, kid_mode: bool = False, age_level: int = None):
    url = f"{BASE_URL}/api/analyze/text"
    data = {
        "text": text,
        "analysis_type": analysis_type,
        "kid_mode": kid_mode
    }
    if kid_mode and age_level:
        data["age_level"] = age_level
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Exemplo de uso
result = analyze_text(
    text="Seu texto aqui...",
    analysis_type="resume",
    kid_mode=False
)
print(result)

# Listar histórico
def get_history(skip: int = 0, limit: int = 20):
    url = f"{BASE_URL}/api/history"
    params = {"skip": skip, "limit": limit}
    response = requests.get(url, params=params, headers=headers)
    return response.json()

history = get_history()
print(history)
```

---

## 🌐 Exemplo em JavaScript/TypeScript

```typescript
const BASE_URL = "http://localhost:8000";
const TOKEN = "seu-token-aqui";

const headers = {
  Authorization: `Bearer ${TOKEN}`,
  "Content-Type": "application/json",
};

// Análise de texto
async function analyzeText(
  text: string,
  analysisType: "resume" | "qa" | "explain",
  kidMode: boolean = false,
  ageLevel?: number
) {
  const response = await fetch(`${BASE_URL}/api/analyze/text`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      text,
      analysis_type: analysisType,
      kid_mode: kidMode,
      age_level: ageLevel,
    }),
  });
  return response.json();
}

// Exemplo de uso
const result = await analyzeText(
  "Seu texto aqui...",
  "resume",
  false
);
console.log(result);

// Listar histórico
async function getHistory(skip: number = 0, limit: number = 20) {
  const response = await fetch(
    `${BASE_URL}/api/history?skip=${skip}&limit=${limit}`,
    { headers }
  );
  return response.json();
}

const history = await getHistory();
console.log(history);
```

---

## ⚠️ Tratamento de Erros

### Exemplo em Python

```python
import requests

def safe_analyze(text: str):
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze/text",
            json={"text": text, "analysis_type": "resume"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Erro: Token inválido ou expirado")
        elif e.response.status_code == 400:
            print(f"Erro: {e.response.json()}")
        else:
            print(f"Erro HTTP {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
```

---

## 🔍 Verificar Health da API

```bash
curl -X GET "http://localhost:8000/health"
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T10:00:00Z",
  "version": "1.0.0"
}
```

---

## 📚 Próximos Passos

1. **Explore a documentação interativa:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

2. **Leia a documentação completa:**
   - Veja `API.md` para detalhes completos de todos os endpoints

3. **Integre com seu frontend:**
   - Use os exemplos acima como base para sua integração

---

## 🆘 Problemas Comuns

### Token expirado
**Sintoma:** Erro 401 Unauthorized  
**Solução:** Faça login novamente para obter um novo token

### Texto muito curto
**Sintoma:** Erro 400 Bad Request  
**Solução:** Certifique-se de que o texto tem pelo menos 50 caracteres

### PDF muito grande
**Sintoma:** Erro 400 Bad Request  
**Solução:** Reduza o tamanho do PDF para menos de 50MB

### Erro ao processar PDF
**Sintoma:** Erro 500 Internal Server Error  
**Solução:** Verifique se o PDF não está corrompido e tente novamente

---

**Última atualização:** 2026-01-06

