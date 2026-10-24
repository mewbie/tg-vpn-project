#!/usr/bin/env python3
"""Build the DM shortlist. Restricted-geo channels, priced from a CPM band."""
import json, glob, datetime

TARGET_LANGS = {"fa", "ru", "tr", "uz", "kk", "uk", "ar", "he", "ur", "az"}
CHEAP = 3.0        # EUR per 1k views, restricted/cheap geos
PREMIUM = 8.0      # EUR per 1k views, tier-1
PREMIUM_LANGS = {"en", "de", "fr", "nl", "sv", "it", "es", "pt", "pl", "zh", "ko", "ja"}

MIN_V, MAX_V = 1200, 10000
MIN_RATE     = 0.10
MAX_COST     = 25.0
STALE_DAYS   = 21

def load(path):
    d = json.load(open(path))
    if isinstance(d, list):
        return d
    if isinstance(d, dict) and not d.get("error"):
        for k in ("data", "channels", "items", "results"):
            if isinstance(d.get(k), list):
                return d[k]
    return []

rows = []
for f in sorted(glob.glob("data/raw/ch-*.json")):
    rows += load(f)

now = datetime.datetime.now(datetime.timezone.utc)
seen, out = set(), []
for r in rows:
    m, v = r.get("members"), r.get("avgViews")
    lang = r.get("lang") or ""
    if not (m and v) or lang not in TARGET_LANGS:
        continue
    rate = v / m
    cpm  = PREMIUM if lang in PREMIUM_LANGS else CHEAP
    cost = (v / 1000) * cpm
    try:
        dt = datetime.datetime.fromisoformat(str(r.get("lastSnapshotAt","")).replace("Z","+00:00"))
        stale = (now - dt).days > STALE_DAYS
    except Exception:
        stale = False
    if not (MIN_V <= v <= MAX_V): continue
    if rate < MIN_RATE:           continue
    if cost > MAX_COST:           continue
    if stale:                     continue
    key = (r.get("title") or "")[:12].lower()
    if key in seen:               continue
    seen.add(key)
    out.append((cost, rate, r))

from collections import Counter
print("lang mix:", dict(Counter(r.get("lang") for _, _, r in out)))
out.sort(key=lambda x: x[0])
print(f"\n{len(out)} candidates, cheapest first\n")
print(f'{"~EUR":>6} {"rate":>5} {"members":>8} {"views":>7} {"lang":>4}  title')
for cost, rate, r in out[:40]:
    print(f'{cost:>6.1f} {rate:>5.2f} {r["members"]:>8,} {r["avgViews"]:>7,} '
          f'{r.get("lang"):>4}  {r["title"][:34]:<34} @{r.get("username")}')
