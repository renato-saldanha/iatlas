# IAtlas Backend

API REST para análise de textos e PDFs com IA.

## 🚀 Tecnologias

- FastAPI
- PostgreSQL
- LangChain + Gemini
- JWT Authentication

## 📦 Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/iatlas_db
SECRET_KEY=seu-secret-key-aqui
ANTHROPIC_API_KEY=sk-...
ENVIRONMENT=development
```

## ▶️ Executar

```bash
uvicorn app.main:app --reload
```

API disponível em: `http://localhost:8000`

## 📚 Documentação

- Swagger UI: `http://localhost:8000/docs`
- Veja [API.md](./API.md) para documentação completa

## 🧪 Testes

```bash
pytest
```
