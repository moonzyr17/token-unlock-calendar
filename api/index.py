"""Vercel serverless entrypoint — re-exports the Flask app as `app`."""
import sys
from pathlib import Path

# Add project root to sys.path so `from app import app` works
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402,F401
