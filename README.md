# Optic Shield AI

AI-powered video accessibility analyzer that detects seizure-triggering content in videos. Features a chat-first AI interface, synced video player with real-time waveform graphs, and YouTube URL analysis.

## Features

**Core Analysis**
- Flash frequency detection (general + red-specific) per WCAG 2.1 SC 2.3.1
- Luminance tracking + transition detection
- Scene cut frequency (histogram comparison)
- Motion intensity (pixel difference)
- Color cycling speed (dominant hue tracking)
- Spatial pattern detection (2D FFT)
- Overall weighted safety score with danger zone identification

**AI Features**
- General accessibility Q&A (works without video)
- Auto-generated safety report after analysis
- Per-graph AI explanations
- Contextual chat about analysis results
- FFmpeg fix command generation
- BYOK — bring your own Anthropic API key

**Interactive Features**
- Synced video player ↔ graph cursor ↔ timeline strip
- Click any graph → video seeks to that timestamp
- Danger zone overlay on player (border pulse)
- YouTube URL paste → auto-download + analyze
- Drag & drop video upload
- Real-time WebSocket progress with stage indicators
- Export report as PDF / JSON

**UX Features**
- Chat-first interface (AI useful from second one)
- 3D animated AI orb (idle, thinking, analyzing, alert states) via Three.js
- Analysis panel slides in/out with spring animation
- Collapsible panel with persistent pill bar
- Glassmorphism cards, gradient accents
- Dark sidebar with icon navigation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Vue 3)                     │
│  ┌──────────┐  ┌───────────┐  ┌────────────────────┐   │
│  │ Chat UI  │  │  Analysis  │  │  Synced Player +   │   │
│  │ + AI Orb │  │   Panel    │  │  Waveform Graphs   │   │
│  └────┬─────┘  └─────┬─────┘  └────────┬───────────┘   │
│       │  REST/WS     │  REST           │  playerStore   │
└───────┼──────────────┼────────────────┼─────────────────┘
        │              │                │
┌───────┼──────────────┼────────────────┼─────────────────┐
│       ▼              ▼                ▼    Backend       │
│  ┌─────────┐  ┌───────────┐  ┌─────────────────┐       │
│  │  Chat   │  │  Analysis  │  │  Video Serving  │       │
│  │ Router  │  │  Router    │  │    Router       │       │
│  └────┬────┘  └─────┬─────┘  └─────────────────┘       │
│       │              │                                   │
│  ┌────▼────┐  ┌─────▼──────────────────────────┐       │
│  │   AI    │  │     Analysis Service            │       │
│  │ Service │  │  ┌────────┐ ┌────────┐ ┌─────┐ │       │
│  │(Claude) │  │  │ Flash  │ │Luminanc│ │Motion│ │       │
│  └─────────┘  │  │Detector│ │Analyzer│ │ ... │ │       │
│               │  └────────┘ └────────┘ └─────┘ │       │
│               │  ProcessPoolExecutor (parallel) │       │
│               └─────────────────────────────────┘       │
│                          │                               │
│               ┌──────────▼──────────┐                   │
│               │   Report Service    │                   │
│               │ (scoring + zones)   │                   │
│               └─────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + TypeScript + Tailwind CSS v4 |
| Charts | Chart.js + vue-chartjs |
| 3D Orb | Three.js |
| Icons | Lucide Vue |
| State | Pinia |
| Backend | Python 3.11+ + FastAPI |
| Video | OpenCV + NumPy + SciPy + FFmpeg |
| YouTube | yt-dlp |
| AI | Anthropic Claude API (BYOK) |
| WebSocket | FastAPI native |
| Parallelism | ProcessPoolExecutor |

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- FFmpeg (must be on PATH)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Backend

```bash
cd server
uv venv .venv
uv pip install -r requirements.txt
.venv/Scripts/activate   # Windows
# source .venv/bin/activate  # macOS/Linux
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000. API docs at http://localhost:8000/docs.

### Frontend

```bash
cd client
npm install
npm run dev
```

Frontend runs at http://localhost:5173.

### Docker

```bash
docker-compose up --build
```

Frontend at http://localhost:3000, backend at http://localhost:8000.

## Usage

1. Open http://localhost:5173
2. Chat with the AI about video accessibility (no API key needed for general questions)
3. Click the API key icon to enter your Anthropic API key (enables AI reports)
4. Upload a video file or paste a YouTube URL
5. Watch real-time analysis progress via WebSocket
6. Explore the analysis panel: safety score, metrics, waveform graphs
7. Play the video and watch the cursor sync across all graphs
8. Click any graph to seek the video to that timestamp
9. Ask the AI follow-up questions about the analysis

## Project Structure

```
optic-shield/
├── client/                  # Vue 3 frontend
│   └── src/
│       ├── components/      # atoms → molecules → organisms → views
│       ├── composables/     # useAnalysis, useChat, useGraphSync, etc.
│       ├── services/        # API + WebSocket communication
│       ├── stores/          # Pinia state management
│       ├── types/           # TypeScript interfaces
│       ├── utils/           # constants, formatters, validators
│       └── viewmodels/      # data transformation (pure functions)
├── server/                  # Python FastAPI backend
│   └── app/
│       ├── analyzers/       # 8 detection modules (flash, motion, etc.)
│       ├── models/          # Pydantic request/response models
│       ├── prompts/         # AI prompt templates
│       ├── routers/         # API endpoints
│       ├── services/        # business logic orchestration
│       ├── utils/           # WCAG thresholds, color math, cleanup
│       └── workers/         # multiprocessing frame analysis
├── shared/                  # TypeScript type mirrors
└── docker-compose.yml
```

## WCAG Thresholds

| Metric | Threshold | Source |
|--------|-----------|--------|
| General flash | ≤ 3 flashes/sec | WCAG 2.1 SC 2.3.1 |
| Flash luminance change | > 20 cd/m² | W3C |
| Red flash | Saturated red with luminance shift | WCAG 2.1 SC 2.3.1 |
| Flash area | > 25% of screen area | W3C |
| Spatial pattern | > 8 cycles across any direction | Harding test standard |

## License

MIT
