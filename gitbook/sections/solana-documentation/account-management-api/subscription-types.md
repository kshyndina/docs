# Subscription types

The catalogue of subscription plans and add-ons attachable to your organisation.

`/v1/subscription-types` is the read-only catalogue of plans and add-ons Triton offers. Use it to populate your billing UI or to programmatically pick what to attach via [Subscriptions](subscriptions.md).

Resource path: `/v1/subscription-types`

## List all types

```text
GET /v1/subscription-types
```

Filter via `?category=base` or `?category=addon` to narrow the list.

```bash
curl 'https://api.triton.one/v1/subscription-types?category=addon' \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

```json
{
  "data": [
    {
      "id": "type_addon_das",
      "category": "addon",
      "name": "DAS API",
      "description": "Digital Asset Standard API for NFTs, compressed assets",
      "pricing": {
        "model": "per_request",
        "rate_usd_per_million": 50
      },
      "monthly_minimum_usd": 0
    },
    {
      "id": "type_addon_hydrant",
      "category": "addon",
      "name": "Hydrant historical archive",
      "description": "Full Solana history beyond the recent ledger",
      "pricing": {
        "model": "per_request",
        "rate_usd_per_million": 10
      },
      "monthly_minimum_usd": 10
    }
  ]
}
```

## Get a specific type

```text
GET /v1/subscription-types/{id}
```

Returns full pricing details including any tiered breakdowns (e.g. committed plans with a credit pool).

## Categories

| Category | What it is |
|---|---|
| `base` | Mutually exclusive root plan: PAYG, Committed (sized), Dedicated (sized) |
| `addon` | Stackable: DAS, Hydrant, Steamboat, SWQoS access, custom regions |

An organisation has exactly one `base` and zero-or-more `addon` subscriptions at any time.

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-rss">:rss:</i> <strong>Subscriptions</strong></td><td>Attach plans, add-ons, or watch lists to the organisation.</td><td><a href="subscriptions.md">subscriptions.md</a></td></tr><tr><td><i class="fa-credit-card">:credit-card:</i> <strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="../get-started/plans-and-billing.md">../get-started/plans-and-billing.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
