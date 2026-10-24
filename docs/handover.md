# Handover — full project context

Date: 2026-10-24
Status: pre-launch. Repo exists, cron works, nothing spent, no affiliate approval.
Purpose: complete context so work continues without the original conversation.

## 1. What this is
Telegram channel-placement affiliate project. Buy sponsored posts in Telegram
channels, send traffic through our own bridge page, capture email, monetise via
affiliate offer on recurring revshare. Goal: replace a day job in 5 years. Solo.

## 2. Constraints
- 250 EUR/month ad budget. No capital for buying assets.
- Technical background: networking / internet infrastructure. A real edge — it is a
  credential for VPN content and rare among affiliates.
- Working alone. First month expected result: break-even or slightly negative.

## 3. The strategic model (read before judging anything)
Every tactic decays. Positions do not.
- Four layers: price asymmetry in attention, intermediary position, conversion of
  perishable traffic into durable claims, decay clock. The asymmetry is the entry
  fee; the position is the business.
- Decay rate tracks visibility. Public-data-visible asymmetries die fastest
  (creative cloning, weeks). Hidden ones last longest (search squatting, 12-24mo).
  Use public data to find opportunity; put money where data is blind.
- The quadrant. fast/fragile (entry: arbitrage) vs slow/durable (asset: owned list,
  revshare base, proprietary data, brand). Start top-left, migrate deliberately.
- Ownership gradient. feed follower < telegram subscriber < email list < paying
  customer. Every play moves people rightward.
- Rule: acquire on the fastest asymmetry available, convert to the slowest position
  affordable.

Evidence: a documented BHW journey peaked at 22k USD in one month, ~20k of it from
referral commissions on users acquired months earlier, while the method itself had
already stopped working. The method died; the position paid.

## 4. Decisions made
- 2026-10-24 Chose VPN over crypto exchange. Closer to existing knowledge, easier
  approval, easier to explain in own voice. Cost: lower ticket. Revisit if opt-in
  cost is good but sales are poor.
- 2026-10-24 Revshare over CPA. Compounding is the only way 250 EUR becomes a salary.
- 2026-10-24 Telegram placements over Google Ads / SEO comparison sites. Both
  documented saturated for VPN. Telegram has no CNET/Forbes competitor.
- 2026-10-24 Niche: crypto users in restricted geos. Highest combined reach + ticket.
- 2026-10-24 Own product deferred to phase 3.

## 5. Product and niche
Product: VPN affiliate. PureVPN preferred (90-day cookie, 35% lifetime recurring,
2-tier sub-affiliates). Fallbacks: Surfshark, NordVPN, TorGuard. Verify terms.
Niche: crypto users in restricted geos (IR, RU, TR, UZ, KZ).
Known risk: proxy-channel audiences use free proxies and may not pay. Mitigate by
attacking the free tier in copy. A live VPN ad already uses this angle.
Expansion order: same product/new audiences first, then same audience/new product
(residential proxies). Never both axes at once.

## 6. The funnel
Traffic to bridge page to email capture to affiliate link. Plus 3 emails
(deliver / help / check-in) and a day-1/7/30 retention layer.
Personalise only on facts we hold (traffic source via sub-ID, geo, language, stated
preference). Match copy language to channel language. Be a named person with a
reply-able handle.

## 7. Rules — non-negotiable
- Revshare, never flat CPA.
- All traffic goes through the bridge page. The email list is the only asset.
- One expansion axis at a time.
- Personalise only on true facts.
- Never commit secrets.
- Match copy language to channel language.

## 8. Metrics and gates
The one metric: cost per email opt-in. Target under 3 EUR. Over 7 EUR means the
page is weak.
Kill gates:
- day 14: under 5 opt-ins from 100 EUR means page or channel list is wrong
- day 30: opt-ins but 0 sales from 40+ emails means the angle is wrong
- day 60: no repeatable channel means change niche, not product

## 9. Verified data (2026-10-24, public API)
- tgadsspy.com/api/v1/stats works anonymous, no key.
- VPN: 29,132 creatives, 8th niche by volume. Moderate, not saturated.
- Geo intent: RU 195,674, IN 56,890, IR 51,560, MM 27,036, AE 46,472.
- AE: 46,472 intent vs 1,456 confident (97% gap). Attribution broken there.
- totalReachable 101, maxOffset 100 on ANON. A free key is required.
- Biggest Telegram channels are proxy channels (Proxy MTProto ~11.9M subs).
- CPM benchmarks (third-party, Q1 2025): 0.03-8 EUR auction; 15-20 EUR direct finance.

## 10. Tech setup
- Repo: tg-vpn-project, private, GitHub.
- scripts/fetch.py: stdlib-only daily snapshot to data/raw/YYYY-MM-DD/.
- .github/workflows/snapshots.yml: daily cron plus workflow_dispatch. Verified green.
- Secret: TGADSSPY_KEY (tgadsspy.com/account/api-keys, free).
- .vscode/mcp.json: Venice MCP server for this agent.
- Git identity: local override to mewbie; global stays work identity.
- Ledger: data/processed/results.csv with columns
  date,channel,subs,views,price_paid,opt_ins,sales,revenue,notes

## 11. Current state
Done: repo, plumbing, cron verified, identity, MCP, strategy, docs.
Not done: API key, affiliate approval, buy list, bridge page, DM outreach, launch.

## 12. Next actions (in order)
1. Get TGADSSPY_KEY, add as GitHub Secret.
2. Apply to PureVPN affiliate. Read terms. Record in docs/decisions.md.
3. Build buy list: pull channels via API, vet 40 on Telemetrio, keep 25.
4. Build bridge page (Carrd + MailerLite free). Copy in funnel/copy.md.
5. Send admin DMs per funnel/dm-template.md.
6. Book 10 placements. Expect 5-30 EUR for small channels.
7. Launch 100 EUR across 10 channels. Hold 150 EUR back for winners.

## 13. Uncertain — re-verify before relying on
- Affiliate terms (third-party reviews, change often).
- CPM figures (stale, third-party).
- Niche ranking (inference, not proven).
- BHW evidence (mostly unfinished journeys).
- API docs (already caught lying about niches.csv being public).
When unsure: verify against the live API before acting.