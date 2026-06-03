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

- **Cost calculator.** Set each slider to expected monthly volume. The total estimates your spend at that rate. Minimum deposit {"$"}125.
- **Dedicated node.** Fixed monthly price covers gRPC streaming. Other services use the same rates as shared infrastructure.

  <button type="button" className="triton-calc-mode-btn active" data-mode="custom">Custom PAYG</button>
  <button type="button" className="triton-calc-mode-btn" data-mode="dedicated">Dedicated nodes</button>

      Minimum deposit is {"$"}125
      {"$"}125.00
      USD

      Start shipping with

      <ul className="triton-calc-features">
        <li>Global bare-metal node network</li>
        <li>GeoDNS routing, auto-failover</li>
        <li>1-on-1 support from senior engineers</li>
        <li>Overage billed at the base rate</li>
        <li>gRPC and WebSockets streaming</li>
        <li>Full access to Yellowstone suite tools</li>
        <li>Turnkey access to advanced APIs</li>
        <li>Solana, Pythnet, Sui, and Monad</li>
      </ul>

      <p className="triton-calc-fineprint">Deposit is prepaid, non-refundable, and valid for 12 months.

        <a className="triton-calc-cta" href="https://customers.triton.one/onboarding" data-cta>Get started →</a>
        Minimum deposit is {"$"}125.00

              Bandwidth across all services
              $0.08 / GB bandwidth

            $0.00

            <input type="range" min="0" max="10000" step="100" defaultValue="0" data-input />

              Standard RPC, indexed accounts, ledger queries
              $10 / million calls + bandwidth

            $0.00

            <input type="range" min="0" max="10" step="0.1" defaultValue="0" data-input />

              Streaming services, Titan Prime API
              $0.08 / GB bandwidth

            $0.00

            <input type="range" min="0" max="10000" step="100" defaultValue="0" data-input />

              Metaplex, Photon APIs
              $50 / million calls + bandwidth

            $0.00

            <input type="range" min="0" max="10" step="0.1" defaultValue="0" data-input />

              Metis API
              $80 / million calls + bandwidth

            $0.00

            <input type="range" min="0" max="10" step="0.1" defaultValue="0" data-input />

  Solana dedicated node

  {"$"}2,900+
  USD per month

  Start shipping with

  <ul className="triton-calc-features" data-chain-features>
    <li>Unmetered gRPC streaming</li>
    <li>Full access to Yellowstone suite and advanced APIs</li>
    <li>Custom geolocated deployment</li>
    <li>Isolated performance, dedicated to your traffic</li>
    <li>Advanced controls and tuning for your workload</li>
    <li>GeoDNS routing and automatic failover</li>
    <li>1-on-1 support from senior engineers</li>
  </ul>

  gRPC streaming (Dragon's Mouth)
  Included in the node price, no overage fees

  Fumarole, Whirligig, WebSockets, other streaming
  $0.08 / GB bandwidth

  <a className="triton-calc-cta" href="https://triton.one/contact" data-cta>Contact sales →</a>

## How pay as you go works

Once you've made a deposit, it's valid for a year and draws down as you use the services. Top up any time from your dashboard.

There is no free trial, as the deposit replaces it: you get a year of testing room with the same account, endpoint, and tokens you'd ship to production.

{% hint style="info" %}
[Sign up at customers.triton.one](https://customers.triton.one/users/sign-up). For a step-by-step, see [How to sign up](../../guides/account-management/how-to-sign-up.md).
{% endhint %}

## What's next

{% content-ref url="quickstart.md" %}
[Quickstart](quickstart.md)
{% endcontent-ref %}

{% content-ref url="platform-overview.md" %}
[Account management](platform-overview.md)
{% endcontent-ref %}

{% content-ref url="rate-and-connection-limits.md" %}
[Rate and connection limits](rate-and-connection-limits.md)
{% endcontent-ref %}

{% content-ref url="plans-and-billing.md" %}
[Metered billing walkthrough](plans-and-billing.md)
{% endcontent-ref %}

---

---

Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  
Sales questions? [Contact sales](https://triton.one/contact).  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
