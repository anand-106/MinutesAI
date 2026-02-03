<p align="center">
  <img src="https://img.shields.io/badge/MinutesAI-Meeting%20Intelligence-6c47ff?style=for-the-badge&logo=googlemeet&logoColor=white" alt="MinutesAI" />
</p>

<h1 align="center">MinutesAI</h1>

<p align="center">
  <strong>AI-powered meeting assistant that joins, records, transcribes, and summarizes your calls.</strong>
</p>

<p align="center">
  Paste a meeting link. MinutesAI joins the call, captures audio, transcribes with AI, and stores everything in one place.
</p>

---

## Features

- **One-click join** — Paste any meeting link and let MinutesAI join as a participant
- **Automatic recording** — Captures meeting audio with browser automation
- **AI transcription** — Powered by Deepgram and Groq for accurate, fast transcripts
- **Summaries** — Get AI-generated summaries of your meetings
- **Secure storage** — Recordings and transcripts stored in S3
- **Dashboard** — View and manage all your meetings in one place
- **Authentication** — Built-in auth with Clerk

---

## Tech Stack

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| **Frontend** | Next.js, React, TypeScript, Clerk   |
| **Backend**  | FastAPI (Python)                    |
| **Worker**   | Python, arq, Playwright, Deepgram, Groq |
| **Data**     | PostgreSQL, Redis                   |
| **Storage**  | AWS S3                              |
| **Monorepo** | Turborepo, pnpm                     |

---

## 📁 Project Structure

```
MinutesAI/
├── apps/
│   ├── frontend/        # Next.js web app (dashboard, meetings, transcripts)
│   ├── backend/         # FastAPI API (auth, meetings)
│   └── meeting-worker/  # Background worker (join, record, transcribe)
├── packages/
│   ├── ui/              # Shared UI components
│   ├── eslint-config/   # Shared ESLint config
│   └── typescript-config/
├── infra/
│   └── docker-compose.yml   # PostgreSQL & Redis
├── turbo.json
└── pnpm-workspace.yaml
```

---

## Getting Started

### Prerequisites

- **Node.js** ≥ 18  
- **pnpm** 9.x  
- **Python** 3.x (for backend & worker)  
- **Docker** & **Docker Compose** (for Postgres & Redis)  
- **Clerk** account (frontend auth)  
- **Deepgram** / **Groq** API keys (transcription)  
- **AWS S3** bucket (storage)

### 1. Clone and install

```bash
git clone https://github.com/your-org/MinutesAI.git
cd MinutesAI
pnpm install
```

### 2. Start infrastructure

```bash
cd infra
docker-compose up -d
```

### 3. Configure environment

Create `.env` files in each app using the existing examples (e.g. `.env.example`). Set:

- Database URL (Postgres)
- Redis URL
- Clerk keys (frontend/backend)
- Deepgram / Groq API keys
- S3 credentials and bucket name

### 4. Run the stack

From the repo root:

```bash
pnpm dev          # Runs frontend + backend (Turbo)
# In separate terminals:
# Start meeting-worker (see apps/meeting-worker/README.md)
```

### 5. Open the app

- Frontend: [http://localhost:3000](http://localhost:3000)  
- Backend API: [http://localhost:8000](http://localhost:8000) (or your configured port)

---

## Scripts

| Command        | Description                |
| -------------- | -------------------------- |
| `pnpm dev`     | Start frontend & backend    |
| `pnpm build`   | Build all apps             |
| `pnpm lint`    | Lint all packages          |
| `pnpm format`  | Format code with Prettier  |
| `pnpm check-types` | Type-check all apps   |

---

## License

MIT
