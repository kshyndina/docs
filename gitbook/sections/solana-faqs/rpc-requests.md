# RPC requests

Questions about Triton's RPC services, latency, rate limits, scripts and monitoring.

## Performance and reliability

How fast and reliable Triton's RPC service is, and what happens during congestion, traffic spikes, or rate-limit hits.

<details>
<summary>How reliable are Triton's RPC services?</summary>

Our infrastructure delivers 99.9% uptime, backed by multiple servers per region and automated health checks. This ensures that nodes stay synced and serve accurate, up-to-date ledger data. If any node falls behind, requests are routed to a shared backup pool while the issue is resolved. Our infrastructure is monitored 24/7, and we're known for fast and responsive support.

As Stephen Hess, founder of Metaplex, put it: "We use Triton RPCs every day at Metaplex. They're fast, reliable, and built by one of the most competent teams I've worked with in Solana or across tech."

</details>

<details>
<summary>How does Triton ensure minimal latency with RPC and gRPC?</summary>

It's a big topic, but at a high level, we do it through:

- **GeoDNS:** Routes traffic to the nearest server in shared pools.
- **Geyser integration:** Streams intra-slot updates via Dragon's Mouth, unlike end-of-slot updates in traditional RPC.
- **Custom indexes:** Steamboat optimises `getProgramAccounts` (gPA) calls to improve query performance.

</details>

<details>
<summary>How does Triton handle network congestion on Solana?</summary>

We mitigate congestion with:

- **Staked nodes:** Prioritise transaction delivery to the block producer.
- **Load balancing:** Distribute traffic across our 100\+ nodes.
- **Rate limiting:** Prevent abuse and ensure fair access.
- **Redundancy:** Automatic failover systems to maintain uptime during outages.

</details>

<details>
<summary>What happens if my gRPC/RPC node receives excessive traffic? Will it affect transaction sending?</summary>

If traffic exceeds your node's capacity, it may lag behind the network's latest state, resulting in older data being served. In such cases, requests will be rerouted to our backup pool, which supports upgrades and traffic spikes but introduces additional latency. This could slow transaction submission. If reliance on the backup pool becomes frequent, we will contact you to discuss scaling your deployment.

</details>

<details>
<summary>What happens if I hit my rate limit?</summary>

Your application will receive `HTTP 429` errors. When this happens, pause requests for 10 seconds to clear the limit. We strongly recommend implementing a backoff-and-retry mechanism. See [Handle 429 rate-limit errors](https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/handle-429-rate-limit-errors) for the pattern, or our [Rate and connection limits](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/rate-and-connection-limits) page for the budgets and headers.

</details>

<details>
<summary>Can I run scripts on the shared service?</summary>

Yes. Shared infrastructure handles backend workloads (scripts, trading bots, indexers) and is sized to absorb traffic spikes. If you expect sustained heavy load (heavy subscriptions, full-chain streams, custom Geyser configurations), a [dedicated node](https://kate-6.gitbook.io/triton-one-docs/documentation/dedicated-nodes/overview) is usually the right choice.

</details>

## Configuration and access

Tokens, endpoints, allowed origins, regions, and the capabilities Triton supports across shared and dedicated infrastructure.

<details>
<summary>How do I monitor my RPC usage?</summary>

Customers with [dedicated nodes](https://kate-6.gitbook.io/triton-one-docs/documentation/dedicated-nodes/overview) get a Grafana dashboard with real-time metrics: request volume, latency, error rates, and bandwidth usage.

    For shared (pay-as-you-go) customers, open the **v3 Billing** tab in your [customer dashboard](https://customers.triton.one). You'll see total requests and GB used (the two dimensions you're billed on), plus a per-service breakdown table with product-level detail. Click **Export CSV** in the top-right corner to download.

</details>

<details>
<summary>Can I create new tokens or endpoints myself?</summary>

Accounts with standard permissions can't create tokens or endpoints directly. Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one) to provision them. If you need self-service, ask support to upgrade you to the operator role -- once enabled, you can add tokens and endpoints from the dashboard yourself.

</details>

<details>
<summary>What's the __blocked.rpcpool.com origin on my endpoint?</summary>

`__blocked.rpcpool.com` is a system origin that Triton automatically adds to every endpoint. It signals that the endpoint only accepts requests authenticated by a valid token, blocking anonymous traffic.

Don't remove it. If you do and leave the allowed origins list empty, the endpoint becomes fully open: anyone can query it without a token, and the resulting traffic will be billed to your account.

</details>

<details>
<summary>How does Triton secure dedicated node endpoints?</summary>

Dedicated node endpoints use:

- **API keys:** unique per client, revocable from the [customer dashboard](https://customers.triton.one).
- **Rate monitoring:** alerts for unusual spikes to detect misuse.

</details>

<details>
<summary>Can I have multiple API keys for the dedicated nodes? Can I manage them by myself?</summary>

Yes. If you have an operator role, you should be able to add them yourself.

</details>

<details>
<summary>Can I choose the geographic location of my RPC nodes?</summary>

Yes, dedicated node users can select primary regions (US, EU, or Asia Pacific) or request multi-region setups for redundancy and lower latency based on their user base.

</details>

<details>
<summary>Are shared RPC subscriptions restricted to a single domain?</summary>

No. You can whitelist as many domains as you need via the **Allowed origins** list on each endpoint. In your [customer dashboard](https://customers.triton.one), click into the mainnet subscription, click the endpoint name to open its settings, and under **Allowed origins** hit `+` to add a new domain. All subdomains are automatically allowed. See [How can I add domains to the allowed origins?](my-account.md) for the full walk-through.

</details>

<details>
<summary>Can Triton provide historical blockchain data?</summary>

Yes, dedicated node users can opt into archival nodes that store full Solana blockchain history (e.g., past blocks, transactions). This requires additional storage (multi-TB scale) and is priced separately -- reach out for a custom quote.

</details>

<details>
<summary>Can I use Jito sendBundle and bundle simulation with Triton RPCs?</summary>

Bundle simulation is available to everyone -- see [Jito bundles](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/jito-bundles) for the full reference.

`sendBundle` itself isn't routed through our infrastructure. Routing bundle sends through Triton would add an extra hop in front of the Jito block engine, which adds latency and works against the reason you're using bundles in the first place. The recommended pattern is to call the Jito block engine directly for sends, and use Triton for everything else (reads, streams, simulation).

</details>

## Troubleshooting

Common issues with WebSocket connections, latency measurement, and gRPC connection monitoring.

<details>
<summary>I have an issue with my Web3.js socket connection. How can I fix it?</summary>

If you're hitting persistent socket or connection errors with `@solana/web3.js` (`fetch failed`, `Connect Timeout Error`, `ECONNREFUSED`, `ECONNRESET`, `other side closed`), see [Web3.js socket and connection issues](https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/web3js-socket-connection-issues). It covers the root causes and the standard fixes.

</details>

<details>
<summary>How can I accurately measure latency when using Triton's RPC services?</summary>

To measure latency effectively, avoid relying on blockchain or explorer timestamps, as these may not reflect the actual performance of your RPC provider due to drift in the timestamping. The on-chain time and clock time drift apart, leading to misleading metrics.

Instead, record a timestamp immediately after receiving a transaction response from each provider in your application. This method captures the actual time it took for the request to complete, providing a reliable metric for assessing latency.

</details>

<details>
<summary>How can I monitor for delays on my gRPC connection?</summary>

To detect delays, examine the `slot` field included in all gRPC messages. The most precise method is to compare this slot value with a secondary source, such as another subscription or a `getSlot` call in your production environment. For additional validation, you may also cross-reference with an alternative RPC provider. Dedicated users can select the "Tracking Tip" folder in their Grafana Dashboard. The slot latency reflected here shows how much your node's slot latency differs from the rest of the network. As the node processes data from the network downstream, it sends this information through Geyser.

If you suspect your Geyser stream is experiencing a drastically different latency, check whether your receiving server is not providing back pressure to the RPC node due to bandwidth constraints.

</details>

---

---

Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  
Sales questions? [Contact sales](https://triton.one/contact).  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
