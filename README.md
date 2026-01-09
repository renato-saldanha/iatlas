# IAtlas - Seu auxiliar em qualquer estudo

Assistente de estudos com IA para análise de textos e PDFs.

## 📁 Estrutura do Projeto

```
projeto/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── iatlas-frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── ...
│   ├── package.json
│   ├── next.config.ts
│   └── README.md
├── iatlas-backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── fly.toml
│   └── README.md
├── README.md
├── ARCHITECTURE.md
└── ROADMAP.md
```

## 🚀 Início Rápido

### Backend

```bash
cd iatlas-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install -e ".[dev]"  # Instalar Black e Ruff
uvicorn app.main:app --reload
```

### Frontend

```bash
cd iatlas-frontend
npm install
npm run dev
```

## 🎨 Formatação de Código

- **Backend**: Usa [Black](https://black.readthedocs.io/) para formatação Python
  - `black .` - Formatar código
  - `black --check .` - Verificar formatação

- **Frontend**: Usa [Prettier](https://prettier.io/) para formatação JavaScript/TypeScript
  - `npm run format` - Formatar código
  - `npm run format:check` - Verificar formatação

## 📚 Documentação

- [Backend README](./iatlas-backend/README.md)
- [Frontend README](./iatlas-frontend/README.md)
- [Arquitetura](./ARCHITECTURE.md)
- [Roadmap](./ROADMAP.md)