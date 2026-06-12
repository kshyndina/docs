# Plans and billing

Triton has two billing methods (pay as you go, invoiced) and two infrastructure types (shared, dedicated). Estimate your cost and pick the combination that fits your workload.

## Pay as you go vs invoiced

|  | Pay as you go | Invoiced |
| --- | --- | --- |
| **Sign up** | Self-onboard at [customers.triton.one](https://customers.triton.one/users/sign-up) | Contact sales |
| **Minimum** | \$125 prepaid deposit | \$125 monthly invoice |
| **Billing** | Drawn from your prepaid balance | Billed at the start of each month for the month |
| **Overages** | Not allowed. Top up to avoid service interruptions | Billed in \$100 increments at the same rate at the start of next month |
| **Payment** | Stablecoins only | Card, USDC, wire, hel.io |
| **Cancellation** | None, balance valid for 12 months | 1 calendar month notice |

Pay as you go is the fastest start, and you can sign up at [customers.triton.one](https://customers.triton.one/users/sign-up) right now. Most teams running steady production traffic switch to monthly invoicing once usage stabilises, for two reasons:

- **Overages at the same rate.** If you go over the estimate, you get a follow-up invoice at the same rates: no sudden service interruption.
- **Predictable bills.** Same line items each month, sized around the previous month's volume and adjustable as usage shifts.

To switch to monthly invoicing, contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one) or [contact sales](https://triton.one/contact).

## Shared or dedicated?

Shared infrastructure is best for most workloads. A dedicated gRPC node is a good fit for traders, market makers, and teams where receiving data a millisecond earlier directly influences your PnL. With one, you get full network bandwidth, CPU, flat streaming costs, and minimal latency with backend colocation.

Most dedicated customers run on monthly invoicing; PAYG dedicated is available on request. [Contact sales](https://triton.one/contact) to start.

## Estimate your spend

Pricing is simple: you pay for what you use. Per-million rates for calls, per-GB rates for bandwidth, line-itemed by service.

- **Cost calculator.** Set each slider to expected monthly volume. The total estimates your spend at that rate. Minimum deposit $125.
- **Dedicated node.** Fixed monthly price covers gRPC streaming. Other services use the same rates as shared infrastructure.

| Service | Rate |
| --- | --- |
| Bandwidth across all services | $0.08 / GB bandwidth |
| Standard RPC, indexed accounts, ledger queries | $10 / million calls + bandwidth |
| Streaming services, Titan Prime API | $0.08 / GB bandwidth |
| Metaplex, Photon APIs | $50 / million calls + bandwidth |
| Metis API | $80 / million calls + bandwidth |
| gRPC streaming (Dragon's Mouth) | Included in the node price, no overage fees |
| Fumarole, Whirligig, WebSockets, other streaming | $0.08 / GB bandwidth |

**Included**
- Global bare-metal node network
- GeoDNS routing, auto-failover
- 1-on-1 support from senior engineers
- Overage billed at the base rate
- gRPC and WebSockets streaming
- Full access to Yellowstone suite tools
- Turnkey access to advanced APIs
- Solana, Pythnet, Sui, and Monad
- Unmetered gRPC streaming
- Full access to Yellowstone suite and advanced APIs
- Custom geolocated deployment
- Isolated performance, dedicated to your traffic
- Advanced controls and tuning for your workload
- GeoDNS routing and automatic failover

Minimum deposit $125 (prepaid, non-refundable, valid for 12 months). [Get started](https://customers.triton.one/onboarding)

## How pay as you go works

Once you've made a deposit, it's valid for a year and draws down as you use the services. Top up any time from your dashboard.

There is no free trial, as the deposit replaces it: you get a year of testing room with the same account, endpoint, and tokens you'd ship to production.

{% hint style="info" %}
[Sign up at customers.triton.one](https://customers.triton.one/users/sign-up). For a step-by-step, see How to sign up.
{% endhint %}

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-rocket">:rocket:</i> <strong>Quickstart</strong></td><td>Sign up, deposit, get an endpoint, send your first request.</td><td><a href="quickstart.md">quickstart.md</a></td></tr><tr><td><i class="fa-user-gear">:user-gear:</i> <strong>Account management</strong></td><td>Customer dashboard tour: endpoints, billing, team, and support.</td><td><a href="platform-overview.md">platform-overview.md</a></td></tr><tr><td><i class="fa-gauge">:gauge:</i> <strong>Rate and connection limits</strong></td><td>Per-endpoint and method rate limits, plus streaming connection caps.</td><td><a href="rate-and-connection-limits.md">rate-and-connection-limits.md</a></td></tr><tr><td><i class="fa-pie-chart">:pie-chart:</i> <strong>Metered billing walkthrough</strong></td><td>Track your usage and billing across calls and bandwidth in the customer dashboard.</td><td><a href="plans-and-billing.md">plans-and-billing.md</a></td></tr></tbody></table>
