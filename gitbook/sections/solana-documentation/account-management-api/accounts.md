# Accounts

List, create, rotate, and revoke organisation members via the Account Management API.

The Accounts resource is the API equivalent of the **Members** tab in the portal. Use it to provision and deprovision team members in code -- typically wired into your HRIS / SSO joiners-and-leavers workflow.

Resource path: `/v1/members`

## List members

```text
GET /v1/members
```

Returns every member of the current organisation with id, email, role, and status.

```bash
curl https://api.triton.one/v1/members \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

```json
{
  "data": [
    {
      "id": "mem_abc123",
      "email": "kate@triton.one",
      "role": "owner",
      "status": "active",
      "created_at": "2026-01-15T09:32:01Z",
      "last_seen_at": "2026-05-03T14:21:45Z"
    },
    {
      "id": "mem_def456",
      "email": "engineer@example.com",
      "role": "admin",
      "status": "invited",
      "created_at": "2026-05-03T10:00:00Z",
      "last_seen_at": null
    }
  ],
  "pagination": { "next_cursor": null }
}
```

## Invite a member

```text
POST /v1/members
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | `string` | Yes | Email address. The invite link is sent here. |
| `role` | `string` | Yes | One of `owner`, `admin`, `viewer`. See [Set up your account](../get-started/platform-overview.md) for capabilities. |
| `message` | `string` | — | Optional custom note included in the invite email (e.g. "joining the trading team"). |
```bash
curl https://api.triton.one/v1/members \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{ "email": "newhire@example.com", "role": "admin" }'
```

The member is created in `status: invited`. They click the email link to activate.

## Change a member's role

```text
PATCH /v1/members/{id}
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `role` | `string` | — | New role. Demotion takes effect immediately; promotion to `owner` requires the caller to already be `owner`. |
```bash
curl https://api.triton.one/v1/members/mem_def456 \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X PATCH -d '{ "role": "viewer" }'
```

## Remove a member

```text
DELETE /v1/members/{id}
```

```bash
curl https://api.triton.one/v1/members/mem_def456 \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -X DELETE
```

The member loses access immediately. Any API tokens they issued are also revoked. If they had pending invites, those are cancelled.

{% hint style="warning" %}
You can't remove the last `owner`. Promote another member to `owner` first, then remove the original.
{% endhint %}

## Resend an invite

```text
POST /v1/members/{id}/resend-invite
```

For members in `status: invited` whose email got lost or expired (invites expire after 7 days).

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Auth and headers</strong></td><td>Bearer tokens, organisation context, and the headers every call needs.</td><td><a href="auth-headers.md">auth-headers.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/id-card.svg">id-card</a></td></tr><tr><td><strong>Endpoints</strong></td><td>Provision, list, configure, and delete endpoints.</td><td><a href="endpoints.md">endpoints.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/link.svg">link</a></td></tr></tbody></table>
---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
