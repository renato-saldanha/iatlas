# Arquitetura: Assistente de Estudos com IA

## 📋 Visão Geral

Sistema full-stack de assistente de estudos alimentado por IA , permitindo que usuários analisem textos e PDFs através de resumos, perguntas de revisão e explicações simplificadas.
```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Navegador)                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Next.js 14 + TypeScript + React            │  │
│  │  - Autenticação (NextAuth.js v5)                     │  │
│  │  - UI com Tailwind + Shadcn/ui                       │  │
│  │  - Acessibilidade (WCAG 2.1 AA)                      │  │
│  │  - Mobile-first responsive design                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕
                    (HTTPS/REST API)
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   SERVIDOR (Fly.io)                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI + Python 3.11 + SQLAlchemy                  │  │
│  │                                                      │  │
│  │  Routes:                                             │  │
│  │  ├── /api/auth/* (login, register, google)          │  │
│  │  ├── /api/analyze/* (text, pdf)                      │  │
│  │  └── /api/history/* (list, get, delete)             │  │
│  │                                                      │  │
│  │  Services:                                           │  │
│  │  ├── auth_service.py (JWT, bcrypt)                  │  │
│  │  ├── ai_service.py (Claude API integration)         │  │
│  │  ├── pdf_service.py (pdfplumber)                    │  │
│  │  └── user_service.py (CRUD users)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│              BANCO DE DADOS (Fly.io PostgreSQL)             │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL 15                                       │  │
│  │                                                      │  │
│  │  Tables:                                             │  │
│  │  ├── users                                           │  │
│  │  ├── study_sessions                                  │  │
│  │  └── documents                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│           SERVIÇOS EXTERNOS (APIs)                          │
│                                                             │
│  ├── Gemini API (IA)                             │
│  ├── Google OAuth (Autenticação)                           │
│  └── Fly.io (Infraestrutura)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Autenticação

### 1. Email/Senha
```
┌──────────┐
│ Usuário  │
└────┬─────┘
     │ Digita email/senha
     ↓
┌─────────────────────────────────────┐
│ Frontend: Login Form                │
└─────────────────────────────────────┘
     │ POST /api/auth/login
     ↓
┌─────────────────────────────────────┐
│ Backend: AuthService.authenticate   │
│ - bcrypt.verify(password)           │
│ - JWT.encode(user_id)               │
└─────────────────────────────────────┘
     │ Retorna token
     ↓
┌─────────────────────────────────────┐
│ Frontend: NextAuth.js               │
│ - Salva session                     │
│ - Redireciona para /dashboard       │
└─────────────────────────────────────┘
```

### 2. Google OAuth
```
┌──────────┐
│ Usuário  │
└────┬─────┘
     │ Clica "Login com Google"
     ↓
┌─────────────────────────────────────┐
│ Frontend: NextAuth.js               │
│ - Redireciona para Google           │
└─────────────────────────────────────┘
     │ Usuário autoriza no Google
     ↓
┌─────────────────────────────────────┐
│ Frontend: NextAuth callback         │
│ POST /api/auth/google-login         │
└─────────────────────────────────────┘
     │ Email + Nome
     ↓
┌─────────────────────────────────────┐
│ Backend: AuthService                │
│ - Cria usuário se não existir       │
│ - JWT.encode(user_id)               │
└─────────────────────────────────────┘
     │ Retorna token
     ↓
┌─────────────────────────────────────┐
│ Frontend: NextAuth.js               │
│ - Salva session                     │
│ - Redireciona para /dashboard       │
└─────────────────────────────────────┘
```

---

## 📊 Fluxo de Análise de Texto
```
┌──────────────┐
│ Usuário      │
└────┬─────────┘
     │ Cola texto + seleciona tipo
     ↓
┌──────────────────────────────────────────┐
│ Frontend: TextInput Component            │
│ - Valida tamanho (50-50k chars)          │
│ - Exibe "Modo Criança" toggle            │
│ - Seleciona tipo: resume/qa/explain      │
└──────────────────────────────────────────┘
     │ POST /api/analyze/text
     │ {
     │   text: "...",
     │   analysis_type: "resume",
     │   kid_mode: false,
     │   age_level: null
     │ }
     ↓
┌──────────────────────────────────────────┐
│ Backend: /api/analyze/text Route         │
│ - Autenticação (JWT middleware)          │
│ - Validação de input                     │
└──────────────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────────┐
│ Backend: AIService.analyze()             │
│ - Seleciona prompt dinâmico              │
│ - Chama Claude API                       │
│ - Aguarda resposta (5-10s)               │
└──────────────────────────────────────────┘
     │ Resultado da IA
     ↓
┌──────────────────────────────────────────┐
│ Backend: StudySession Model              │
│ - Salva no PostgreSQL                    │
│ - Armazena tokens usados                 │
└──────────────────────────────────────────┘
     │ Retorna AnalyzeResponse
     ↓
┌──────────────────────────────────────────┐
│ Frontend: ResultsView Component          │
│ - Exibe resultado formatado              │
│ - Copy-to-clipboard                      │
│ - Link para histórico                    │
└──────────────────────────────────────────┘
```

---

## 📄 Fluxo de Análise de PDF
```
┌──────────────┐
│ Usuário      │
└────┬─────────┘
     │ Seleciona PDF
     ↓
┌──────────────────────────────────────────┐
│ Frontend: PDFUpload Component            │
│ - Validação (type, size)                 │
│ - FormData upload                        │
└──────────────────────────────────────────┘
     │ POST /api/analyze/pdf
     │ multipart/form-data
     ↓
┌──────────────────────────────────────────┐
│ Backend: /api/analyze/pdf Route          │
│ - Autenticação (JWT)                     │
│ - File validation                        │
└──────────────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────────┐
│ Backend: PDFService.extract_text()       │
│ - pdfplumber.open(pdf_bytes)             │
│ - Loop pages, extract text               │
│ - Truncate se > 50k chars                │
└──────────────────────────────────────────┘
     │ Texto extraído
     ↓
┌──────────────────────────────────────────┐
│ Backend: AIService.analyze()             │
│ - Processa como texto normal             │
│ - Claude API call                        │
└──────────────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────────┐
│ Backend: StudySession Model              │
│ - Salva resultado + file_size            │
└──────────────────────────────────────────┘
     │
     ↓
┌──────────────────────────────────────────┐
│ Frontend: ResultsView                    │
│ - Exibe resultado                        │
└──────────────────────────────────────────┘
```

---

## 🗄️ Esquema de Banco de Dados

### User Table
```sql
CREATE TABLE users (
  id VARCHAR PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  hashed_password VARCHAR,  -- NULL se Google auth
  full_name VARCHAR,
  is_active BOOLEAN DEFAULT true,
  auth_provider VARCHAR,     -- 'credentials' ou 'google'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### StudySession Table
```sql
CREATE TABLE study_sessions (
  id VARCHAR PRIMARY KEY,
  user_id VARCHAR FOREIGN KEY REFERENCES users(id),
  
  -- Documento original
  document_text TEXT NOT NULL,
  document_size INTEGER,  -- bytes
  
  -- Tipo de análise
  analysis_type VARCHAR,  -- 'resume', 'qa', 'explain'
  
  -- Modo criança
  kid_mode BOOLEAN DEFAULT false,
  age_level INTEGER,      -- 6-18
  
  -- Resultados (JSON)
  results JSONB NOT NULL,
  
  -- Tokens
  tokens_used INTEGER DEFAULT 0,
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_sessions_created_at ON study_sessions(created_at DESC);
CREATE INDEX idx_sessions_analysis_type ON study_sessions(analysis_type);
```

### Document Table (Opcional)
```sql
CREATE TABLE documents (
  id VARCHAR PRIMARY KEY,
  user_id VARCHAR FOREIGN KEY REFERENCES users(id),
  
  filename VARCHAR,
  original_text TEXT,
  file_size INTEGER,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Fluxo de Segurança

### Autenticação
```
Request com JWT
     ↓
├─ Middleware HTTPBearer
│  └─ Extrai token do header
│     ↓
├─ AuthService.decode_token()
│  └─ JWT.decode(token, SECRET_KEY)
│     └─ Valida assinatura + expiração
│        ↓
├─ get_current_user()
│  └─ Busca user no DB
│     └─ Verifica se ativo
│        ↓
└─ Request Permitido
```

### Hashing de Senhas
```
Senha Plain
     ↓
bcrypt.gensalt()
     ↓
bcrypt.hashpw(password, salt)
     ↓
Armazenado no DB (irreversível)
```

### JWT Token
```
Payload: {
  "sub": "user-id-uuid",
  "exp": 1704067200,  -- 24h
  "iat": 1703980800
}

Assinado com: SECRET_KEY (256-bit)
Algoritmo: HS256
```

---

## 🌍 Ambientes

### Desenvolvimento (Local)
```
Frontend: http://localhost:3000
Backend:  http://localhost:8000
DB:       postgresql://localhost:5432/study_ai_dev
```

### Produção (Fly.io)
```
Frontend: https://study-ai.vercel.app
Backend:  https://study-ai-backend.fly.dev
DB:       PostgreSQL Fly.io (managed)
```

---

## 🚀 CI/CD Pipeline
```
Developer Push
     ↓
GitHub Webhook
     ↓
├─ [GitHub Actions] Test Job
│  ├─ Run pytest (backend)
│  ├─ Run jest/cypress (frontend)
│  └─ Check coverage (70%+)
│     ↓
├─ If all tests pass ✅
│  ├─ Build Docker image
│  └─ Deploy to Fly.io
│     ↓
└─ Vercel Auto-deploy (frontend)
   └─ Build Next.js
      └─ Deploy to Vercel
```

**Arquivo:** `.github/workflows/deploy.yml`

---

## 📦 Estrutura de Pastas

### Backend
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── study_session.py
│   │   └── document.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── history.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── analyze.py
│   │   └── history.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── ai_service.py
│   │   ├── pdf_service.py
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # JWT, get_db, etc
│   │   └── security.py         # Hash, token funcs
│   │
│   └── database/
│       ├── __init__.py
│       └── db.py               # SQLAlchemy setup
│
├── migrations/                 # Alembic migrations
│   └── versions/
│       └── 001_initial.py
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_ai_service.py
│   ├── test_pdf_service.py
│   └── test_routes.py
│
├── requirements.txt
├── Dockerfile
├── fly.toml
├── .env.example
├── alembic.ini
└── README.md
```

### Frontend
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home/redirect
│   │   │
│   │   ├── auth/
│   │   │   ├── layout.tsx
│   │   │   └── login/
│   │   │       └── page.tsx
│   │   │
│   │   └── dashboard/
│   │       ├── layout.tsx
│   │       ├── page.tsx        # Main dashboard
│   │       │
│   │       ├── history/
│   │       │   ├── page.tsx
│   │       │   └── [id]/
│   │       │       └── page.tsx
│   │       │
│   │       └── analyze/
│   │           └── [id]/
│   │               └── page.tsx
│   │
│   ├── components/
│   │   ├── ui/                 # Shadcn components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   │
│   │   ├── Header.tsx
│   │   ├── TextInput.tsx
│   │   ├── PDFUpload.tsx
│   │   ├── ResultsView.tsx
│   │   ├── HistoryList.tsx
│   │   ├── LoadingState.tsx
│   │   └── ErrorState.tsx
│   │
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Auth helpers
│   │   └── utils.ts
│   │
│   ├── hooks/
│   │   └── useAnalyze.ts       # Custom hooks
│   │
│   └── styles/
│       └── globals.css
│
├── public/
│   └── favicon.ico
│
├── tests/
│   ├── __tests__/
│   │   ├── auth.test.tsx
│   │   ├── components.test.tsx
│   │   └── e2e.spec.ts
│   │
│   └── setup.ts
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── middleware.ts
├── auth.ts                     # NextAuth config
├── .env.example
└── README.md
```

---

## 🔌 APIs & Integrações

### Claude API
```python
from anthropic import Anthropic

client = Anthropic(api_key=ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": prompt
    }]
)
```

### Google OAuth
```typescript
import Google from "next-auth/providers/google";

Google({
  clientId: process.env.AUTH_GOOGLE_ID,
  clientSecret: process.env.AUTH_GOOGLE_SECRET,
})
```

### JWT (Python)
```python
import jwt
from datetime import datetime, timedelta

token = jwt.encode(
    {"sub": user_id, "exp": datetime.utcnow() + timedelta(hours=24)},
    SECRET_KEY,
    algorithm="HS256"
)

payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

---

## 📈 Performance & Escalabilidade

### Caching Strategy
```
Request → Cache Check (Redis, optional)
   ↓
   ├─ HIT: Return cached result
   │
   └─ MISS: Process request
      ├─ Query DB
      ├─ Call IA (if needed)
      └─ Cache result (TTL: 24h)
```

### Database Optimization
```
- Índices em user_id, created_at
- Query com relationship eager loading
- Paginação com skip/limit
- JSON fields para resultados flexíveis
```

### Frontend Performance
```
- Code splitting (Next.js automatic)
- Image optimization (next/image)
- Lazy loading de componentes
- Bundle size < 200KB gzipped
```

---

## 🛡️ Segurança

### Input Validation
```
Text:
- Min: 50 characters
- Max: 50,000 characters
- Sanitização: Strip tags

PDF:
- Max size: 50MB
- Allowed types: .pdf only
- Virus scan: Optional
```

### Rate Limiting
```
Optional implementação:
- 10 requests/min por usuário
- 100 requests/hour por IP
- Tokens: 100k/day por usuário
```

### HTTPS/CORS
```
- Force HTTPS em produção
- CORS: Allow only Vercel domain
- CSRF: NextAuth gerencia
```

---

## 📊 Monitoramento

### Logs
```bash
fly logs -a study-ai-backend
fly logs -a study-ai-db
```

### Métricas
```
- Response time (target < 2s)
- Error rate (target < 0.1%)
- Database queries (N+1 check)
- Token usage (track costs)
- Uptime (target 99.9%)
```

### Alerts (Opcional)
```
- High error rate
- Database connection lost
- Anthropic API quota exceeded
- Disk space low
```

---

## 🚀 Deployment Architecture
```
┌──────────────────────────────────────────┐
│         Frontend (Vercel)                │
│                                          │
│  - Next.js built & deployed              │
│  - CDN global distribution               │
│  - Auto-deploy from main branch          │
│  - Preview deployments for PRs           │
└──────────────────────────────────────────┘
              ↕ HTTPS ↕
┌──────────────────────────────────────────┐
│       Backend (Fly.io)                   │
│                                          │
│  - FastAPI container                     │
│  - Auto-scaling (optional)               │
│  - Health checks                         │
│  - Graceful shutdown                     │
└──────────────────────────────────────────┘
              ↕ TCP ↕
┌──────────────────────────────────────────┐
│   PostgreSQL (Fly.io)                    │
│                                          │
│  - Managed database                      │
│  - Automated backups                     │
│  - Replication (optional)                │
│  - Point-in-time recovery                │
└──────────────────────────────────────────┘
```

---

**Documento atualizado: 2026-01-06**
```
```

---

# COSTS.md
```markdown
# Análise de Custos

## 💰 Custo Mensal Estimado: **$0 (ZERO)**

---

## Breakdown por Serviço

### Frontend (Vercel)
```
Tier: Free
├─ Deployments: Ilimitados
├─ Storage: 100GB
├─ Bandwidth: 100GB/mês
├─ Build minutes: 6000/mês
└─ Custo: FREE

Alternativa Pro: $20/mês (não necessário para MVP)
```

### Backend (Fly.io)
```
Tier: Free
├─ Computação: 3 apps × 256MB RAM compartilhado
├─ Horas: Ilimitadas (não dorme)
├─ Banda: 160GB/mês egress
└─ Custo: FREE

Upgrade necessário se:
- Apps crescerem para > 512MB RAM
- Tráfego > 160GB/mês
- Estimado upgrade: $10-20/mês por app
```

### PostgreSQL (Fly.io)
```
Tier: Free
├─ Armazenamento: 3GB
├─ Backups: Automáticos
├─ Snapshots: Diários
├─ Replicação: Nenhuma (add $15/mês)
└─ Custo: FREE

Upgrade necessário se:
- DB crescer > 3GB
- Estimado: $15-30/mês por 10GB extra
```

### IA (Anthropic Claude)
```
Modelo: Claude 3.5 Sonnet

Pricing:
├─ Input:  $0.003 por 1K tokens
├─ Output: $0.015 por 1K tokens
└─ Total:  ~$0.009 por requisição média

Uso estimado (MVP):
├─ 100 análises/dia
├─ 500 tokens médios = 5K tokens
├─ Custo/dia: 100 × $0.009 = $0.90
├─ Custo/mês: $0.90 × 30 = $27
└─ Total: ~$25-40/mês

Otimizações para reduzir:
├─ Cache resultados similares
├─ Limitar tamanho de entrada
├─ Rate limiting por usuário
└─ Batch processing (futuro)
```

### Google OAuth
```
Tier: Free
├─ Autenticação: Ilimitada
├─ Custo: FREE
└─ Limite: Nenhum para MVP
```

### Outros Serviços (Opcional)
```
Sentry (Error tracking):
├─ Free tier: 5K events/mês
├─ Custo: FREE para MVP
└─ Upgrade: $29/mês depois

Analytics (Google Analytics):
├─ Free tier: Ilimitado
├─ Custo: FREE
└─ Alternativa: Vercel Analytics (FREE)

Email (Transacional):
├─ Sendgrid: 100 emails/dia grátis
├─ Custo: FREE para MVP
└─ Upgrade: $15/mês
```

---

## 📊 Resumo Financeiro

### Cenário 1: MVP (Ideal)
```
Serviço              Custo/mês
─────────────────────────────
Vercel               $0
Fly.io (Backend)     $0
Fly.io (PostgreSQL)  $0
Claude API           $30
─────────────────────────────
TOTAL               $30/mês

Sem créditos iniciais do Fly.io
```

### Cenário 2: Com Crédito Fly.io
```
Fly.io oferece $15 de crédito na assinatura

Serviço              Custo/mês
─────────────────────────────
Vercel               $0
Fly.io (Backend)     $0 (crédito)
Fly.io (PostgreSQL)  $0 (crédito)
Claude API           $30
─────────────────────────────
TOTAL               $30/mês

(Crédito cobrir primeiros ~2 meses)
```

### Cenário 3: Crescimento Moderado (6 meses)
```
Caso o app cresça para 1000 usuários ativos:

Serviço              Custo/mês
─────────────────────────────
Vercel               $0 (upgrade: $20)
Fly.io (Backend)     $10 (upgrade computação)
Fly.io (PostgreSQL)  $0 (upgrade: $15)
Claude API           $100 (mais requisições)
─────────────────────────────
TOTAL               $110/mês

(Ainda muito barato para SaaS)
```

---

## 🎯 Break-Even Point (Se Monetizar)

### Cenário Premium ($9/mês por usuário)
```
Usuários necessários: 30-50
├─ Receita: $270-450/mês
├─ Custos: $110/mês
└─ Lucro: $160-340/mês

Tempo para 50 usuários: 2-3 meses (esperado)
```

### Cenário Freemium ($3/mês por premium)
```
Usuários necessários: 100-150
├─ Receita: $300-450/mês
├─ Custos: $110/mês
└─ Lucro: $190-340/mês

Tempo para 150 usuários: 3-6 meses
```

---

## 💡 Estratégias de Redução de Custos

### IA (Maior custo)
```
1. Cache de resultados
   └─ Evita re-processar mesma análise
   
2. Summarização de texto automática
   └─ Truncar entrada em 2000 chars
   
3. Usar Claude 3 Haiku (mais barato)
   └─ $0.00025 input / $0.00125 output
   
4. Batch processing à noite
   └─ Processar análises em fila
   
Redução potencial: 50% (de $30 para $15)
```

### Infraestrutura
```
1. Usar SQLite em vez de PostgreSQL
   └─ Grátis, mas sem scaling
   
2. Usar Render em vez de Fly.io
   └─ Praticamente idêntico, free tier
   
3. Self-host em VPS barato
   └─ $5-10/mês (DigitalOcean)
   
Impacto: Minimal, já está otimizado
```

### Banda/Armazenamento
```
1. Compressão de imagens
   └─ Diminui tamanho de PDFs
   
2. Lazy loading no frontend
   └─ Reduz downloads iniciais
   
3. CDN caching (Vercel já faz)
   └─ Reutiliza assets
   
Impacto: Minimal, banda is free tier
```

---

## 🚀 Escalabilidade de Custos

### Usuários vs Custos
```
Usuários    IA/mês    Infra/mês    Total/mês    Custo/user
─────────────────────────────────────────────────────
100         $3        $0           $3           $0.03
500         $15       $0           $15          $0.03
1000        $30       $10          $40          $0.04
5000        $150      $30          $180         $0.036
10000       $300      $50          $350         $0.035

Cenário: 100 análises/usuário/mês
```

### ROI (Return on Investment)
```
Premium Plan: $9/mês

Usuários    Receita     Custos    Margem    Margem %
─────────────────────────────────────────────────────
100         $900        $3        $897      99.7%
500         $4500       $15       $4485     99.7%
1000        $9000       $40       $8960     99.6%
5000        $45000      $180      $44820    99.6%

Conclusão: ALTAMENTE LUCRATIVO
```

---

## 💎 Comparação com Alternativas

### Opção 1: Fly.io (Recomendado)
```
Free Tier: ✅ PostgreSQL + Computação grátis
Custo/mês: $30 (IA)
Escalabilidade: Excelente
Recomendação: ⭐⭐⭐⭐⭐
```

### Opção 2: Railway
```
Free Tier: ❌ Crédito $5 apenas
Custo/mês: $18 (infra) + $30 (IA) = $48
Escalabilidade: Boa
Recomendação: ⭐⭐⭐
```

### Opção 3: AWS
```
Free Tier: ✅ 750h EC2 + PostgreSQL
Custo/mês: $30 (IA) + $0-20 (após free)
Escalabilidade: Excelente
Recomendação: ⭐⭐⭐ (complexo)
```

### Opção 4: Heroku (Descontinuado)
```
Free Tier: ❌ Descontinuado 2022
Custo/mês: N/A
Escalabilidade: N/A
Recomendação: ❌
```

### Opção 5: DigitalOcean
```
Free Tier: ❌ Nenhum
Custo/mês: $5 (VPS) + $15 (DB) + $30 (IA) = $50
Escalabilidade: Boa
Recomendação: ⭐⭐⭐ (mais barato para crescimento)
```

---

## 🎁 Créditos & Promoções

### Fly.io
```
Crédito de inscrição: $15
├─ Validade: 30 dias
├─ Cobre: ~2 meses de uso total
└─ Após expiração: Pay-as-you-go
```

### GitHub Student Pack (Se aplicável)
```
Inclui:
├─ $50 em crédito Heroku (não aplicável, descontinuado)
├─ $100 em DigitalOcean
├─ Acesso a várias ferramentas
└─ Validade: 1 ano
```

### Anthropic (Claude API)
```
Nenhum crédito inicial
├─ Mas oferece: Trial mode (100 mensagens grátis)
└─ Depois: Pay-as-you-go
```

---

## 📋 Checklist Financeiro

### Antes do Lançamento
- [ ] Configurar billing alerts em Fly.io ($5/mês)
- [ ] Configurar billing alerts em Vercel
- [ ] Setup de monitoring de custos Anthropic
- [ ] Documentar preços atuais
- [ ] Testar escalabilidade com load tests

### Após Lançamento (30 dias)
- [ ] Revisar custos reais vs estimados
- [ ] Ajustar limites de tokens se necessário
- [ ] Otimizar prompts se Claude caro
- [ ] Análise de ROI

### Mensalmente
- [ ] Revisar faturas
- [ ] Verificar uso de banda/armazenamento
- [ ] Monitorar quantidade de usuários
- [ ] Projetar custos futuros

---

## 💬 FAQ de Custos

### P: Por que Claude API é o maior custo?
**R:** IA é cara. Cada análise consome tokens. Sem ele, seria $0/mês, mas sem IA.

### P: Como reduzir custos de IA?
**R:** Cache, truncar entrada, usar Haiku, batch processing. Alvo: 50% redução.

### P: E se crescer para 10k usuários?
**R:** ~$350/mês. Ainda muito barato. Com $9/user premium = $90k receita.

### P: Preciso de Sentry?
**R:** Não para MVP. Vercel oferece logs básicos grátis.

### P: PostgreSQL Fly.io é confiável?
**R:** Sim. Backups automáticos, snapshots, managed service.

### P: Posso usar SQLite em produção?
**R:** Não. Vários usuários simultâneos causam lock. Use PostgreSQL.

---

## 📈 Projeção 12 Meses
```
Mês  Usuários  IA      Infra   Total/mês  Acumulado
───────────────────────────────────────────────────
1    10        $1      $0      $1         $1
2    50        $5      $0      $5         $6
3    150       $15     $0      $15        $21
4    300       $30     $0      $30        $51
5    500       $50     $0      $50        $101
6    1000      $100    $10     $110       $211
7    1500      $150    $10     $160       $371
8    2500      $250    $20     $270       $641
9    4000      $400    $30     $430       $1071
10   6000      $600    $40     $640       $1711
11   8000      $800    $50     $850       $2561
12   10000     $1000   $60     $1060      $3621

Receita (assumindo $9/user premium com 30%):
Mês 12: 3000 × $9 = $27k/mês
Lucro: $27k - $1.06k = $25.94k/mês

ROI: 24 meses para break-even completo
```

---

**Documento atualizado: 2026-01-06**
```