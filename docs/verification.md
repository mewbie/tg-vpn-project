# Verification log — re-run these and append results

Purpose: watch the arbitrage decay. If VPN creative count climbs and CPM rises,
the window is closing.

## 2026-10-24
- curl /api/v1/stats works anonymous. VPN count 29,132 (8th niche by volume).
- curl "/api/v1/ads?niche=vpn&limit=1" returns meta.totalReachable 101 on ANON.
  A free key is required for real pagination.
- curl /api/v1/geos returns RU 195,674 / IR 51,560 / AE 46,472 intent.
- Live VPN creative uses the anti-free-proxy angle. Validated and contested.
- workflow snapshots.yml run #1: green, 16s.
