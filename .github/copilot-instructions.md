# Project instructions

Telegram channel-placement affiliate project. VPN affiliate, niche = crypto users
in restricted geos. Budget €250/month. Read `docs/brief.md` for the reasoning
behind every rule here — use it to judge cases these rules don't cover.

## Rules (non-negotiable)
- Revshare, never flat CPA. Compounding is the entire point.
- All traffic goes through our bridge page with email capture. The email list is
  the only asset we own.
- Expand one axis at a time. Never new-audience + new-product together.
- Personalise only on facts we hold: traffic source, geo, stated preference.
- Never commit secrets. Keys go in GitHub Secrets or `.vscode/mcp.json` inputs.
- Match copy language to the channel's language.

## The one metric
Cost per email opt-in. Target < €3. > €7 means the page is weak. Sales are
secondary in month one.

## Kill gates
- day 14: < 5 opt-ins from €100 → page or channel list is wrong
- day 30: opt-ins but 0 sales from 40+ emails → angle is wrong
- day 60: no repeatable channel → change niche, not product

## Conventions
- `data/raw/YYYY-MM-DD/*.json` — daily snapshots, committed by cron. Don't edit by hand.
- `data/processed/results.csv` — header:
  `date,channel,subs,views,price_paid,opt_ins,sales,revenue,notes`
- `funnel/` — bridge page + email copy, versioned
- `docs/decisions.md` — append a dated entry whenever a decision is made

## Data source
`tgadsspy.com/api/v1` — free anonymous; 600 req/min with a key in `TGADSSPY_KEY`.
Never hardcode. VPN is 8th niche by volume (~29k creatives). Attribution gap in
AE/ES/FR means geo targeting is unreliable there.

## When asked to do something
Prefer committing working code over describing it. If a rule conflicts with a
request, say so rather than silently following the request.