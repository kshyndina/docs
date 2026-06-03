# Rate tiers

Read and configure per-endpoint rate limits via the Account Management API.

The Rate tiers resource exposes the per-endpoint rate-limit configuration. Configurable on dedicated; read-only on shared by default (support can tune on request).

Resource path: `/v1/endpoints/{endpoint_id}/rate-tier`

## Get the current rate tier

```text
GET /v1/endpoints/{endpoint_id}/rate-tier
```

```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/rate-tier \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

```json
{
  "endpoint_id": "ep_abc123",
  "general": {
    "requests_per_window": 1200,
    "window_seconds": 10,
    "concurrent_requests": 100
  },
  "method_overrides": [
    {
      "method": "getProgramAccounts",
      "requests_per_window": 60,
      "window_seconds": 10
    },
    {
      "method": "getTokenAccountsByOwner",
      "requests_per_window": 200,
      "window_seconds": 10,
      "applies_when": "data_size > 1000000"
    }
  ],
  "streaming": {
    "max_concurrent_grpc_subs": 10,
    "max_concurrent_ws_connections": 50
  },
  "configurable": false,
  "plan": "payg"
}
```

`configurable: false` on shared. Dedicated endpoints have `configurable: true` and accept the PATCH below.

## Update the rate tier (dedicated)

```text
PATCH /v1/endpoints/{endpoint_id}/rate-tier
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `general` | `object` | — | Update the general bucket. Send only the fields you want to change. |
| `method_overrides` |  | — | "> Full replace of the method-overrides list. To add one without removing others, fetch first, mutate, send back. |
| `streaming` | `object` | — | Update streaming connection caps. |
```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/rate-tier \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X PATCH -d '{
    "general": { "requests_per_window": 3000 },
    "streaming": { "max_concurrent_grpc_subs": 25 }
  }'
```

The change takes effect within seconds across the edge fleet.

{% hint style="warning" %}
You can't raise limits beyond what your endpoint's ceiling allows. Trying to set `requests_per_window` above the ceiling returns `403` with the max value in the error body. Higher limits require a plan upgrade or dedicated.
{% endhint %}

## Reset to plan defaults

```text
DELETE /v1/endpoints/{endpoint_id}/rate-tier/overrides
```

Removes all method-specific overrides and resets `general` and `streaming` to plan defaults.

## Bursting

Some endpoints include short-burst allowance above the steady-state limit. The `general` object then includes a `burst` block:

```json
{
  "general": {
    "requests_per_window": 3000,
    "window_seconds": 10,
    "concurrent_requests": 200,
    "burst": {
      "requests_per_burst": 6000,
      "burst_window_seconds": 1,
      "burst_cooldown_seconds": 30
    }
  }
}
```

Burst means you can briefly hit double the steady-state for one second, then must drop back below steady-state for the cooldown window.

## Read live counts

The Account Management API exposes the *configuration*. The actual per-second counters are on the endpoint itself: `https://<your-endpoint>.mainnet.rpcpool.com/<token>/ratelimits` plus the `X-Ratelimit-*` headers on every RPC response. See [Rate and connection limits](../get-started/rate-and-connection-limits.md) for the runtime view.

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-gauge">:gauge:</i> <strong>Rate and connection limits</strong></td><td>Per-endpoint and method rate limits, plus streaming connection caps.</td><td><a href="../get-started/rate-and-connection-limits.md">../get-started/rate-and-connection-limits.md</a></td></tr><tr><td><i class="fa-credit-card">:credit-card:</i> <strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="../get-started/plans-and-billing.md">../get-started/plans-and-billing.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
