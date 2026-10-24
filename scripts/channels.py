#!/usr/bin/env python3
"""Fetch and score crypto/proxy Telegram channels for the placement shortlist."""

import csv
import json
import math
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://tgadsspy.com/api/v1"
QUERIES = ("crypto", "proxy")
MIN_MEMBERS = 1000
PAGE_SIZE = 20
TIMEOUT = 30
MAX_RETRIES = 4
MAX_AUTOMATIC_RETRY_DELAY = 30
MAX_SANE_CPM_EUR = 20.0
ESTIMATED_CPM_EUR = 2.0
MAX_ESTIMATED_COST_EUR = 60.0
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "channels.csv"
FIELDS = (
    "username",
    "title",
    "subs",
    "avgViews",
    "view_rate",
    "est_cost_eur",
    "affordable",
    "low_engagement",
    "lang",
    "category",
    "score",
    "price_paid",
    "notes",
)


def fetch_page(query_term, offset):
    """Fetch one page, optionally authenticating with TGADSSPY_KEY."""
    query = urllib.parse.urlencode(
        {
            "q": query_term,
            "minMembers": MIN_MEMBERS,
            "limit": PAGE_SIZE,
            "offset": offset,
        }
    )
    request = urllib.request.Request(
        f"{BASE}/channels?{query}",
        headers={"User-Agent": "tg-vpn-project/1.0"},
    )
    key = os.environ.get("TGADSSPY_KEY", "").strip()
    if key:
        request.add_header("X-Api-Key", key)

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                payload = json.load(response)
            break
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == MAX_RETRIES:
                raise
            retry_after = number(error.headers.get("Retry-After"))
            if retry_after is not None and retry_after > MAX_AUTOMATIC_RETRY_DELAY:
                raise RuntimeError(
                    f"API rate limit requires waiting {retry_after:g} seconds; "
                    "retry later or configure TGADSSPY_KEY"
                ) from error
            delay = retry_after if retry_after is not None else 2**attempt
            time.sleep(max(0, delay))
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError(f"Unexpected response from /channels for query {query_term}")
    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise ValueError(f"Missing pagination metadata for query {query_term}")
    return payload["data"], meta


def fetch_query(query_term):
    """Fetch all API-reachable pages for one channel search term."""
    channels = []
    offset = 0
    while True:
        page, meta = fetch_page(query_term, offset)
        channels.extend(page)
        if not meta.get("hasMore"):
            break

        next_offset = meta.get("nextOffset")
        max_offset = number(meta.get("maxOffset"))
        if next_offset is None and max_offset is not None and offset >= max_offset:
            print(
                f"warning: q={query_term} results limited by API reachability at offset {offset}; "
                "set a valid TGADSSPY_KEY to expand access",
                file=sys.stderr,
            )
            break
        if not isinstance(next_offset, int) or next_offset <= offset:
            raise ValueError(f"Invalid pagination metadata for query {query_term}")
        offset = next_offset
    return channels


def number(value):
    """Return a finite numeric value, or None for missing/invalid API data."""
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def actual_paid_price(channel):
    """Read a paid price only when the API explicitly supplies one."""
    for field in ("price_paid", "pricePaid"):
        value = number(channel.get(field))
        if value is not None and value >= 0:
            return value
    return None


def price_sanity(channel, price_paid, views):
    """Return a price score and note source without treating estimates as paid."""
    if price_paid is not None and views > 0:
        cpm = price_paid / views * 1000
        return (
            max(0.0, 100.0 * (1.0 - cpm / MAX_SANE_CPM_EUR)),
            f"paid CPM €{cpm:.2f}; sanity ceiling €{MAX_SANE_CPM_EUR:.0f}",
        )

    estimated_cpm = number(channel.get("estimatedCpm"))
    if estimated_cpm is not None and estimated_cpm >= 0:
        return (
            max(0.0, 100.0 * (1.0 - estimated_cpm / MAX_SANE_CPM_EUR)),
            f"estimated CPM €{estimated_cpm:.2f}; sanity ceiling €{MAX_SANE_CPM_EUR:.0f}",
        )
    if price_paid is not None:
        return 0.0, "no views; CPM cannot be checked"
    return 50.0, "price unavailable; sanity factor neutral"


def score_channel(channel):
    """Combine views-per-sub with CPM sanity; unknown prices are neutral."""
    raw_subs = number(channel.get("members"))
    raw_views = number(channel.get("avgViews"))
    subs = raw_subs
    views = raw_views
    if subs is None or subs <= 0:
        subs = 0
    if views is None or views < 0:
        views = 0

    views_per_sub = views / subs if raw_subs and raw_subs > 0 and raw_views is not None else None
    score_view_rate = views_per_sub if views_per_sub is not None else 0
    engagement_score = min(score_view_rate, 1.0) * 100
    estimated_cost = views / 1000 * ESTIMATED_CPM_EUR if raw_views is not None else None
    price_paid = actual_paid_price(channel)
    price_score, price_note = price_sanity(channel, price_paid, views)

    score = 0.7 * engagement_score + 0.3 * price_score
    notes = [
        f"views/sub={views_per_sub:.3f}" if views_per_sub is not None else "view rate unavailable",
        price_note,
    ]

    return {
        "username": channel.get("username", ""),
        "title": channel.get("title", ""),
        "subs": int(subs),
        "avgViews": int(views),
        "view_rate": "" if views_per_sub is None else f"{views_per_sub:.4f}",
        "est_cost_eur": "" if estimated_cost is None else f"{estimated_cost:.2f}",
        "affordable": (
            "unknown"
            if estimated_cost is None
            else "yes" if estimated_cost <= MAX_ESTIMATED_COST_EUR else "no"
        ),
        "low_engagement": (
            "unknown"
            if views_per_sub is None
            else "yes" if views_per_sub < 0.10 else "no"
        ),
        "lang": channel.get("lang", ""),
        "category": channel.get("category", ""),
        "score": f"{score:.2f}",
        "price_paid": "" if price_paid is None else f"{price_paid:.2f}",
        "notes": "; ".join(notes),
        "_score": score,
        "_views_per_sub": score_view_rate,
    }


def main():
    rows_by_username = {}
    query_counts = {}
    for query_term in QUERIES:
        channels = fetch_query(query_term)
        eligible = [
            channel
            for channel in channels
            if number(channel.get("members")) is not None
            and number(channel.get("members")) >= MIN_MEMBERS
        ]
        query_counts[query_term] = len(eligible)
        for channel in eligible:
            username = str(channel.get("username", "")).strip().lstrip("@").lower()
            if not username:
                continue
            row = score_channel(channel)
            row["username"] = username
            if username in rows_by_username:
                existing = rows_by_username[username]
                existing["_queries"].add(query_term)
                if row["_score"] > existing["_score"]:
                    row["_queries"] = existing["_queries"]
                    rows_by_username[username] = row
            else:
                row["_queries"] = {query_term}
                rows_by_username[username] = row

    rows = sorted(
        rows_by_username.values(),
        key=lambda row: (-row["_score"], -row["_views_per_sub"], row["username"]),
    )
    affordable_rows = [
        row for row in rows if row["affordable"] == "yes"
    ]
    proxy_rows = sorted(
        (row for row in rows if "proxy" in row["_queries"]),
        key=lambda row: (-row["_score"], -row["_views_per_sub"], row["username"]),
    )[:10]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({field: row[field] for field in FIELDS} for row in rows)

    for query_term, count in query_counts.items():
        print(f"q={query_term}: {count} eligible channels")
    print(f"Wrote {len(rows)} channels to {OUTPUT}")
    print(f"\nAffordable channels (estimated cost <= €{MAX_ESTIMATED_COST_EUR:.0f}):")
    for row in affordable_rows:
        print(
            f"{row['username']}\t{row['title']}\tview_rate={row['view_rate']}"
            f"\test_cost_eur={row['est_cost_eur']}\tscore={row['score']}"
        )
    print("\nTop 10 proxy-query channels (ranked by score):")
    for row in proxy_rows:
        print(
            f"{row['username']}\t{row['title']}\tview_rate={row['view_rate']}"
            f"\test_cost_eur={row['est_cost_eur']}\tscore={row['score']}"
        )


if __name__ == "__main__":
    main()
