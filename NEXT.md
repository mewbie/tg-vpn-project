# Next actions

## Tomorrow, after ~00:30 (ban expires ~3h after 21:27)
1. Confirm cron disabled: `gh workflow list`
2. Warm-up, single request, then wait 60s:
   curl -s -H "X-Api-Key: $TGADSSPY_KEY" \
     "https://tgadsspy.com/api/v1/channels?q=proxy&limit=100&offset=0"
3. Resume crypto tail: `START_OFFSET=2100 python3 scripts/fetch_channels.py crypto`
4. Narrow terms, smallest set first:
   `python3 scripts/fetch_channels.py крипто kripto کریپتو forex airdrop defi web3 signals`
5. Recompute the true floor: `python3 scripts/channels.py`
6. Re-enable cron ONLY after a clean full run: `gh workflow enable snapshots.yml`

## Unblocked tonight (no API)
- DM the 10 shortlisted channels, sub-ID each with ?c=<handle>
- Open each channel first; verify topic, recency, reachable admin

## Known constraints
- 5100 records/query, maxOffset 5000 (FREE). 2100 was a ban, not a cap.
- estimatedCpm is null on FREE -> price from a CPM band.
- lang field is unreliable; verify manually.
- Abort fetch on first error body. Every poke resets the fade.
