# Tokens

Issue, list, rotate, and revoke endpoint tokens via the Account Management API.

Each Triton endpoint has its own set of tokens. The Tokens API is for programmatic issue / rotate / revoke -- typically wired into a scheduled rotation job or your CI's secret-rolling flow.

Resource path: `/v1/endpoints/{endpoint_id}/tokens`

## List tokens

```text
GET /v1/endpoints/{endpoint_id}/tokens
```

Returns metadata about each token -- not the secret value (that's only shown at creation).

```json
{
  "data": [
    {
      "id": "tok_abc",
      "label": "default",
      "created_at": "2026-02-12T11:24:08Z",
      "last_used_at": "2026-05-03T14:32:09Z",
      "status": "active",
      "ip_count_24h": 3
    },
    {
      "id": "tok_def",
      "label": "trading-bot-prod",
      "created_at": "2026-04-30T09:00:00Z",
      "last_used_at": "2026-05-03T14:32:11Z",
      "status": "active",
      "ip_count_24h": 1
    }
  ]
}
```

## Issue a new token

```text
POST /v1/endpoints/{endpoint_id}/tokens
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | `string` | Yes | Human-readable name. Visible in usage logs to attribute traffic. |
| `expires_at` | `string` | — | ISO 8601 timestamp. If set, token auto-revokes at this time. Use for time-boxed CI pipelines or contractor access. |
```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/tokens \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{ "label": "trading-bot-prod" }'
```

```json
{
  "id": "tok_def",
  "label": "trading-bot-prod",
  "value": "8f3a2c... (full secret, displayed once)",
  "created_at": "2026-05-03T14:35:00Z",
  "expires_at": null,
  "status": "active"
}
```

{% hint style="warning" %}
The `value` field is **only** in the create response. Store it in your secret manager immediately. There's no recovery -- if it's lost, revoke and issue a new one.
{% endhint %}

## Rotate a token

The recommended pattern: issue a fresh token, deploy services with the new value, revoke the old one. The API has a built-in helper:

```text
POST /v1/endpoints/{endpoint_id}/tokens/{id}/rotate
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `grace_period_hours` | `number` | — | How long the old token stays valid after rotation. Default 24 hours. Set to 0 for instant cutover (only do this if you can deploy synchronously). |
```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/tokens/tok_abc/rotate \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{ "grace_period_hours": 24 }'
```

Returns the **new** token value. The old one is auto-revoked after the grace period.

## Revoke a token

```text
DELETE /v1/endpoints/{endpoint_id}/tokens/{id}
```

Effective within seconds across the edge fleet. Used for: leaked tokens, departing employees, deprovisioning a service.

```bash
curl https://api.triton.one/v1/endpoints/ep_abc123/tokens/tok_def \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -X DELETE
```

## Limits

| Limit | Default |
|---|---|
| Tokens per endpoint | 10 |
| Token rotations per endpoint per day | 50 |

Higher limits available on dedicated. Talk to support if you have legitimate per-tenant token use cases (per-customer scoped tokens).

## Best practices

- **One token per service**, not one shared. Easier to attribute traffic in logs and rotate one without touching the others.
- **Set `expires_at` on time-boxed access** (CI, contractors).
- **Use the rotate endpoint, not delete-then-create** -- it gives you the grace period for free.
- **Reflect rotations in your secret store as part of the same scheduled job**. If your job rotates the Triton token but doesn't update Vault, your service goes down at the grace-period end.

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-shield">:shield:</i> <strong>Auth and security</strong></td><td>Endpoint, token, and spend security. What Triton handles and what you configure.</td><td><a href="../get-started/authentication.md">../get-started/authentication.md</a></td></tr><tr><td><i class="fa-link">:link:</i> <strong>Endpoints</strong></td><td>Provision, list, configure, and delete endpoints.</td><td><a href="endpoints.md">endpoints.md</a></td></tr></tbody></table>
