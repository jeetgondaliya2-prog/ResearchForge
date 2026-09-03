"""
Simple JSON-file-based research history storage.
No PostgreSQL required for basic history functionality.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


# ==========================================
# HISTORY FILE PATH
# ==========================================

HISTORY_FILE = Path(__file__).resolve().parents[2] / "data" / "research_history.json"


def _load_history() -> List[Dict[str, Any]]:
    """Load research history from JSON file."""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        print(f"[HISTORY] Could not load history: {e}")
    return []


def _save_history(history: List[Dict[str, Any]]) -> None:
    """Save research history to JSON file."""
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[HISTORY] Could not save history: {e}")


def save_research_result(
    user_query: str,
    final_report: str,
    analysis: str = "",
    feasibility: str = "",
    critique: str = "",
) -> Dict[str, Any]:
    """
    Save a research result to history.
    Returns the saved entry with its ID.
    """
    history = _load_history()

    entry_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(history)}"

    entry = {
        "id": entry_id,
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "final_report": final_report,
        "analysis": analysis,
        "feasibility": feasibility,
        "critique": critique,
        "report_length": len(final_report),
    }

    # Keep only the last 50 entries
    history.append(entry)
    if len(history) > 50:
        history = history[-50:]

    _save_history(history)

    print(f"[HISTORY] Saved research: {entry_id}")

    return entry


def get_history(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get the most recent research history entries.
    Returns entries sorted newest-first, without the full report text.
    """
    history = _load_history()

    # Return newest first, with truncated content for list view
    result = []
    for entry in reversed(history[-limit:]):
        result.append({
            "id": entry.get("id", ""),
            "timestamp": entry.get("timestamp", ""),
            "user_query": entry.get("user_query", ""),
            "report_preview": (entry.get("final_report", "")[:200] + "...")
            if len(entry.get("final_report", "")) > 200
            else entry.get("final_report", ""),
            "report_length": entry.get("report_length", 0),
        })

    return result


def get_research_by_id(entry_id: str) -> Dict[str, Any]:
    """Get a specific research entry by its ID."""
    history = _load_history()
    for entry in history:
        if entry.get("id") == entry_id:
            return entry
    return {}


def delete_research_by_id(entry_id: str) -> bool:
    """Delete a specific research entry by its ID."""
    history = _load_history()
    new_history = [e for e in history if e.get("id") != entry_id]
    if len(new_history) < len(history):
        _save_history(new_history)
        print(f"[HISTORY] Deleted research: {entry_id}")
        return True
    return False


def clear_history() -> None:
    """Clear all research history."""
    _save_history([])
    print("[HISTORY] History cleared.")
