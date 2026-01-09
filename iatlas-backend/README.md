# IAtlas Backend

API REST para análise de textos e PDFs com IA.

## 🚀 Tecnologias

- FastAPI
- PostgreSQL
- LangChain + Gemini
- JWT Authentication
- Black (formatação de código)
- Ruff (linter)

## 📦 Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento (Black, Ruff)
pip install -e ".[dev]"
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
# Desenvolvimento
uvicorn main:app --reload

# Ou executar diretamente
python main.py
```

API disponível em: `http://localhost:8000`

## 📚 Documentação

- Swagger UI: `http://localhost:8000/docs`
- Veja [API.md](./API.md) para documentação completa

## 🧪 Testes

```bash
pytest
```

## 🎨 Formatação de Código

Este projeto usa [Black](https://black.readthedocs.io/) para formatação automática de código Python.

```bash
# Formatar código com Black
black .

# Verificar formatação sem aplicar mudanças
black --check .
```

A configuração do Black está em `pyproject.toml`.
