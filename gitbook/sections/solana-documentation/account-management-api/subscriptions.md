# Subscriptions

Manage subscriptions, attach subscription types, and read billing configuration via the Account Management API.

The Subscriptions resource describes which products your organisation has access to (Solana, Pyth, SUI, Monad) and which add-ons (DAS, Hydrant, Steamboat). The API is read + minor writes; full plan changes go through the portal or your account manager.

Resource path: `/v1/subscriptions`

## What's a subscription

A subscription couples your organisation to a [subscription type](subscription-types.md). One organisation typically has one base plan (PAYG / committed) plus zero or more add-ons (DAS, Hydrant, Steamboat).

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#F2EDF6','primaryBorderColor':'#7A4BA0','primaryTextColor':'#171717','lineColor':'#956FB3','secondaryColor':'#E4DBEC','tertiaryColor':'#D7C9E3','noteBkgColor':'#FFC845','noteTextColor':'#171717','actorBkg':'#F2EDF6','actorBorder':'#7A4BA0','actorTextColor':'#171717','signalColor':'#492D60','labelBoxBkgColor':'#7A4BA0','labelTextColor':'#F7F7F7','edgeLabelBackground':'transparent'}}}%%
flowchart LR
    O[Organisation] --> SB[Base subscription<br/>e.g. Committed Solana]
    O --> SA[Add-on: DAS API]
    O --> SH[Add-on: Hydrant]
    O --> SS[Add-on: Steamboat]
```

## List active subscriptions

```text
GET /v1/subscriptions
```

```bash
curl https://api.triton.one/v1/subscriptions \
  -H "Authorization: Bearer $TRITON_API_TOKEN"
```

```json
{
  "data": [
    {
      "id": "sub_base_abc",
      "type_id": "type_committed_solana_500",
      "status": "active",
      "started_at": "2026-02-01T00:00:00Z",
      "renewal_at": "2026-06-01T00:00:00Z",
      "monthly_credits": 500000
    },
    {
      "id": "sub_addon_das",
      "type_id": "type_addon_das",
      "status": "active",
      "started_at": "2026-03-15T00:00:00Z",
      "renewal_at": null
    }
  ]
}
```

## Attach an add-on

```text
POST /v1/subscriptions
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type_id` | `string` | Yes | Subscription type ID. List available types via `GET /v1/subscription-types`. |
| `metadata` | `object` | — | Optional key-value notes (cost-centre, project name). |
```bash
curl https://api.triton.one/v1/subscriptions \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{ "type_id": "type_addon_hydrant" }'
```

Add-ons activate immediately. Billing prorates from the activation timestamp.

## Detach an add-on

```text
DELETE /v1/subscriptions/{id}
```

```bash
curl https://api.triton.one/v1/subscriptions/sub_addon_das \
  -H "Authorization: Bearer $TRITON_API_TOKEN" \
  -X DELETE
```

Add-on stops billing at the next billing cycle (no proration of the partial month). The feature stays active until cycle end.

## Change base plan

Base plan changes (PAYG -> committed, sizing up / down) go through the portal or via your account manager. The API only supports add-on attach / detach.

[Reach out to support](https://customers.triton.one) for plan changes.

## What's next

{% content-ref url="subscription-types.md" %}
[Subscription types](subscription-types.md)
{% endcontent-ref %}

{% content-ref url="../get-started/plans-and-billing.md" %}
[Plans and billing](../get-started/plans-and-billing.md)
{% endcontent-ref %}

---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
