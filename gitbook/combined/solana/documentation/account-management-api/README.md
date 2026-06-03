# Overview

Triton's REST API for programmatically managing organisations, members, endpoints, tokens, and rate tiers.

Everything you can do in the portal -- create endpoints, rotate tokens, manage origin allowlists, change rate limits, invite teammates -- is also available as a REST API. Use it for IaC, CI pipelines, automated rotation, and provisioning per-customer endpoints in your own product.

## When to use the API

| Use case | Why API beats portal |
|---|---|
| **Per-tenant endpoints** | If your product gives each of *your* customers a Solana endpoint, the API lets you provision and revoke in code. |
| **Scheduled token rotation** | Cron job hits the API every 90 days; no human in the loop. |
| **Infrastructure as Code** | Terraform / Pulumi / OpenTofu pattern: declare endpoints in code, the API applies. |
| **CI gates** | A failing CI job revokes its temporary endpoint. |
| **Disaster recovery** | Re-provision an environment in seconds from a saved manifest. |

## Where to start

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-id-card">:id-card:</i> <strong>Auth and headers</strong></td><td>Bearer tokens, organisation context, and the headers every call needs.</td><td><a href="auth-headers.md">auth-headers.md</a></td></tr><tr><td><i class="fa-user">:user:</i> <strong>Accounts</strong></td><td>List, create, rotate, and revoke organisation members.</td><td><a href="accounts.md">accounts.md</a></td></tr><tr><td><i class="fa-link">:link:</i> <strong>Endpoints</strong></td><td>Provision, list, configure, and delete endpoints.</td><td><a href="endpoints.md">endpoints.md</a></td></tr><tr><td><i class="fa-lock">:lock:</i> <strong>Tokens</strong></td><td>Issue, list, rotate, and revoke endpoint tokens.</td><td><a href="tokens.md">tokens.md</a></td></tr></tbody></table>
## Resource model

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#F2EDF6','primaryBorderColor':'#7A4BA0','primaryTextColor':'#171717','lineColor':'#956FB3','secondaryColor':'#E4DBEC','tertiaryColor':'#D7C9E3','noteBkgColor':'#FFC845','noteTextColor':'#171717','actorBkg':'#F2EDF6','actorBorder':'#7A4BA0','actorTextColor':'#171717','signalColor':'#492D60','labelBoxBkgColor':'#7A4BA0','labelTextColor':'#F7F7F7','edgeLabelBackground':'transparent'}}}%%
flowchart TB
    O[Organisation] --> M[Members]
    O --> E[Endpoints]
    E --> T[Tokens]
    E --> R[Rate tiers]
    E --> S[Subscriptions]
    S --> ST[Subscription types]
    E --> AWL[Address watch lists]
```

- **Members** belong to the organisation.
- **Endpoints** belong to the organisation; everything below belongs to an endpoint.
- **Tokens** authenticate RPC requests against an endpoint.
- **Rate tiers** describe the limits on an endpoint (configurable on dedicated; read-only on shared by default).
- **Subscriptions** + **subscription types** describe what plans are attached.
- **Address watch lists** are server-side filters for streaming endpoints.

## Quickstart: list your endpoints

{% tabs %}
{% tab title="curl" %}
```bash
curl https://api.triton.one/v1/endpoints \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Accept: application/json"
```
{% endtab %}
{% tab title="fetch" %}
```javascript
const res = await fetch('https://api.triton.one/v1/endpoints', {
  headers: {
    'Authorization': `Bearer ${process.env.TRITON_API_TOKEN}`,
    'Accept': 'application/json'
  }
});
const json = await res.json();
console.log(json);
```
{% endtab %}
{% tab title="python" %}
```python

r = requests.get(
    'https://api.triton.one/v1/endpoints',
    headers={
        'Authorization': f'Bearer {os.environ["TRITON_API_TOKEN"]}',
        'Accept': 'application/json',
    }
)
print(r.json())
```
{% endtab %}
{% endtabs %}

The API returns JSON with one entry per endpoint: ID, region, plan, current usage, list of tokens, and the rate-tier configuration.

## Authentication

Bearer tokens, scoped to an organisation. Issue from **Members → API tokens → New** in the portal. Treat them like a password; rotate quarterly.

```text
Authorization: Bearer triton_pat_<random>
```

See [Auth and headers](auth-headers.md) for the full header set including organisation switching.

## Rate limits on the API itself

The Account Management API is rate-limited at **60 requests per minute per token**. Mutating calls (POST / PATCH / DELETE) count the same as reads. If you hit the limit you get `429 Too Many Requests` and an `X-Ratelimit-Reset` header telling you how many seconds until the window resets.

{% hint style="info" %}
This is separate from your *RPC* rate limits. The API token authenticates portal-style management calls, not Solana RPC traffic.
{% endhint %}

## Errors

| Status | Meaning |
|---|---|
| `200 OK` / `201 Created` | Success |
| `400 Bad Request` | Malformed body or missing required field; error message identifies the field |
| `401 Unauthorized` | Token missing, expired, or revoked |
| `403 Forbidden` | Token valid but lacks the role required for this action (e.g. viewer trying to create an endpoint) |
| `404 Not Found` | Resource doesn't exist or isn't visible to your organisation |
| `409 Conflict` | Duplicate (e.g. endpoint name already taken) |
| `429 Too Many Requests` | API rate limit hit; back off and retry |
| `5xx` | Server-side; retry with backoff. Persistent 5xx -> [contact support](https://customers.triton.one) |

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-id-card">:id-card:</i> <strong>Auth and headers</strong></td><td>Bearer tokens, organisation context, and the headers every call needs.</td><td><a href="auth-headers.md">auth-headers.md</a></td></tr><tr><td><i class="fa-link">:link:</i> <strong>Endpoints</strong></td><td>Provision, list, configure, and delete endpoints.</td><td><a href="endpoints.md">endpoints.md</a></td></tr></tbody></table>
---
<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
<i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
<i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)  
<i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
<i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
