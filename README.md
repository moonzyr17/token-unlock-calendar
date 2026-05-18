# Token Unlock Calendar 🗓️

> Curated calendar of upcoming token unlocks for major crypto projects. Track supply pressure before it hits the market — across **24 tokens** and **53 unlock events**, totaling over **$4B** in pipeline value.

[![Live Demo](https://img.shields.io/badge/Live-Demo-2563EB?style=flat-square)](#demo)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

## Demo

🔗 **Coming soon** (deploy in progress)

![Token Unlock Calendar](https://img.shields.io/badge/Tokens-24-3B82F6?style=for-the-badge) ![Events](https://img.shields.io/badge/Events-53-059669?style=for-the-badge) ![Pipeline](https://img.shields.io/badge/Pipeline-%244B-F59E0B?style=for-the-badge)

## What it does

Token unlocks are scheduled supply emissions from team, investor, and ecosystem allocations. Large unlocks frequently precede price drops because they create immediate sell pressure. This calendar gives traders a curated, filterable view of upcoming events across major projects.

- **Landing page** — hero, stats, biggest upcoming unlocks, soonest unlocks, marketing CTA
- **Calendar app** — interactive month grid with USD-volume heatmap
- **Filtering** — by token, recipient (team / investors / ecosystem / foundation / mixed), and unlock type (monthly / cliff / linear)
- **Side panel detail** — click any day with events to see breakdown by token, USD value, % of circulating supply, and recipient

## Features

- 🗓️ Month-grid calendar with click-to-inspect day breakdown
- 🔥 Volume heatmap — heavier days shade brighter, $400M+ shows red
- 🔍 Triple filter: token / recipient / unlock type
- 📊 Monthly KPIs: event count, USD volume, biggest day, unique tokens
- 🪙 Featured "biggest unlocks" + "soonest unlocks" on landing
- 📱 Mobile-friendly responsive grid
- ♿ `prefers-reduced-motion` respected, focus states, semantic ARIA
- 🎨 Designed using the **UI Pro Max** design system: `Exaggerated Minimalism` style + Orbitron / Exo 2 typography + crypto-blue + green-accent palette

## Tracked tokens

ARB · APT · OP · SUI · AVAX · IMX · SEI · STRK · MANTA · JTO · JUP · APE · DYDX · WLD · PYTH · W (Wormhole) · ENA · TIA · BLUR · BIGTIME · ID · ZETA · ALT · DYM

## Stack

- **Backend** — Flask + SQLite (seeded from `data/seed.json`)
- **Frontend** — Tailwind (CDN) + vanilla JS + Chart.js-style data viz built from scratch
- **Deploy** — Railway / any Python host with `Procfile`
- **Data** — Hand-curated JSON from public vesting schedules

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/calendar` | GET | Calendar app |
| `/api/calendar?year=YYYY&month=MM` | GET | Events grouped by date for a month |
| `/api/unlocks?from=&to=&token=&recipient=&type=` | GET | Filtered list |
| `/api/tokens` | GET | All tracked tokens with summary stats |
| `/api/health` | GET | Health check |

### Sample `/api/calendar` response

```json
{
  "year": 2026,
  "month": 5,
  "total_events": 13,
  "by_date": {
    "2026-05-16": {
      "events": [
        {
          "id": "arb-2026-05-16",
          "token_symbol": "ARB",
          "token_name": "Arbitrum",
          "amount_tokens": 92.65,
          "amount_usd_estimate": 78.75,
          "pct_of_circulating": 1.92,
          "unlock_type": "monthly",
          "recipient": "Mixed"
        }
      ],
      "total_usd": 78.75,
      "count": 1
    }
  }
}
```

## Local setup

```bash
git clone https://github.com/moonzyr17/token-unlock-calendar.git
cd token-unlock-calendar

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
# → http://localhost:5000
```

The SQLite DB regenerates from `data/seed.json` on first run.

## Contributing data

Want to add or update an unlock event? Edit `data/seed.json` and open a PR.

Each entry follows this schema:

```json
{
  "id": "arb-2026-06-16",
  "token_symbol": "ARB",
  "token_name": "Arbitrum",
  "unlock_date": "2026-06-16",
  "amount_tokens": 92.65,
  "amount_usd_estimate": 78.5,
  "pct_of_circulating": 2.18,
  "unlock_type": "monthly",
  "chain": "Arbitrum",
  "recipient": "Mixed",
  "description": "Monthly linear unlock to team and investors per original Arbitrum DAO vesting schedule.",
  "logo_url": "https://assets.coingecko.com/coins/images/16547/large/photo_2023-03-29_21.25.45.jpeg",
  "coingecko_id": "arbitrum"
}
```

Delete `unlocks.db` after editing the seed to force a refresh.

## Caveats

- USD estimates use approximate prices at curation time and will drift.
- Unlock schedules can change via governance votes or contract migrations — verify against project docs before trading.
- This is a curated dataset, not a real-time on-chain scanner. Coverage will expand via contributions.

**Educational tool. Not financial advice.**

## License

MIT — see [LICENSE](LICENSE).
