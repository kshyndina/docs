# Address watch lists

Manage account watch lists used by gRPC and WebSocket subscriptions via the Account Management API.

Address watch lists let you maintain a named, server-side list of Solana addresses that any of your streaming subscriptions can reference. Update the list once and every active subscription using it picks up the change without reconnecting.

Resource path: `/v1/endpoints/{endpoint_id}/address-watch-lists`

## Why use a watch list

Without watch lists, each gRPC / WebSocket subscription carries its full filter list inline -- typically a `account.account` array of public keys. For a portfolio dashboard that watches 5,000 addresses across many users, this means:

- 5,000 keys repeated in every subscription message.
- Reopening the connection to add a new address.
- Client-side state drift between processes.

With a watch list:

- Subscription references the list by name (`my-portfolio-v1`).
- Add / remove addresses via this API; subscriptions see updates within seconds.
- One source of truth, accessible from every client.

## List watch lists

```text
GET /v1/endpoints/{endpoint_id}/address-watch-lists
```

```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/address-watch-lists \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

## Create a watch list

```text
POST /v1/endpoints/{endpoint_id}/address-watch-lists
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | Yes | Identifier referenced in subscriptions. Lowercase, dashes, alphanumeric. Must be unique within the endpoint. |
| `addresses` |  | — | " required> Solana addresses (base-58). Up to 50,000 per list. |
| `description` | `string` | — | Free-text label for humans. |
```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/address-watch-lists \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{
    "name": "trading-pairs-v1",
    "description": "All Raydium AMM pools for trading-bot-prod",
    "addresses": [
      "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2",
      "..."
    ]
  }'
```

## Get a watch list

```text
GET /v1/endpoints/{endpoint_id}/address-watch-lists/{name}
```

Returns the full address array. For very large lists (>10,000 addresses), use `?cursor=...` to paginate the addresses in 5,000-element chunks.

## Update a watch list

Two patterns: full replace and incremental.

### Full replace

```text
PUT /v1/endpoints/{endpoint_id}/address-watch-lists/{name}
```

Replaces `addresses` wholesale. Use when you have a fresh full list (e.g. nightly recompute).

### Incremental add / remove

```text
POST /v1/endpoints/{endpoint_id}/address-watch-lists/{name}/addresses
DELETE /v1/endpoints/{endpoint_id}/address-watch-lists/{name}/addresses
```

Body: `{ "addresses": [ "...", "..." ] }`. Use when reconciling small deltas (a user added a new portfolio holding).

## Delete a watch list

```text
DELETE /v1/endpoints/{endpoint_id}/address-watch-lists/{name}
```

{% hint style="warning" %}
You can't delete a watch list that's referenced by an active subscription. The error returns `409 Conflict` with the list of subscriptions still using it.
{% endhint %}

## Reference from a subscription

In the gRPC subscribe message, set `accounts.{filter}.account_filter_name` to the list name instead of inlining the address array. See the [Dragon's Mouth quickstart](../streaming-data/dragon-s-mouth-grpc.md) for an example.

## Limits

| Limit | Default |
|---|---|
| Watch lists per endpoint | 100 |
| Addresses per list | 50,000 |
| Total addresses across all lists | 1,000,000 |
| Update rate | 100 mutations / minute / endpoint |

Higher limits available on dedicated -- talk to support.

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-rss">:rss:</i> <strong>Subscriptions</strong></td><td>Attach plans, add-ons, or watch lists to the organisation.</td><td><a href="subscriptions.md">subscriptions.md</a></td></tr><tr><td><i class="fa-radio">:radio:</i> <strong>Dragon's Mouth gRPC</strong></td><td>Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC.</td><td><a href="../streaming-data/dragon-s-mouth-grpc.md">../streaming-data/dragon-s-mouth-grpc.md</a></td></tr></tbody></table>
<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
