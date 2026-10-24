## 2026-10-24 — Chose VPN over crypto exchange
Reason: closer to my existing knowledge (networking), faster approval, easier
explanation in own voice. Cost: lower ticket than crypto revshare.
Revisit if: opt-in cost is good but sales are poor.
## 2026-10-24 — Revshare over CPA
Compounding is the only mechanism by which 250 EUR becomes a salary. A flat CPA
pays once and stops. Revisit if: revshare programs reject or cap us.

## 2026-10-24 — Telegram placements over Google Ads / SEO comparison sites
BHW documents both as saturated for VPN (one member spent 1,500 USD with no
profit). Telegram placements have no CNET/Forbes competitor in the auction.

## 2026-10-24 — Niche: crypto users in restricted geos
Highest combined reach and willingness to pay. On Telegram in volume, already
spend on crypto, acute pain from geo-blocked exchanges and KYC IP flags.

## 2026-10-24 — Own product deferred to phase 3
Affiliate first, to learn the funnel on someone else's infrastructure at zero
build cost. Build only once we know what converts.

## 2026-10-24 — Applied to three VPN affiliate programs
PureVPN, Surfshark, NordVPN. Applications submitted same day, in parallel rather
than sequentially, because approval has an uncontrollable delay and the affiliate
link is required before any traffic can be monetised.

- Website URL submitted: https://voluble-sorbet-a8e5ca.netlify.app
- Audience category: Crypto. Website language: English.
- Status: pending approval on all three.
- First to approve is the one we use. No plan changes except one URL.

### On approval, record for the chosen program
- Cookie window length (expect 90 days for PureVPN — CONFIRM, it came from
  third-party reviews)
- Revshare percentage and whether it is lifetime
- Payout minimum and method
- Which of the six traps appear in the actual terms
- The affiliate link, and the sub-ID parameter format

## 2026-10-24 — Chose Netlify over Carrd for hosting
Carrd's free tier limits form elements and the routing question needs anchors
rather than JS. Netlify Drop deploys in seconds, is free, and the page is a
versioned file in the repo rather than a config in a web UI.

## 2026-10-24 — Deferred renaming the Netlify URL
The random subdomain (voluble-sorbet-a8e5ca) is already on three applications.
Renaming would change the URL and risk breaking references. Revisit once there is
a custom domain.

## 2026-10-24 — Page rebuild pending
funnel/index.html is currently an article with no conversion mechanics. It was
built from docs/brief.md rather than funnel/copy.md. Rebuild required: credential
intro, routing question with 4 JS buttons, 4 variants, email capture, CTA.

## 2026-10-24 — tgadsspy free tier: hard constraints (ban active)

- Free tier caps `offset` at 10,000 and sorts by `members` DESC. Paginated
  queries therefore only ever surface the largest channels. Sampling bias.
- `q=crypto` reports 153,022 total. 2,100 retrieved before the ban hit.
  **2,100 is the BAN BOUNDARY, not a proven API cap.** Re-test page 22+.
- Floor over those 2,100: 24,443 members, median 132,163. Sort is DESC and the
  boundary is wherever the ban landed, so the true floor is likely lower.
- `data/raw/ch-crypto-{21..99}.json` are byte-identical quarantine bodies
  (289 bytes, md5 identical). Script wrote error bodies as data and continued
  -> 79 requests burned into an active quarantine.
- Signature: {"error":"identity_quarantined","level":"banned",
  "retryAfterMs":10800000}. Fades ONLY if no further requests land.
- Probable trigger: two loops running concurrently + no error detection.

### Enforced in scripts/fetch_channels.py
1. No `channels` key -> error body, abort.
2. Any `error` field -> abort entire run, wait 3h.
3. Jittered delay 3.0-5.5s.
4. One term at a time.

### Primary filters are now real fields, not guesses
`estimatedCpm` (cost/post = avgViews/1000 * cpm) | `lang` (fa,ru,tr,uz,kk,az)
| `isSponsoredEligible`.

### Cron
snapshots.yml disabled during ban (fires from GitHub IP with same key).
Re-enable: gh workflow enable snapshots.yml

## 2026-10-24 — tgadsspy free tier: real API limits (supersedes the offset-cap note)

Source: the `meta` block of a clean response, `data/raw/ch-crypto-0.json`.
Readable offline, zero API cost.

The API's own numbers:
    total: 153022 | reachable: 5100 | totalReachable: 5100 | maxOffset: 5000 | plan: FREE

Corrections to what we believed earlier:
- Offset cap is 5,000 (maxOffset), NOT 10,000. Full set for any query is 51 pages.
- Reachable records per query is 5,100 (totalReachable). Hard ceiling, FREE plan.
- 2,100 was the BAN BOUNDARY, not a cap. We hold 2,100 of 5,100 = 41%.
- offsetClamped: false. Requests were not being silently truncated.

Consequences:
- The 24,443 floor is the 2,100th-largest channel. PROVISIONAL, not a real floor.
  ~3,000 channels exist below it and have never been fetched.
- The €10-25/post target band most likely sits in offsets 2,100-5,000.
- Any term whose `total` is <= 5,100 is FULLY covered. That is the only route
  into the small tail. Terms far above 5,100 give a top-5,100 sample only.

Pending:
- Fetch crypto offsets 2,100-5,000 (30 pages), then recompute the true floor.
- Check each term's `total` in the first response before committing to a full run.

Ban signature: {"error":"identity_quarantined","level":"banned","retryAfterMs":10800000}
Fades ONLY if no further requests land. Every extra poke resets the clock.
