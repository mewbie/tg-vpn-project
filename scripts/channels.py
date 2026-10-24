#!/usr/bin/env python3
"""Offline selection from data/raw/. Makes ZERO API calls."""
import json, glob, datetime

MIN_V, MAX_V = 1500, 12000
MIN_RATE     = 0.10
MAX_COST     = 30.0
STALE_DAYS   = 21

def load(path):
    """Return (records, meta). Handles bare arrays and dict wrappers."""
    d = json.load(open(path))
    if isinstance(d, list):
        return d, {}
    if isinstance(d, dict):
        if d.get("error"):
            return [], {}
        for k in ("data", "channels", "items", "results"):
            if isinstance(d.get(k), list):
                return d[k], d.get("meta", {})
    return [], {}

files = sorted(glob.glob("data/raw/ch-*.json"))
if not files:
    raise SystemExit("no files matched data/raw/ch-*.json - wrong cwd?")

print(f"debug: {files[0]} -> {type(json.load(open(files[0]))).__name__}")
print(f"debug: load() extracted {len(load(files[0])[0])} records from it")

rows, bad, meta = [], 0, {}
for f in files:
    recs, m = load(f)
    if not recs:
        bad += 1
        continue
    rows += recs
    if m and not meta:
        meta = m

print(f"\n{len(rows)} records loaded, {bad} error files skipped")
if meta:
    print("API meta:", {k: meta.get(k) for k in ("total", "totalReachable", "maxOffset",
          "reachable", "hasMore", "offsetClamped", "plan")})
if not rows:
    raise SystemExit("still zero - paste the debug lines above")

priced = [r for r in rows if r.get("estimatedCpm")]
print(f"priced records: {len(priced)}/{len(rows)}")
print(f"langs present: {sorted({r.get('lang') for r in rows if r.get('lang')})}\n")

now = datetime.datetime.now(datetime.timezone.utc)
seen, out = set(), []
for r in rows:
    m, v = r.get("members"), r.get("avgViews")
    cpm  = r.get("estimatedCpm")
    if not (m and v):
        continue
    rate = v / m
    cost = (v / 1000) * cpm if cpm else None
    try:
        dt = datetime.datetime.fromisoformat(str(r.get("lastSnapshotAt","")).replace("Z","+00:00"))
        stale = (now - dt).days > STALE_DAYS
    except Exception:
        stale = False
    if not (MIN_V <= v <= MAX_V): continue
    if rate < MIN_RATE:           continue
    if cost is not None and cost > MAX_COST: continue
    if stale:                     continue
    key = (r.get("title") or "")[:12].lower()
    if key in seen:               continue
    seen.add(key)
    out.append((rate, cost, r))

out.sort(key=lambda x: -x[0])
print(f"{len(out)} candidates\n")
print(f'{"rate":>5} {"members":>8} {"views":>7} {"~cost":>6} {"lang":>4} {"ads":>4}  title')
for rate, cost, r in out[:40]:
    cs = f"{cost:.1f}" if cost is not None else "  n/a"
    print(f'{rate:>5.2f} {r["members"]:>8,} {r["avgViews"]:>7,} {cs:>6} '
          f'{str(r.get("lang")):>4} {str(r.get("isSponsoredEligible"))[:1]:>4}  '
          f'{r["title"][:32]:<32} @{r.get("username")}')
