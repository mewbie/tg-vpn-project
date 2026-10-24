#!/usr/bin/env python3
"""
Fetch channels from tgadsspy. One careful pass.

Rules learned the hard way:
  - no 'data' key -> error body, not an empty page -> abort
  - any error field -> abort the run, wait 3h. Every poke resets the fade.
  - follow meta.nextOffset, never compute offsets yourself
  - jittered delay, one term at a time
Env: LIMIT, START_OFFSET, MAX_PAGES
"""
import json, os, random, sys, time
import urllib.error, urllib.parse, urllib.request

KEY        = os.environ.get("TGADSSPY_KEY", "")
BASE       = "https://tgadsspy.com/api/v1/channels"
LIMIT      = int(os.environ.get("LIMIT", "100"))
START      = int(os.environ.get("START_OFFSET", "0"))
MAX_PAGES  = int(os.environ.get("MAX_PAGES", "60"))
DELAY      = (3.0, 5.5)
OUTDIR     = "data/raw"

def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Api-Key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except Exception:
            return {"error": f"http_{e.code}"}

def main(terms):
    if not KEY:
        sys.exit("TGADSSPY_KEY not set")
    os.makedirs(OUTDIR, exist_ok=True)
    got = 0
    for term in terms:
        off, pages = START, 0
        while pages < MAX_PAGES:
            d = get({"q": term, "limit": LIMIT, "offset": off})
            if d.get("error"):
                print(f"\n!! {d['error']} q={term} offset={off} "
                      f"retryAfterMs={d.get('retryAfterMs')}")
                print(f"!! ABORT. Do not retry for 3h. {got} records this run.")
                return
            batch = d.get("data")
            if batch is None:
                print(f"?? no 'data' key at offset {off}: {list(d)[:5]} -> ABORT")
                return
            meta = d.get("meta", {})
            if meta.get("offsetClamped") or meta.get("limitClamped"):
                print(f"   clamped: offset={meta.get('offsetClamped')} "
                      f"limit={meta.get('limitClamped')} maxOffset={meta.get('maxOffset')}")
            if not batch:
                print(f"{term}: empty at offset {off}, done")
                break
            json.dump(d, open(f"{OUTDIR}/ch-{term}-{off}.json", "w"))
            got += len(batch); pages += 1
            print(f"{term} offset={off:>5} +{len(batch):>3} running={got} "
                  f"reachable={meta.get('totalReachable')}")
            nxt = meta.get("nextOffset")
            if not meta.get("hasMore") or nxt is None:
                print(f"{term}: no more (maxOffset={meta.get('maxOffset')})")
                break
            off = nxt
            time.sleep(random.uniform(*DELAY))

if __name__ == "__main__":
    main(sys.argv[1:] or ["crypto"])
