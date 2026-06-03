---
icon: id-card
---

# Auth & headers

Bearer-token authentication, organisation context, and required headers for the Account Management API.

Every Account Management API call carries the same handful of headers. This page is the reference for what to set and why.

## Required: `Authorization`

Bearer token, issued from **Members → API tokens → New** in the portal.

```text
Authorization: Bearer triton_pat_<random>
```

Tokens are scoped to a single organisation by default. To use one token across multiple orgs, see `X-Triton-Org` below.

{% hint style="warning" %}
Tokens grant the same role you have in the portal. An admin's token can create endpoints; a viewer's token can't. Issue tokens with the **least privilege** they need.
{% endhint %}

## Optional: `X-Triton-Org`

Switch organisation context for a single request. Useful for API tokens that have access to multiple organisations (e.g. partner integrations).

```text
X-Triton-Org: org_abcdef123
```

If omitted, the token's default organisation is used.

## Optional: `Idempotency-Key`

Mutating calls (POST / PATCH / DELETE) accept an `Idempotency-Key` header. Identical keys within 24 hours return the **original** response without re-applying the change. Use UUIDs.

```text
Idempotency-Key: 7c7e3b9a-3a4f-4d8c-9e6b-2c8d4a5f6e7b
```

Strongly recommended for any pipeline that retries on network failures.

## Optional: `Accept`

We default to `application/json`. Set it explicitly for clarity:

```text
Accept: application/json
```

## Pagination

List endpoints (e.g. `/v1/endpoints`, `/v1/members`) use cursor pagination. Pass `limit` and `cursor` query params:

```text
GET /v1/endpoints?limit=50&cursor=eyJpZCI6ImVwX2FiYyJ9
```

The response includes a `pagination.next_cursor` (or `null` if you've reached the end). Default `limit` is 50, max 200.

## Time format

All timestamps are ISO 8601 in UTC:

```text
2026-05-03T14:32:09.221Z
```

Pass timestamps in the same format on input.

## Versioning

The API is versioned in the URL: `/v1/...`. Breaking changes get a new version. The current `v1` is stable; we publish 90-day deprecation notices for any change.

## Example: full request

{% tabs %}
{% tab title="curl" %}
```bash
curl https://api.triton.one/v1/endpoints \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "X-Triton-Org: org_abcdef123" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Accept: application/json" \
  -X POST -d '{
    "name": "trading-mainnet",
    "chain": "solana",
    "network": "mainnet",
    "region": "fra",
    "plan": "committed"
  }'
```
{% endtab %}
{% tab title="fetch" %}
```javascript

const res = await fetch('https://api.triton.one/v1/endpoints', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.TRITON_API_TOKEN}`,
    'X-Triton-Org': 'org_abcdef123',
    'Idempotency-Key': randomUUID(),
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'trading-mainnet',
    chain: 'solana',
    network: 'mainnet',
    region: 'fra',
    plan: 'committed',
  })
});
console.log(await res.json());
```
{% endtab %}
{% endtabs %}

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Endpoints</strong></td><td>Provision, list, configure, and delete endpoints.</td><td><a href="endpoints.md">endpoints.md</a></td></tr><tr><td><strong>Tokens</strong></td><td>Issue, list, rotate, and revoke endpoint tokens.</td><td><a href="tokens.md">tokens.md</a></td></tr></tbody></table>
---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
