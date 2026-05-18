"""Token Unlock Calendar — track upcoming token unlocks across major crypto projects.

In-memory data store loaded from data/seed.json. Works on:
- Local dev (python app.py)
- Railway / Render / Fly (gunicorn)
- Vercel (serverless via api/index.py wrapper)
"""
from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).parent
SEED_PATH = BASE_DIR / "data" / "seed.json"

app = Flask(__name__)


# ---------------------------------------------------------------------------
# In-memory store (loaded once at boot)
# ---------------------------------------------------------------------------
def load_unlocks() -> list[dict[str, Any]]:
    """Load and normalize the unlock dataset."""
    if not SEED_PATH.exists():
        return []
    rows = json.loads(SEED_PATH.read_text())
    rows.sort(key=lambda r: (r["unlock_date"], -(r.get("amount_usd_estimate") or 0)))
    return rows


UNLOCKS: list[dict[str, Any]] = load_unlocks()


def filter_rows(
    rows: list[dict[str, Any]],
    *,
    date_from: str | None = None,
    date_to: str | None = None,
    token: str | None = None,
    recipient: str | None = None,
    unlock_type: str | None = None,
) -> list[dict[str, Any]]:
    out = rows
    if date_from:
        out = [r for r in out if r["unlock_date"] >= date_from]
    if date_to:
        out = [r for r in out if r["unlock_date"] <= date_to]
    if token:
        token = token.upper()
        out = [r for r in out if r["token_symbol"] == token]
    if recipient:
        out = [r for r in out if r["recipient"] == recipient]
    if unlock_type:
        out = [r for r in out if r["unlock_type"] == unlock_type]
    return out


# ---------------------------------------------------------------------------
# Routes — pages
# ---------------------------------------------------------------------------
@app.route("/")
def landing() -> str:
    today = date.today().isoformat()
    next_30 = (date.today() + timedelta(days=30)).isoformat()

    upcoming_all = filter_rows(UNLOCKS, date_from=today)
    next_30_rows = filter_rows(UNLOCKS, date_from=today, date_to=next_30)

    biggest = sorted(upcoming_all, key=lambda r: -(r.get("amount_usd_estimate") or 0))[:6]
    upcoming = upcoming_all[:6]

    stats = {
        "total_events": len(upcoming_all),
        "total_tokens": len({r["token_symbol"] for r in upcoming_all}),
        "total_usd": sum(r.get("amount_usd_estimate") or 0 for r in upcoming_all),
        "next_30_usd": sum(r.get("amount_usd_estimate") or 0 for r in next_30_rows),
        "next_30_events": len(next_30_rows),
    }

    return render_template(
        "landing.html",
        stats=stats,
        biggest=biggest,
        upcoming=upcoming,
    )


@app.route("/calendar")
def calendar_page() -> str:
    return render_template("calendar.html")


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------
@app.route("/api/unlocks")
def api_unlocks() -> Any:
    rows = filter_rows(
        UNLOCKS,
        date_from=request.args.get("from"),
        date_to=request.args.get("to"),
        token=request.args.get("token"),
        recipient=request.args.get("recipient"),
        unlock_type=request.args.get("type"),
    )
    return jsonify({"count": len(rows), "rows": rows})


@app.route("/api/calendar")
def api_calendar() -> Any:
    year = int(request.args.get("year") or date.today().year)
    month = int(request.args.get("month") or date.today().month)
    start = date(year, month, 1).isoformat()
    if month == 12:
        end = date(year + 1, 1, 1).isoformat()
    else:
        end = date(year, month + 1, 1).isoformat()

    rows = [r for r in UNLOCKS if start <= r["unlock_date"] < end]

    by_date: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"events": [], "total_usd": 0.0, "count": 0}
    )
    for r in rows:
        d = r["unlock_date"]
        by_date[d]["events"].append(r)
        by_date[d]["total_usd"] += r.get("amount_usd_estimate") or 0
        by_date[d]["count"] += 1

    return jsonify({
        "year": year,
        "month": month,
        "by_date": dict(by_date),
        "total_events": len(rows),
    })


@app.route("/api/tokens")
def api_tokens() -> Any:
    today = date.today().isoformat()
    upcoming = [r for r in UNLOCKS if r["unlock_date"] >= today]

    grouped: dict[str, dict[str, Any]] = {}
    for r in upcoming:
        sym = r["token_symbol"]
        if sym not in grouped:
            grouped[sym] = {
                "token_symbol": sym,
                "token_name": r["token_name"],
                "chain": r.get("chain"),
                "logo_url": r.get("logo_url") or "",
                "coingecko_id": r.get("coingecko_id") or "",
                "events": 0,
                "total_usd": 0.0,
                "next_unlock": r["unlock_date"],
            }
        g = grouped[sym]
        g["events"] += 1
        g["total_usd"] += r.get("amount_usd_estimate") or 0
        if r["unlock_date"] < g["next_unlock"]:
            g["next_unlock"] = r["unlock_date"]

    tokens = sorted(grouped.values(), key=lambda g: -g["total_usd"])
    return jsonify({"count": len(tokens), "tokens": tokens})


@app.route("/api/health")
def api_health() -> Any:
    return jsonify({
        "status": "ok",
        "loaded": len(UNLOCKS),
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
