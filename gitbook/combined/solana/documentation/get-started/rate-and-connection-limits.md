# Rate and connection limits

We apply 2 kinds of limits: rate limits for HTTP requests (per IP, 10-second window) and connection limits for streaming (simultaneous connections per endpoint).

## Rate limits

Two budgets apply at the same time, both reset every 10 seconds, both keyed to the IP making the request:

- **Total RPS** is the budget across every method. If your IP sends 1,000 `getBalance` and 1,000 `getSlot` in 10 seconds, that counts as 2,000 against this budget.
- **Per-method RPS** is a separate budget for each individual RPC method. Even if your total is under the cap, you can hit the per-method cap on a single hot method (most often `getProgramAccounts`, `sendTransaction`, or `getBlock`).

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#F2EDF6','primaryBorderColor':'#7A4BA0','primaryTextColor':'#171717','lineColor':'#956FB3','secondaryColor':'#E4DBEC','tertiaryColor':'#D7C9E3','noteBkgColor':'#FFC845','noteTextColor':'#171717','actorBkg':'#F2EDF6','actorBorder':'#7A4BA0','actorTextColor':'#171717','signalColor':'#492D60','labelBoxBkgColor':'#7A4BA0','labelTextColor':'#F7F7F7','edgeLabelBackground':'transparent'},'flowchart':{'nodeSpacing':18,'rankSpacing':32,'padding':6,'curve':'linear'}}}%%
flowchart LR
    Req("Request from your IP") --> Total("Total RPS<br/>< 2,000 per 10s?")
    Total -->|No| Block("HTTP 429")
    Total -->|Yes| Method("Per-method RPS<br/>under cap?")
    Method -->|No| Block
    Method -->|Yes| OK("Request processed")
```

If either check fails, the response is `HTTP 429 Too Many Requests`. In practice, most 429s come from the per-method limit, not the total.

{% hint style="info" %}
**Per IP** means the IP making the request. Backends sharing one IP share one budget.
{% endhint %}

## Defaults

New accounts on the shared service default to a tier sized for typical workloads (frontends, indexers, light backends). Heavier traffic, especially trading bots and analytics pipelines, often wants higher per-method caps. We can raise yours on request; contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).

## Per-method limits

Methods not listed below fall back to the 2,000-per-10s global budget. Limits group by cap, so methods that share a budget appear on the same row.

### Standard JSON-RPC

| Per 10s | Methods |
| --- | --- |
| 2,000 | Total RPS per IP, `getAccountInfo`, `getTransaction` |
| 400 | `getMultipleAccounts`, `getVoteAccounts`, `getClusterNodes` |
| 200 | `getBlock`, `getConfirmedTransaction`, `getLeaderSchedule` |
| 100 | `getRecentPerformanceSamples`, `getLatestBlockhash`, `getTokenAccountsByOwner`, `sendTransaction` |
| 50 | `getProgramAccounts`, `getTokenLargestAccounts` |

### Streaming services (gRPC)

| Per 10s | Service | Methods |
| --- | --- | --- |
| 5,000 | Old Faithful | `GetBlockTime`, `StreamBlocks`, `StreamTransactions` |
| 2,000 | Fumarole | all methods |
| 1,000 | Old Faithful | `GetBlock`, `GetTransaction`, `Get`, `GetVersion` |
| 1,000 | Vixen | `Subscribe`, `ProgramStreams.Subscribe` |

## Read your live limits

Every endpoint exposes its current limits at `/ratelimits`:

```bash
curl https://<your-app>.mainnet.rpcpool.com/<token>/ratelimits
```

The response is JSON, listing the request budget per window, every per-method override, and the connection cap. It's the source of truth for **your** endpoint's exact numbers, which can differ from the defaults above if support has tuned them.

Every JSON-RPC response also carries `X-Ratelimit-*` headers. Watch them in your client to back off **before** you hit a 429:

| Header | What it tells you |
| --- | --- |
| `X-Ratelimit-Limit` | Total budget for the current 10-second window |
| `X-Ratelimit-Remaining` | How many total requests you have left |
| `X-Ratelimit-Reset` | Seconds until the window resets |
| `X-Ratelimit-Method-Limit` | Per-method cap for this RPC |
| `X-Ratelimit-Method-Remaining` | How many of this method you have left |

If you do hit a 429, see the [Error handling guide](../../guides/error-handling/how-to-troubleshoot.md) for the full debug flow.

## Browser concurrency

Browsers cap parallel HTTP/2 streams to a single host, so a frontend with many parallel calls can self-throttle before Triton's limits ever apply. Best practices:

- Use a single shared `Connection` (web3.js) per page
- Batch reads with `getMultipleAccounts` instead of N parallel `getAccountInfo` calls
- Move heavy reads (program scans, signature crawls) to your backend

## Connection limits

Streaming products (Yellowstone gRPC, Whirligig WebSockets, Fumarole) cap **simultaneous connections per endpoint**, not request rate.

Connection limits are flexible. If you hit one, contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one) and we'll work with you to either optimise usage or raise the cap.

{% hint style="info" %}
A single gRPC connection can multiplex many subscriptions. The right pattern is one connection plus many subscribe messages, not one connection per filter. See [Multiplexing in one connection](../streaming-data/dragon-s-mouth-grpc.md) on Dragon's Mouth for the canonical example.
{% endhint %}

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-credit-card">:credit-card:</i> <strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="plans-and-billing.md">plans-and-billing.md</a></td></tr><tr><td><i class="fa-server">:server:</i> <strong>Dedicated gRPC node</strong></td><td>Private node with isolated CPU and unlimited concurrent gRPC connections. For latency-sensitive or heavy streaming workloads.</td><td><a href="../dedicated-nodes/overview.md">../dedicated-nodes/overview.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
