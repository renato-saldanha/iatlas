# IAtlas Frontend

Interface web do IAtlas - Assistente de Estudos com IA.

## 🚀 Tecnologias

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- NextAuth.js
- Prettier (formatação de código)
- ESLint (linter)

## 📦 Instalação

```bash
# Instalar dependências
npm install
```

## ⚙️ Configuração

Crie um arquivo `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
AUTH_SECRET=seu-secret-key-aqui
AUTH_GOOGLE_ID=seu-google-client-id
AUTH_GOOGLE_SECRET=seu-google-client-secret
```

## ▶️ Executar

```bash
# Desenvolvimento
npm run dev

# Produção
npm run build
npm start
```

Aplicação disponível em: `http://localhost:3000`

## 🧪 Testes

```bash
npm run lint
```

## 🎨 Formatação de Código

Este projeto usa [Prettier](https://prettier.io/) para formatação automática de código.

```bash
# Formatar código com Prettier
npm run format

# Verificar formatação sem aplicar mudanças
npm run format:check
```

A configuração do Prettier está em `.prettierrc`.
