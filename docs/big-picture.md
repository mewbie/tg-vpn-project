# Big picture

## The system

```mermaid
flowchart TD
    subgraph L1["resources"]
        R1["250 EUR per month budget"]
        R2["networking background"]
        R3["time"]
    end

    subgraph L2["the weekly engine"]
        E1["pick small channels, 20-60 EUR per post"]
        E2["buy placement, unique sub-ID"]
        E3["traffic to bridge page, routing question"]
        E4["email capture"]
        E5["affiliate link, recurring revshare"]
        E1 --> E2 --> E3 --> E4 --> E5
    end

    subgraph L3["two outputs"]
        O1["revshare base, recurring monthly"]
        O2["owned email list"]
    end

    D1{"day 14 gate: 5+ opt-ins?"}
    D2{"day 30 gate: 1+ sale?"}
    D3{"day 60 gate: repeatable channel?"}

    subgraph L4["asset layer, what survives"]
        A1["own channel"]
        A2["channel portfolio"]
        A3["own product"]
    end

    DC["decay clock: methods die, positions survive"]

    R1 --> E1
    R2 --> E1
    R3 --> E1
    E5 --> O1
    E5 --> O2
    O1 --> D1
    O2 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> A1
    D3 --> A2
    D3 --> A3
    D1 -->|fix funnel, not product| E1
    D2 -->|fix funnel, not product| E1
    D3 -->|fix funnel, not product| E1
    DC -.-> E1
```

## How to read it

Top to bottom, one sentence: convert a temporary asymmetry into a permanent
position, and let the gates decide whether you are allowed to.

- **Resources** — the three things actually available.
- **The engine** — a weekly loop. Email capture sits before the affiliate link;
  that ordering is the design.
- **The two outputs** — revshare and the email list are the asset, not the reward.
- **The gates loop backward, not down.** A failed gate means fix the funnel, not
  change the product.
- **The asset layer** — own channel, portfolio, own product.
- **The dotted line** — the decay clock hits tactics; the asset is what you built
  before it arrived.

## Phases

| Phase | When | Income | You own |
|---|---|---|---|
| 0 Setup | done | 0 | nothing |
| 1 Validate | month 1-3 | 0-300 | small email list |
| 2 Repeat | month 3-9 | 300-1,500 | working channel list |
| 3 Own inventory | month 9-24 | 1,500-6,000 | a channel |
| 4 Portfolio + product | year 2-5 | 6,000-20,000 | a business |

Phase 1 exit is not income. It is cost per opt-in under 3 EUR.