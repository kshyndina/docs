# Best practices

Environment, configuration, and client-code patterns that keep a high-volume Solana gRPC stream connected under load. Tested against Yellowstone-fed streams from trading bots to indexers.

{% hint style="warning" %}
**Work in progress.** This page is being reviewed -- don't reference it yet, copy isn't final.
{% endhint %}

A high-volume Solana gRPC stream is a tight conversation between your client and the network. If your environment, configuration, or code can't keep up with current throughput, data accumulates in buffers, you drift off the tip of the chain, and the stream disconnects.

Solana's average daily TPS nearly doubled in the first quarter of 2026 (~832 → ~1,570), and the full-chain Yellowstone feed can now spike to 1.3-1.8 Gbps during busy periods. The practices below are what we see in setups that stay connected under load. Most apply whether you're on Triton or anywhere else.

## Environment

Your subscriber's hardware, network capacity, and physical distance to the endpoint set the ceiling on what every other optimisation can do.

### Provision enough bandwidth

10 Gbps download capacity is the recommended target for full-chain subscriptions (accounts plus transactions). 5 Gbps is the minimum for any large subscription. Many cloud instance types cap network at ~1 Gbps by default, which is only enough for narrow, single-program streams. Check your instance class before you debug code.

### Stay close to the endpoint

Target a round-trip time of ≤ 50 ms from your subscriber to the Triton endpoint. Distance compounds: longer routes mean more router hops, each adding propagation and queueing delay. Yellowstone gRPC also has a hard ceiling here, since the HTTP/2 maximum window size of 14.6 MiB caps full-chain streaming around 60 ms RTT at 2 Gbps. Below 50 ms gives you headroom for jitter and variable network conditions.

Measure with `ping <your-endpoint>` from the same host that runs your subscriber. If you're on a major cloud, switching to a region near a Solana validator hub (Frankfurt, Tokyo, or US East) is usually a one-config change.

### Don't run subscribers on serverless

Cloud Lambdas (AWS Lambda, Cloud Functions, equivalent) don't pair well with persistent streaming connections. They leave open connections on the server side, accumulate state outside the lifecycle the platform expects, and degrade over time. Run subscribers on long-lived compute: VMs, dedicated hosts, or containers with stable lifetimes.

### Use a real gRPC client

Vanilla Node.js can't keep up with Solana streaming volume on its own. Use Rust, Go, or the [Yellowstone Node.js / TypeScript client](https://github.com/rpcpool/yellowstone-grpc/tree/master/examples/typescript) we maintain for that runtime. The standard `@grpc/grpc-js` package will fall behind under load.

## Configuration

### Enable adaptive flow-control window

gRPC runs on HTTP/2, which uses a flow-control window to gate how much data the server can have in flight before the client acknowledges it. If the window is smaller than the bandwidth-delay product (bandwidth × RTT), part of your pipe sits idle. Adaptive sizing lets the client and server negotiate the window dynamically based on observed throughput.

There's no good reason to leave this off.

```rust
GeyserGrpcBuilder::from_shared("https://your-endpoint.rpcpool.com")
    .http2_adaptive_window_size(true)
```

### Enable zstd compression

Compression cuts the bytes on the wire, lowers your bandwidth-delay product, and reduces sensitivity to packet loss and jitter. Enable it when your RTT is ≥ 7 ms or when you're running a full-chain subscription. At 30 ms or higher, it's effectively required to stay on the tip.

```rust
GeyserGrpcBuilder::from_shared("https://your-endpoint.rpcpool.com")
    .accept_compressed(Some(CompressionEncoding::Zstd))
```

### Filter as narrowly as the use case allows

Every byte you receive is a byte that has to travel, decompress, deserialise, and queue. Subscribe only to the programs, accounts, and transaction types you actually consume. Mutate filters in place during the stream rather than opening a wide subscription and discarding most of it client-side.

### Pick the right commitment level

Use the lowest commitment that your application can tolerate. `processed` gives the fastest signal, `confirmed` is the safest default for most apps, `finalized` only matters when irreversibility is a hard requirement. Higher commitments add latency and reduce throughput, so don't pay for `finalized` if `confirmed` is good enough.

## Client code

### Decouple ingestion from processing

A receive loop that parses, writes to a database, and acknowledges in the same thread will fill buffers and disconnect under current chain activity. The receive loop should push messages into a queue or channel and immediately wait for the next one. Workers handle parsing, writes, and downstream calls in parallel.

This is the single most common cause of disconnects we see in support tickets.

### Reconnect with exponential backoff

Disconnects happen, even on healthy clients (network blips, leader rotations, pod restarts on the server side). Reconnect logic should:

- Retry on disconnect, with backoff that doubles each attempt and caps at a sensible ceiling (e.g. 30 seconds)
- Reset the backoff once a connection holds for a defined window
- Log every reconnect with the disconnect reason so patterns are visible in your monitoring

For workloads where missing data between disconnect and reconnect is unacceptable, use [Fumarole](fumarole-persistent-streams.md) instead and resume from the last cursor.

### Send keepalive pings

Configure HTTP/2 keepalives at ~30-second intervals so dead connections fail fast instead of hanging. Most Solana gRPC client libraries expose this on the channel builder.

### Handle every stream event

Wire up handlers for `data`, `error`, `end`, and `close` (or your language's equivalent). A missed `error` or `close` handler is how a "silent" disconnect turns into stale data nobody notices for hours.

### Monitor and alert

Track at minimum:

- Connection state and uptime
- Messages per second received
- Lag from `processed` slot to your latest received slot
- Reconnect count over time

Alert when any of these cross a threshold. The test client below is a useful local benchmark, but production monitoring is what catches drift.

### Test before production

The Yellowstone test client benchmarks your end-to-end setup with the exact filters and flags you plan to use. It sends an application-level ping every ~10 seconds alongside the data stream, so you can see whether your client is keeping up with the chain.

```bash
./client-ubuntu-22.04 \
  --http2-adaptive-window true \
  --compression zstd \
  --endpoint https://<your-endpoint>.rpcpool.com \
  --x-token <your-token> \
  subscribe \
  --transactions \
  --accounts \
  --stats
```

Read the output:

- **Healthy:** ping number increases by 1 every ~10 seconds, full-chain throughput sits in the 60-80 Mbps range
- **Behind:** ping interval stretches to 12+ seconds or stops entirely, throughput is below the band

If the test client falls behind on a clean machine, your environment or filters need attention before you run production traffic.

## Pick the right streaming product

[Dragon's Mouth](dragon-s-mouth-grpc.md) is built for ultra-low-latency consumers: trading bots, MEV searchers, liquidation engines. It's stateless. It streams the chain as it happens and doesn't track what you missed.

[Fumarole](fumarole-persistent-streams.md) sits between Dragon's Mouth and your client, caching ~48 hours of history and the exact cursor where you disconnected. Use Fumarole when:

- You're indexing, doing analytics, or running compliance or accounting pipelines
- You need to backfill arbitrary windows after a disconnect
- You only consume confirmed data and the latency floor of confirmed delivery is fine

The same Geyser pipeline feeds both, and you don't have to choose one forever. Many teams run Dragon's Mouth for the hot path and Fumarole for the durable downstream copy.

## Pre-support checklist

If you're hitting disconnects and want help from Triton support, please confirm the following before opening a ticket. We'll ask for these answers, so it's faster to gather them upfront.

- What is your download capacity from the subscriber host? 10 Gbps is ideal for full-chain subscriptions
- What is the round-trip latency from the subscriber to the Triton endpoint? ≤ 50 ms is ideal
- Is HTTP/2 adaptive window enabled on the client?
- Is zstd compression enabled on the client?
- What throughput and ping interval does the Yellowstone test client report on the same host with the same filters?
- Are you running on a serverless platform (Lambda, Cloud Functions, etc.)?
- What client language and library version are you on?

Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one) with that information attached.

## See also

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-compass">:compass:</i> <strong>Streaming overview</strong></td><td>Compare every Triton streaming service side by side.</td><td><a href="overview.md">overview.md</a></td></tr><tr><td><i class="fa-play">:play:</i> <strong>Streaming quickstart</strong></td><td>Test every Triton streaming service in under five minutes.</td><td><a href="quickstart.md">quickstart.md</a></td></tr><tr><td><i class="fa-radio">:radio:</i> <strong>Dragon's Mouth gRPC</strong></td><td>Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC.</td><td><a href="dragon-s-mouth-grpc.md">dragon-s-mouth-grpc.md</a></td></tr><tr><td><i class="fa-layer-group">:layer-group:</i> <strong>Fumarole reliable streams</strong></td><td>Redundant streaming layer with 96h of stored data and built-in cursor resume.</td><td><a href="fumarole-persistent-streams.md">fumarole-persistent-streams.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
