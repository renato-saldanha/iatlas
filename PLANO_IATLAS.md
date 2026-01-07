# IAtlas backend


# Plano de Desenvolvimento: Assistente de Estudos com IA
## Full-Stack com Auth Google + Credentials + PostgreSQL + Fly.io

---

## 1. Fase 0: Preparação (1-2 semanas)

### 1.1 Setup Inicial
- [ X] Criar repositório Git (monorepo com `/frontend` e `/backend`)
- [ x] Configurar estrutura de pastas (backend: models, routes, services, schemas, utils)
- [ x] Configurar variáveis de ambiente 
- [ x] Documentação inicial (README, arquitetura, API docs)
- [ ] Criar issues/tasks no GitHub Projects

### 1.2 Infraestrutura

#### Conta Fly.io
- [ ] Registrar em https://fly.io
- [ ] Verificar email
- [ ] Instalar Fly CLI (`curl -L https://fly.io/install.sh | sh`)
- [ ] Fazer login (`fly auth login`)

#### PostgreSQL no Fly.io
- [ ] Criar app PostgreSQL: `fly postgres create --name study-ai-db`
- [ ] Anotar connection string (DATABASE_URL)
- [ ] Criar backup automático (opcional)
- [ ] Testar conexão local

#### Aplicação Backend no Fly.io
- [ ] Criar app Web Service: `fly apps create study-ai-backend`
- [ ] Anexar PostgreSQL: `fly postgres attach study-ai-db --app study-ai-backend`
- [ ] Configurar regra de health check

#### Outras Contas
- [ ] Registrar aplicação Google OAuth (obter CLIENT_ID e CLIENT_SECRET)
- [ ] Configurar conta Anthropic (obter API KEY Claude)
- [ ] Configurar conta Vercel para deploy frontend

### 1.3 Dependências & Ferramentas
- [ ] Gerar `requirements.txt` (FastAPI, SQLAlchemy, Anthropic, pdfplumber, bcrypt, JWT, etc)
- [ ] Gerar `package.json` (Next.js, NextAuth, Tailwind, Shadcn/ui, axios)
- [ ] Instalar e configurar linters/formatters (Black, Prettier)
- [ ] Setup Docker para desenvolvimento local

### 1.4 Configuração Fly.io Específica
- [ ] Criar `fly.toml` (configuração Fly.io)
- [ ] Criar `Dockerfile` (opcional, para mais controle)
- [ ] Configurar variáveis de ambiente em Fly.io:
```bash
  fly secrets set -a study-ai-backend \
    SECRET_KEY="your-secret-key" \
    ANTHROPIC_API_KEY="sk-..." \
    ENVIRONMENT="production"
```
- [ ] Testar deploy automático via GitHub

---

## 2. Fase 1: Backend Core (2-3 semanas)

### 2.1 Database & ORM
- [ ] Configurar PostgreSQL Fly.io (connection string)
- [ ] Criar models SQLAlchemy (User, StudySession, Document)
- [ ] Setup Alembic para migrations
- [ ] Criar migration inicial
- [ ] Testes de conexão DB (local + Fly.io)

**Deliverables:**
- [ ] `app/database/db.py` (engine, session)
- [ ] `app/models/user.py`, `study_session.py`, `document.py`
- [ ] `migrations/versions/001_initial.py`
- [ ] `fly.toml` com configurações de conexão

### 2.2 Autenticação
- [ ] Implementar hashing de senhas (bcrypt)
- [ ] Criar JWT token generation/validation
- [ ] Endpoint POST `/api/auth/register` (email/senha)
- [ ] Endpoint POST `/api/auth/login` (email/senha)
- [ ] Endpoint POST `/api/auth/google-login` (integração NextAuth)
- [ ] Endpoint GET `/api/auth/me` (usuário logado)
- [ ] Middleware de autenticação (HTTPBearer + JWT)

**Deliverables:**
- [ ] `app/services/auth_service.py`
- [ ] `app/routes/auth.py`
- [ ] `app/utils/dependencies.py` (get_current_user)
- [ ] `app/utils/security.py` (hashing, token)

### 2.3 Schemas & Validação
- [ ] Pydantic schemas para User (create, login, response)
- [ ] Pydantic schemas para Analysis (request, response)
- [ ] Pydantic schemas para History
- [ ] Validações customizadas (tamanho de texto, tipos de análise)

**Deliverables:**
- [ ] `app/schemas/user.py`
- [ ] `app/schemas/analysis.py`
- [ ] `app/schemas/history.py`

### 2.4 Testes Básicos
- [ ] Testes unitários de auth (hashing, token)
- [ ] Testes de endpoints (registro, login)
- [ ] Cobertura mínima: 60%

**Deliverables:**
- [ ] `tests/test_auth.py`
- [ ] `tests/test_models.py`

### 2.5 Deploy Inicial Fly.io
- [ ] Criar `fly.toml` com configurações básicas
- [ ] Conectar repo GitHub para auto-deploy
- [ ] Testar deploy automático (push → Fly.io)
- [ ] Verificar logs em `fly logs -a study-ai-backend`
- [ ] Testar health check

**Deliverables:**
- [ ] `fly.toml` funcional
- [ ] GitHub Actions para auto-deploy (opcional)

---

## 3. Fase 2: IA & Analysis (1-2 semanas)

### 3.1 Integração Claude API
- [ ] Configurar cliente Anthropic
- [ ] Implementar método `analyze()` com 3 tipos
  - [ ] Resumo (resume)
  - [ ] Perguntas (Q&A)
  - [ ] Explicação de termos (explain)
- [ ] Tratamento de erros (timeout, quota)
- [ ] Logging de tokens usados
- [ ] Testar em Fly.io (variável de ambiente ANTHROPIC_API_KEY)

**Deliverables:**
- [ ] `app/services/ai_service.py`
- [ ] Documentação de prompts

### 3.2 Modo Criança (Simple Explanation)
- [ ] Adicionar parâmetro `kid_mode` boolean
- [ ] Adicionar parâmetro `age_level` (6-18 anos)
- [ ] Ajustar prompts para linguagem simples
- [ ] Testar diferentes idades

**Deliverables:**
- [ ] Métodos em `ai_service.py` com prompts dinâmicos

### 3.3 PDF Processing
- [ ] Implementar extração de texto com pdfplumber
- [ ] Validação de tamanho máximo (50MB)
- [ ] Tratamento de PDFs com imagens/scans
- [ ] Endpoint POST `/api/analyze/pdf`
- [ ] Testar upload em Fly.io

**Deliverables:**
- [ ] `app/services/pdf_service.py`
- [ ] Rota de análise de PDF

### 3.4 Routes de Análise
- [ ] Endpoint POST `/api/analyze/text` (análise de texto)
- [ ] Endpoint POST `/api/analyze/pdf` (análise de PDF)
- [ ] Salvar resultado no banco (StudySession)
- [ ] Retornar análise + tokens usados

**Deliverables:**
- [ ] `app/routes/analyze.py`

### 3.5 Testes
- [ ] Mock de Claude API (não chamar em testes)
- [ ] Testes de analyze_text
- [ ] Testes de PDF extraction
- [ ] Cobertura: 70%+

**Deliverables:**
- [ ] `tests/test_ai_service.py`
- [ ] `tests/test_pdf_service.py`

### 3.6 Deploy em Fly.io
- [ ] Testar IA chamadas em produção
- [ ] Monitorar logs: `fly logs -a study-ai-backend`
- [ ] Verificar consumo de tokens
- [ ] Implementar rate limiting (opcional)

---

## 4. Fase 3: Histórico & Query (1 semana)

### 4.1 History Routes
- [ ] Endpoint GET `/api/history` (lista paginada)
- [ ] Endpoint GET `/api/history/{session_id}` (detalhes)
- [ ] Endpoint DELETE `/api/history/{session_id}` (deletar)
- [ ] Filtros: data, tipo de análise, ordenação
- [ ] Paginação (skip, limit)

**Deliverables:**
- [ ] `app/routes/history.py`

### 4.2 Queries Otimizadas
- [ ] Query com relationship user
- [ ] Agregações (total de tokens, quantidade de sessões)
- [ ] Índices em user_id, created_at

**Deliverables:**
- [ ] Migrations com índices

### 4.3 Testes
- [ ] Testes de listagem
- [ ] Testes de paginação
- [ ] Testes de deleção

---

## 5. Fase 4: Polish Backend (1 semana)

### 5.1 Config & Environment
- [ ] `app/config.py` com Settings
- [ ] Validação de variáveis obrigatórias
- [ ] Diferentes configs por ambiente (dev, prod)
- [ ] Integração com Fly.io secrets

### 5.2 CORS & Security
- [ ] CORS configurado com allowed_origins
- [ ] Rate limiting (opcional)
- [ ] Input validation & sanitization
- [ ] Error handling consistente

### 5.3 Main App
- [ ] `app/main.py` com all routers
- [ ] Health check endpoint
- [ ] Swagger docs automático
- [ ] Init de DB (migrations automáticas)

### 5.4 Logging & Observability
- [ ] Setup logging estruturado
- [ ] Log de requisições importantes
- [ ] Monitoramento em Fly.io (fly logs)
- [ ] Sentry integration (opcional)

**Deliverables:**
- [ ] `app/main.py` finalizado
- [ ] `app/config.py`

### 5.5 Documentação Backend
- [ ] README com setup local
- [ ] API docs (Swagger automático)
- [ ] Exemplo de .env
- [ ] Guia Fly.io deployment

---

## 6. Fase 5: Frontend Auth (1-2 semanas)

### 6.1 NextAuth Setup
- [ ] Instalar NextAuth.js v5
- [ ] Configurar Credentials provider (email/senha)
- [ ] Configurar Google provider
- [ ] Criar `auth.ts` com callbacks
- [ ] Setup middleware para protected routes
- [ ] Conectar ao backend Fly.io (usar URL pública)

**Deliverables:**
- [ ] `frontend/auth.ts`
- [ ] `frontend/middleware.ts`

### 6.2 Login Page (UX/A11y Focado)
- [ ] Página `/auth/login`
- [ ] Formulário email/senha (com pré-preenchimento: lavaprato@email.com / cyvsza5r)
- [ ] Botão "Login com Google"
- [ ] Validações client-side
- [ ] Tratamento de erros (feedback visual)
- [ ] Acessibilidade: labels, ARIA, contraste
- [ ] Loading states
- [ ] Redirect automático após login

**Deliverables:**
- [ ] `frontend/src/app/auth/login/page.tsx`
- [ ] Componente reutilizável de formulário

### 6.3 Session Management
- [ ] Hook useSession (Next.js)
- [ ] getSession server-side
- [ ] Logout functionality
- [ ] Refresh token (se necessário)

**Deliverables:**
- [ ] `frontend/lib/auth.ts` (helpers)

### 6.4 Testes
- [ ] Testes de login
- [ ] Testes de logout
- [ ] Redirecionamento pós-auth

---

## 7. Fase 6: Frontend UI Core (1-2 semanas)

### 7.1 Setup Next.js & Styling
- [ ] Criar projeto Next.js 14 com TypeScript
- [ ] Tailwind CSS configurado
- [ ] Shadcn/ui setup
- [ ] Fonte acessível (ex: Inter, Roboto)
- [ ] Dark mode (opcional)

### 7.2 Layout Base
- [ ] Root layout com NextAuth provider
- [ ] Header com usuário logado + logout
- [ ] Navegação (dashboard, history)
- [ ] Footer (opcional)
- [ ] Responsive mobile-first

**Deliverables:**
- [ ] `frontend/src/app/layout.tsx`
- [ ] `frontend/src/components/Header.tsx`

### 7.3 Dashboard Page
- [ ] Página principal `/dashboard`
- [ ] Protected (redirect se não logado)
- [ ] Layout com 2 colunas (input + histórico)
- [ ] Responsive (stack vertical em mobile)

**Deliverables:**
- [ ] `frontend/src/app/dashboard/page.tsx`

### 7.4 API Client
- [ ] Classe `APIClient` com métodos type-safe
- [ ] Gestão de tokens (Authorization header)
- [ ] Error handling uniforme
- [ ] Retry logic (opcional)
- [ ] Apontar para URL do Fly.io em produção

**Deliverables:**
- [ ] `frontend/lib/api.ts`

### 7.5 Componentes Shadcn
- [ ] Button
- [ ] Input
- [ ] Textarea
- [ ] Select
- [ ] Tabs
- [ ] Card
- [ ] Toast/Alert
- [ ] Dialog (para confirmações)

---

## 8. Fase 7: Análise & Resultados (1-2 semanas)

### 8.1 Text Input Component
- [ ] Textarea grande
- [ ] Contador de caracteres
- [ ] Validação (min 50 chars, max 50k)
- [ ] Botão "Analisar" com estados
- [ ] Seletor de tipo (resume, QA, explain)
- [ ] Toggle "Modo Criança"
- [ ] Slider de idade (se kid mode ativo)
- [ ] Acessibilidade completa (labels, ARIA)

**Deliverables:**
- [ ] `frontend/src/components/TextInput.tsx`

### 8.2 PDF Upload Component
- [ ] Input file ou drag-drop
- [ ] Validação (apenas PDF)
- [ ] Progresso de upload
- [ ] Preview do nome do arquivo
- [ ] Tratamento de erros
- [ ] Acessibilidade (labels, error messages)

**Deliverables:**
- [ ] `frontend/src/components/PDFUpload.tsx`

### 8.3 Results Display Component
- [ ] Exibição de resumo formatado
- [ ] Lista de perguntas com dificuldade
- [ ] Cards de explicação de termos
- [ ] Navegação entre tipos de análise
- [ ] Copy-to-clipboard para resultados
- [ ] Acessibilidade (headings, semantic HTML)

**Deliverables:**
- [ ] `frontend/src/components/ResultsView.tsx`

### 8.4 Loading & Error States
- [ ] Skeleton loaders (Shadcn)
- [ ] Error boundaries
- [ ] Toast notifications
- [ ] Retry buttons

**Deliverables:**
- [ ] `frontend/src/components/LoadingState.tsx`
- [ ] `frontend/src/components/ErrorState.tsx`

### 8.5 Integration
- [ ] Conectar TextInput → API Fly.io
- [ ] Conectar PDFUpload → API Fly.io
- [ ] Exibir resultados em ResultsView
- [ ] Loading states durante requisição

---

## 9. Fase 8: Histórico & Navigation (1 semana)

### 9.1 History List Component
- [ ] Cards com sessões anteriores
- [ ] Data/hora formatadas
- [ ] Ícone do tipo (resumo, QA, explain)
- [ ] Badge "Modo Criança" se aplicável
- [ ] Botão delete com confirmação
- [ ] Click para visualizar detalhes

**Deliverables:**
- [ ] `frontend/src/components/HistoryList.tsx`

### 9.2 History Page
- [ ] Página `/dashboard/history`
- [ ] Listagem paginada
- [ ] Filtros (tipo, data range)
- [ ] Busca (opcional)
- [ ] Estatísticas (total de sessões, tokens usados)

**Deliverables:**
- [ ] `frontend/src/app/dashboard/history/page.tsx`

### 9.3 Session Detail Page
- [ ] Página `/dashboard/history/:id`
- [ ] Exibir resultado completo
- [ ] Texto original em collapse
- [ ] Delete button
- [ ] Back button

**Deliverables:**
- [ ] `frontend/src/app/dashboard/history/[id]/page.tsx`

### 9.4 Navigation
- [ ] Links entre pages
- [ ] Breadcrumbs (opcional)
- [ ] Active tab indication

---

## 10. Fase 9: Acessibilidade (A11y) (1 semana)

### 10.1 WCAG 2.1 Compliance (AA Level)
- [ ] Contraste de cores (4.5:1 para texto)
- [ ] Fontes legíveis (16px+)
- [ ] Responsive design (mobile friendly)
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Sem traps de teclado

### 10.2 Screen Reader Support
- [ ] ARIA labels em botões
- [ ] ARIA descriptions em inputs
- [ ] Semantic HTML (nav, main, section)
- [ ] Alt text em ícones
- [ ] Form labels associadas (htmlFor)

### 10.3 Visual Accessibility
- [ ] Focus indicators visíveis
- [ ] Color not sole differentiator
- [ ] Icons + text para ações
- [ ] Adequate spacing para clicks (44px+)

### 10.4 Motion & Animation
- [ ] Respeitar prefers-reduced-motion
- [ ] Disable animations se necessário

### 10.5 Testing
- [ ] axe DevTools scan
- [ ] Manual keyboard testing
- [ ] Screen reader testing (NVDA, JAWS)
- [ ] WAVE tool

**Deliverables:**
- [ ] Relatório de A11y
- [ ] Fixes implementados

---

## 11. Fase 10: UX & Usability (1 semana)

### 11.1 User Feedback
- [ ] Toast notifications (sucesso, erro, info)
- [ ] Inline validation (real-time)
- [ ] Helpful error messages
- [ ] Empty states com orientações
- [ ] Loading indicators claros

### 11.2 Mobile UX
- [ ] Responsive design (mobile-first)
- [ ] Touch-friendly buttons (44px)
- [ ] Avoid horizontal scroll
- [ ] Appropriate input types (email keyboard, etc)
- [ ] Bottom sheet para modals (opcional)

### 11.3 Performance UX
- [ ] Code splitting
- [ ] Image optimization
- [ ] Lazy loading
- [ ] Skeleton loaders (vs spinners)

### 11.4 Microcopy
- [ ] Rever texto em botões
- [ ] Help text em inputs
- [ ] Mensagens de erro claras
- [ ] Confirmations antes de deletar

### 11.5 Onboarding
- [ ] Instruções claras na primeira vez
- [ ] Tooltips (opcional)
- [ ] Demo text pré-preenchido (admin demo)

---

## 12. Fase 11: Testing & QA (1 semana)

### 12.1 Frontend Testing
- [ ] Unit tests (Jest)
- [ ] Component tests (React Testing Library)
- [ ] E2E tests (Playwright/Cypress)
- [ ] Visual regression (Percy, opcional)
- [ ] Cobertura: 70%+

**Deliverables:**
- [ ] `frontend/__tests__/` com testes

### 12.2 Backend Testing
- [ ] Unit tests (pytest)
- [ ] Integration tests (API endpoints)
- [ ] Cobertura: 70%+
- [ ] Performance tests (carga)

**Deliverables:**
- [ ] `backend/tests/` com testes

### 12.3 Manual QA
- [ ] Checklist de funcionalidades
- [ ] Testar todos os browsers (Chrome, Firefox, Safari, Edge)
- [ ] Testar em diferentes resoluções
- [ ] Testar em dispositivos reais
- [ ] Testes de casos extremos

### 12.4 Security Testing
- [ ] SQL injection tests
- [ ] XSS prevention
- [ ] CSRF tokens (NextAuth cuida)
- [ ] Rate limiting
- [ ] Token expiration

### 12.5 Teste de Integração Fly.io
- [ ] Testar database connection (PostgreSQL Fly.io)
- [ ] Testar health check
- [ ] Testar logs (`fly logs`)
- [ ] Testar redeploy

---

## 13. Fase 12: Deployment Setup (2 semanas)

### 13.1 Backend - Fly.io (Estruturado)

#### Semana 1: Setup Inicial
- [ ] Criar app Web Service: `fly apps create study-ai-backend`
- [ ] Criar PostgreSQL: `fly postgres create --name study-ai-db`
- [ ] Anexar DB: `fly postgres attach study-ai-db --app study-ai-backend`
- [ ] Configurar `fly.toml`:
```toml
  app = "study-ai-backend"
  
  [build]
    builder = "heroku"
    
  [env]
    ENVIRONMENT = "production"
  
  [[services]]
    internal_port = 8000
    protocol = "tcp"
    
    [[services.ports]]
      port = 80
      handlers = ["http"]
      force_https = true
    
    [[services.ports]]
      port = 443
      handlers = ["tls", "http"]
  
  [checks]
    [checks.http]
      grace_period = "10s"
      interval = "30s"
      method = "GET"
      path = "/health"
      protocol = "http"
      timeout = "5s"
      success_threshold = 1
      failure_threshold = 2
```

- [ ] Configurar secrets Fly.io:
```bash
  fly secrets set -a study-ai-backend \
    DATABASE_URL="postgresql://..." \
    SECRET_KEY="$(openssl rand -hex 32)" \
    ANTHROPIC_API_KEY="sk-..." \
    ENVIRONMENT="production"
```

- [ ] Criar Dockerfile (opcional, para controle total):
```dockerfile
  FROM python:3.11-slim
  
  WORKDIR /app
  
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  COPY . .
  
  EXPOSE 8000
  
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] Teste deploy manual: `fly deploy`

#### Semana 2: Auto-Deploy & CI/CD
- [ ] Conectar GitHub:
```bash
  fly auth token
  # Copiar token
```
  
- [ ] Criar GitHub Secret: `FLY_API_TOKEN`

- [ ] Criar `.github/workflows/deploy.yml`:
```yaml
  name: Deploy to Fly.io
  
  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]
  
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with:
            python-version: '3.11'
        - run: |
            cd backend
            pip install -r requirements.txt
            pytest
    
    deploy:
      needs: test
      if: github.ref == 'refs/heads/main'
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: superfly/flyctl-actions/setup-flyctl@master
        - run: flyctl deploy --remote-only
          env:
            FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

- [ ] Testar auto-deploy com push

- [ ] Configurar migrations automáticas:
```bash
  # Em Procfile ou run script
  alembic upgrade head && uvicorn app.main:app
```

- [ ] Health check endpoint funcionando

**Deliverables:**
- [ ] `fly.toml` pronto
- [ ] `Dockerfile` (opcional)
- [ ] `.github/workflows/deploy.yml`
- [ ] Variáveis de ambiente em Fly.io

### 13.2 Frontend - Vercel
- [ ] Criar projeto Vercel (via web)
- [ ] Conectar GitHub repo
- [ ] Configurar environment variables:
```
  NEXT_PUBLIC_API_URL=https://study-ai-backend.fly.dev
  AUTH_GOOGLE_ID=...
  AUTH_GOOGLE_SECRET=...
  AUTH_SECRET=gerado-pelo-nextauth
```

- [ ] Testar build local: `npm run build`
- [ ] Testar deploy automático (push → Vercel)
- [ ] Verificar preview deployments

**Deliverables:**
- [ ] Vercel project configurado
- [ ] Environment variables configuradas

### 13.3 Monitoramento Fly.io
- [ ] Setup logs: `fly logs -a study-ai-backend`
- [ ] Setup alertas (email, opcional)
- [ ] Monitorar CPU/Memória: `fly status -a study-ai-backend`
- [ ] Documentar comandos úteis:
```bash
  fly logs -a study-ai-backend            # Ver logs
  fly status -a study-ai-backend          # Ver status
  fly secrets list -a study-ai-backend    # Listar secrets
  fly deploy -a study-ai-backend          # Redeploy manual
  fly ssh console -a study-ai-backend     # SSH into app
```

**Deliverables:**
- [ ] Documentação de monitoring
- [ ] Setup de logs estruturados

### 13.4 Backup & Disaster Recovery
- [ ] Configurar backup automático PostgreSQL (Fly.io faz por padrão)
- [ ] Documentar restore process:
```bash
  fly postgres connect -a study-ai-db
  # Usar ferramentas de backup
```

- [ ] Testar restore em desenvolvimento

**Deliverables:**
- [ ] Documentação de backup/restore

---

## 14. Fase 13: Documentação (1 semana)

### 14.1 Backend Documentation
- [ ] README com setup local
- [ ] README com setup Fly.io
- [ ] API docs (Swagger automático em `/docs`)
- [ ] Database schema diagram
- [ ] Environment variables guide
- [ ] Deployment guide Fly.io específico
- [ ] Troubleshooting Fly.io
- [ ] Contributing guidelines

**Deliverables:**
- [ ] `backend/README.md`
- [ ] `backend/API.md`
- [ ] `backend/DEPLOYMENT.md` (Fly.io focused)
- [ ] `backend/FLY_IO_GUIDE.md`
- [ ] `backend/TROUBLESHOOTING.md`

### 14.2 Frontend Documentation
- [ ] README com setup local
- [ ] README com setup Vercel
- [ ] Component library (Storybook, opcional)
- [ ] Acessibilidade guide
- [ ] Environment variables guide
- [ ] Deployment guide Vercel

**Deliverables:**
- [ ] `frontend/README.md`
- [ ] `frontend/DEPLOYMENT.md`

### 14.3 Root Documentation
- [ ] Project README (visão geral)
- [ ] Architecture diagram (com Fly.io)
- [ ] Stack overview
- [ ] Roadmap futuro
- [ ] Contributing guide
- [ ] Custo mensal estimado ($0!)

**Deliverables:**
- [ ] `README.md` raiz (destacar Fly.io free!)
- [ ] `ARCHITECTURE.md`
- [ ] `ROADMAP.md`
- [ ] `COSTS.md` (demonstrar que é $0)

### 14.4 User Documentation
- [ ] Como usar a app (guia)
- [ ] FAQ
- [ ] Troubleshooting

---

## 15. Fase 14: Polish Final (1 semana)

### 15.1 Bug Fixes
- [ ] Reproduzir e fixar bugs reportados
- [ ] Edge cases
- [ ] Performance issues

### 15.2 Performance Optimization
- [ ] Frontend bundle size
- [ ] Database queries (N+1)
- [ ] API response times em Fly.io
- [ ] Image optimization
- [ ] Caching strategy

### 15.3 Security Review
- [ ] Code review para segurança
- [ ] Dependency audit (npm, pip)
- [ ] API authentication/authorization review
- [ ] HTTPS enforced (Fly.io faz automaticamente)
- [ ] Secret management (secrets Fly.io)

### 15.4 Fly.io Optimization
- [ ] Verificar utilização de recursos
- [ ] Otimizar Dockerfile (layers, tamanho)
- [ ] Implementar health checks robustos
- [ ] Configurar graceful shutdown
- [ ] Setup de auto-scaling (se necessário)

### 15.5 UX Polish
- [ ] Micro-interactions
- [ ] Animations refinadas
- [ ] Loading states perfeitos
- [ ] Error messages finais
- [ ] Onboarding smooth

### 15.6 Final QA
- [ ] Full regression testing
- [ ] Cross-browser testing
- [ ] Mobile testing (real devices)
- [ ] A11y final check
- [ ] Performance audit (Lighthouse)
- [ ] Teste integrado (frontend + backend Fly.io)

---

## Checklist de Lançamento

- [ ] Todas as fases completadas
- [ ] Testes passando (100%)
- [ ] Code review completo
- [ ] Security audit realizado
- [ ] Documentação completa
- [ ] Fly.io configurado e testado
- [ ] Vercel configurado e testado
- [ ] CI/CD automático funcionando
- [ ] Backups PostgreSQL verificados
- [ ] Monitoring ativo em Fly.io
- [ ] Error tracking ativo
- [ ] Anúncio de lançamento
- [ ] Feedback dos primeiros usuários coletado

---

## Próximas Features (Pós-MVP)

- [ ] Export histórico (PDF, CSV)
- [ ] Compartilhamento de sessões (link público)
- [ ] Colaboração em tempo real
- [ ] Integração com Google Drive
- [ ] Voice input (Web Speech API)
- [ ] Análise por imagem (OCR)
- [ ] Planos pagos/freemium
- [ ] Chat com IA (follow-up questions)
- [ ] Gamificação (pontos, streaks)
- [ ] Mobile app nativa (React Native)
