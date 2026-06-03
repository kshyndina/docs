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

[Rate and connection limits](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/rate-and-connection-limits)

[Streaming overview](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/overview)

[Auth and security](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security)

[Thorofare blog post](https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/)

---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
