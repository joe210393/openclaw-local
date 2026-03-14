#!/usr/bin/env python3
import json
import os
import subprocess
import sys

def run_cmd(cmd, env=None):
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.returncode, result.stdout, result.stderr

def parse_items(raw: str):
    raw = raw.strip()
    if not raw:
        return []

    # 舊格式：JSON array
    if raw.startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("input must be a json array")
        return data

    # 新格式：每行一筆
    # from|to|summary|location|description
    items = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            raise ValueError(f"line {line_no}: need at least from|to|summary")
        while len(parts) < 5:
            parts.append("")
        start, end, summary, location, description = parts[:5]
        items.append({
            "summary": summary,
            "from": start,
            "to": end,
            "location": location,
            "description": description,
        })
    return items

def main():
    if len(sys.argv) != 2:
        print("Usage: batch_add_calendar.py '<json-array-or-lines>'")
        sys.exit(1)

    try:
        items = parse_items(sys.argv[1])
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": f"invalid input: {e}"
        }, ensure_ascii=False))
        sys.exit(1)

    home = "/Users/hung-weichen/openclaw-local/.home"
    env = os.environ.copy()
    env["HOME"] = home
    env["XDG_CONFIG_HOME"] = "/Users/hung-weichen/openclaw-local/.xdg-config"
    env["XDG_CACHE_HOME"] = "/Users/hung-weichen/openclaw-local/.xdg-cache"
    env["XDG_STATE_HOME"] = "/Users/hung-weichen/openclaw-local/.local-state"
    env["GOG_ACCOUNT"] = "joe210393@gmail.com"

    calendar_id = "joe210393@gmail.com"
    results = []

    for idx, item in enumerate(items, start=1):
        summary = str(item.get("summary", "")).strip()
        start = str(item.get("from", "")).strip()
        end = str(item.get("to", "")).strip()
        location = str(item.get("location", "")).strip()
        description = str(item.get("description", "")).strip()

        if not summary or not start or not end:
            results.append({
                "index": idx,
                "summary": summary,
                "ok": False,
                "error": "missing summary/from/to"
            })
            continue

        if not location:
            location = "宜蘭"

        cmd = [
            "gog", "calendar", "create", calendar_id,
            "--summary", summary,
            "--from", start,
            "--to", end,
            "--location", location,
            "--json",
            "--no-input"
        ]

        if description:
            cmd.extend(["--description", description])

        code, out, err = run_cmd(cmd, env=env)

        if code == 0:
            try:
                parsed = json.loads(out)
                event = parsed.get("event", {})
                results.append({
                    "index": idx,
                    "summary": event.get("summary", summary),
                    "ok": True,
                    "eventId": event.get("id"),
                    "from": event.get("start", {}).get("dateTime", start),
                    "to": event.get("end", {}).get("dateTime", end),
                    "location": event.get("location", location)
                })
            except Exception:
                results.append({
                    "index": idx,
                    "summary": summary,
                    "ok": True,
                    "raw": out.strip()
                })
        else:
            results.append({
                "index": idx,
                "summary": summary,
                "ok": False,
                "error": (err.strip() or out.strip() or f"exit code {code}")
            })

    print(json.dumps({
        "ok": True,
        "count": len(results),
        "results": results
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
