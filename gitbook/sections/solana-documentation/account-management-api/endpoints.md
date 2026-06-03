# Endpoints

Provision, list, configure, and delete endpoints via the Account Management API.

The Endpoints resource is the most-used part of the Account Management API. Provision endpoints in code, configure them, and tear them down -- typically wired into Terraform or a CI pipeline.

Resource path: `/v1/endpoints`

## List endpoints

```text
GET /v1/endpoints
```

Returns every endpoint your token has access to.

```bash
curl https://api.triton.one/v1/endpoints \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

```json
{
  "data": [
    {
      "id": "ep_abc123",
      "name": "trading-mainnet",
      "chain": "solana",
      "network": "mainnet",
      "region": "fra",
      "plan": "committed",
      "status": "active",
      "url_https": "https://app-trading-mainnet.fra.mainnet.rpcpool.com",
      "url_wss": "wss://app-trading-mainnet.fra.mainnet.rpcpool.com",
      "created_at": "2026-02-12T11:24:08Z"
    }
  ],
  "pagination": { "next_cursor": null }
}
```

Filter via `?chain=solana&network=mainnet&status=active`.

## Create an endpoint

```text
POST /v1/endpoints
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | Yes | Human-readable name. Lowercase, dashes, alphanumeric. Must be unique within the organisation. |
| `chain` | `string` | Yes | `solana`, `pyth`, `sui`, or `monad`. |
| `network` | `string` | Yes | `mainnet` or `devnet`. |
| `region` | `string` | Yes | Region code: `fra`, `ams`, `nyc`, `lax`, `sgp`, `tyo`. List supported regions via `GET /v1/regions`. |
| `plan` | `string` | Yes | `payg`, `committed`, or `dedicated`. Dedicated requires a pre-arranged contract -- API will return `403` otherwise. |
| `metadata` | `object` | — | Optional key-value annotations (cost-centre, owning team, environment). |
```bash
curl https://api.triton.one/v1/endpoints \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{
    "name": "indexer-mainnet",
    "chain": "solana",
    "network": "mainnet",
    "region": "fra",
    "plan": "committed",
    "metadata": { "team": "data-platform", "env": "prod" }
  }'
```

The response carries the new endpoint with its URL and a freshly-issued default token. **Save the token immediately** -- it's only displayed at creation.

## Get an endpoint

```text
GET /v1/endpoints/{id}
```

Includes everything the list call returns plus current usage (requests in current window, error rate, balance impact).

## Update an endpoint

```text
PATCH /v1/endpoints/{id}
```

Mutable fields: `name`, `metadata`, and `region` (region change triggers re-provisioning, ~5 minutes downtime). Plan changes -- see [Subscriptions](subscriptions.md).

```bash
curl https://api.triton.one/v1/endpoints/ep_abc123 \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X PATCH -d '{ "name": "trading-mainnet-renamed" }'
```

## Delete an endpoint

```text
DELETE /v1/endpoints/{id}
```

{% hint style="danger" %}
Permanently destroys the endpoint, all its tokens, allowlists, and watch lists. This is **not** reversible. Use a [confirmation header](#delete-confirmation) to avoid accidents.
{% endhint %}

### Delete confirmation

By default, `DELETE` returns `400` unless you add `X-Confirm-Delete: yes` to acknowledge. This is intentional -- single-token credentials in CI scripts often have admin scope, and a stray DELETE is otherwise irreversible.

```bash
curl https://api.triton.one/v1/endpoints/ep_abc123 \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "X-Confirm-Delete: yes" \
  -X DELETE
```

## Sub-resources

| Resource | Path |
|---|---|
| **Tokens** | `/v1/endpoints/{id}/tokens` -- see [Tokens](tokens.md) |
| **Origin allowlist** | `/v1/endpoints/{id}/origin-allowlist` |
| **IP allowlist** | `/v1/endpoints/{id}/ip-allowlist` |
| **Address watch lists** | `/v1/endpoints/{id}/address-watch-lists` -- see [Address watch lists](address-watch-lists.md) |
| **Rate tier** | `/v1/endpoints/{id}/rate-tier` -- see [Rate tiers](rate-tiers.md) |
| **Logs** | `/v1/endpoints/{id}/logs` (last 7 days) |

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-lock">:lock:</i> <strong>Tokens</strong></td><td>Issue, list, rotate, and revoke endpoint tokens.</td><td><a href="tokens.md">tokens.md</a></td></tr><tr><td><i class="fa-sliders">:sliders:</i> <strong>Rate tiers</strong></td><td>Read and configure per-endpoint rate limits programmatically.</td><td><a href="rate-tiers.md">rate-tiers.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
