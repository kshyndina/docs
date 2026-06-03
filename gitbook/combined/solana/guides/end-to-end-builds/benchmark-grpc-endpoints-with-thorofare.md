# Benchmark gRPC endpoints with Thorofare

How to benchmark Solana RPC and Yellowstone gRPC endpoints the right way using Triton's Thorofare tool. Compare providers on like-for-like workloads, not on ping times.

Most Solana RPC benchmarks are misleading. They measure ping or one cherry-picked method, then publish numbers that don't reflect real workloads. **Thorofare** is the tool we built to benchmark the way that actually matters: realistic request mixes, realistic concurrency, and metrics that match what your application sees.

For the long-form rationale, see the [How to benchmark Solana RPC endpoints](https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/) blog post.

## What Thorofare measures

- **HTTPS RPC latency and throughput** -- request/response round-trip across the methods your app actually calls.
- **Yellowstone gRPC subscribe throughput and lag** -- account, transaction, slot, block updates. Measures how far behind real time the stream falls under load.
- **Per-percentile metrics** -- p50, p95, p99 latency. Means hide the tail; tails are what hurt your users.

## When to run it

- Choosing between RPC providers -- give every provider the same Thorofare profile and compare apples to apples.
- Validating a region change -- did moving from `nyc` to `ams` actually reduce p99?
- Diagnosing degraded performance -- is the regression in our infrastructure or your client code?

## Run a benchmark

Thorofare lives in the Triton GitHub. Clone, build, and point it at any RPC or gRPC endpoint with a token.

The full setup, profile examples, and metric interpretation are in the [Thorofare blog post](https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/).

{% hint style="info" %}
Thorofare runs on your machine. Run it from a backend close to where your real production traffic originates -- benchmarking from a different region distorts every result.
{% endhint %}

## Common pitfalls

- **Cold cache vs warm cache.** First-request latency is always higher. Discard the first N requests in your analysis or run a warm-up phase.
- **Rate limits as latency.** If you exceed a provider's rate limit, you'll get 429s that look like high latency. Lower your concurrency until 429s drop to zero, then measure.
- **Single-method benchmarks.** Real apps mix `getAccountInfo`, `getProgramAccounts`, `sendTransaction`, and subscriptions. A `getSlot`-only benchmark says nothing about anything else.
- **Public RPC fairness.** Public endpoints are throttled aggressively. Benchmark against your own paid endpoint, not the public default.

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-gauge">:gauge:</i> <strong>Rate and connection limits</strong></td><td>Per-endpoint and method rate limits, plus streaming connection caps.</td><td><a href="../../documentation/get-started/rate-and-connection-limits.md">../../documentation/get-started/rate-and-connection-limits.md</a></td></tr><tr><td><i class="fa-compass">:compass:</i> <strong>Streaming overview</strong></td><td>Compare every Triton streaming service side by side.</td><td><a href="../../documentation/streaming-data/overview.md">../../documentation/streaming-data/overview.md</a></td></tr><tr><td><i class="fa-shield">:shield:</i> <strong>Auth and security</strong></td><td>Endpoint, token, and spend security. What Triton handles and what you configure.</td><td><a href="../../documentation/get-started/auth-and-security.md">../../documentation/get-started/auth-and-security.md</a></td></tr><tr><td><i class="fa-book">:book:</i> <strong>Thorofare blog post</strong></td><td>Why most gRPC benchmarks are wrong, and how to do them right.</td><td><a href="https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/">https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
