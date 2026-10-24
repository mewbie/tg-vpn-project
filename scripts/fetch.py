#!/usr/bin/env python3
"""
Daily snapshot of the tgadsspy public API.

Writes JSON to data/raw/YYYY-MM-DD/. Run by hand or by the GitHub workflow.
Uses only the standard library, so nothing needs installing.
"""
import json
import os
import sys
import datetime
import urllib.request

BASE = "https://tgadsspy.com/api/v1"

# Each entry becomes one file in the snapshot folder.
ENDPOINTS = {
    "stats":  "/stats",    # global counts, niche + geo rankings
    "geos":   "/geos",     # advertiser-intent per country
    "niches": "/niches",   # niche list with counts
}


def fetch(path):
    """Call one endpoint and return parsed JSON."""
    req = urllib.request.Request(
        BASE + path,
        headers={"User-Agent": "tg-vpn-project/1.0"},  # be polite
    )
    key = os.environ.get("TGADSSPY_KEY", "").strip()
    if key:
        req.add_header("X-Api-Key", key)              # optional; works without

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    day = datetime.date.today().isoformat()           # e.g. 2026-10-24
    out_dir = os.path.join("data", "raw", day)
    os.makedirs(out_dir, exist_ok=True)

    ok = failed = 0

    for name, path in ENDPOINTS.items():
        try:
            data = fetch(path)
            with open(os.path.join(out_dir, f"{name}.json"), "w") as fh:
                json.dump(data, fh, indent=2)
            print(f"ok    {name}")
            ok += 1
        except Exception as exc:
            # One bad endpoint shouldn't kill the whole run.
            print(f"fail  {name}: {exc}", file=sys.stderr)
            failed += 1

    print(f"{ok} ok, {failed} failed -> {out_dir}")

    # Exit non-zero only if everything failed, so GitHub shows a red X.
    if ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()