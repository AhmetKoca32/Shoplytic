# Shoplytic — AI Shopping Assistant

An AI-powered personalized shopping assistant mobile application. Users describe a life change (e.g., "I'm starting university in Adana"), and the app generates an interactive mind map of needs, product recommendations with price comparisons, and legal support for consumer rights.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────────┐
│   Flutter App   │────▶│   FastAPI REST   │────▶│  LangGraph Workflow │
│  (shoplytic_ui) │◀────│ (shoplytic_back) │◀────│  + DeepSeek V4-Flash│
└─────────────────┘     └─────────────────┘     └──────────────────────┘
```

### Frontend (`shoplytic_ui/`)
- **Framework:** Flutter / Dart
- **State Management:** Provider + ChangeNotifier
- **Design:** Dark glassmorphism theme with Teal/Emerald/Amber palette
- **Fonts:** Montserrat (headings), Inter (body), JetBrains Mono (technical)
- **Navigation:** 5-tab floating glass navbar

### Backend (`shoplytic_backend/`)
- **Framework:** FastAPI (Python)
- **AI Engine:** LangGraph workflow with DeepSeek V4-Flash agents
- **Agents:**
  - `ContextAnalysisAgent` — Analyzes user's situation (location, climate, needs)
  - `MindMapAgent` — Generates structured shopping mind map (JSON)
  - `ProductAgent` — LLM-generated product recommendations + scoring function
  - `LegalAgent` — Turkish Consumer Law (Law No. 6502) analysis & petition generation
  - `CustomerAgent` — User segmentation & personalization

## User Flow

```
Splash (2.4s animation) → Onboard (5 pages) → Home
                                                    ├── Tab 1: Dashboard (prompt + examples)
                                                    ├── Tab 2: Mind Map (interactive visual map)
                                                    │   ├── Tap node → Product bottom sheet
                                                    │   └── Long press → AI chat panel
                                                    ├── Tab 3: Chat (general AI assistant)
                                                    ├── Tab 4: Consumer Rights (complaint/law/petition)
                                                    └── Tab 5: Profile (history/favorites/settings/help)
```

## Quick Start

### Backend
```bash
cd shoplytic_backend
cp .env.example .env
# Edit .env and set DEEPSEEK_API_KEY
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd shoplytic_ui
flutter pub get
flutter run
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/api/v1/system/status` | GET | Agent status |
| `/api/v1/ai/generate-mindmap` | POST | Generate mind map |
| `/api/v1/ai/chat` | POST | AI chat |
| `/api/v1/ecommerce/search` | GET | Product search |
| `/api/v1/ecommerce/compare/{name}` | GET | Price comparison |
| `/api/v1/legal/analyze` | POST | Legal complaint analysis |
| `/api/v1/legal/petition` | POST | Generate legal petition |

## Tech Stack

- **Frontend:** Flutter, Dart, Provider, Dio
- **Backend:** Python, FastAPI, LangGraph, LangChain
- **AI Model:** DeepSeek V4-Flash (OpenAI-compatible API)
- **Vector DB:** ChromaDB (for legal RAG)

## Project Structure

```
shoplytic_ui/lib/
├── app.dart                → MaterialApp + MultiProvider + routing
├── theme/                  → Color palette, text themes, font config
├── views/                  → All screens (splash, onboard, home, mind_map, chat, legal, profile)
├── widgets/                → Reusable (floating_glass_navbar, glass_card, mind_map_widget, etc.)
├── providers/              → State management
└── services/               → API service (Dio)

shoplytic_backend/
├── main.py                 → FastAPI entry point
├── api/routes/             → REST endpoints
├── agents/                 → AI agents (context, mindmap, product, legal, customer)
├── graph/                  → LangGraph workflow (state, nodes, workflow)
├── clients/                → LLM client (DeepSeek), e-commerce client
├── models/                 → Pydantic data models
└── core/                   → Config, dependencies
```

## Requirements

- Flutter SDK ^3.11.4
- Python ^3.11
- DeepSeek API key ([platform.deepseek.com](https://platform.deepseek.com))
