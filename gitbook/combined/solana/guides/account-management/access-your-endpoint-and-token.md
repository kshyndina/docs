# Access your endpoint and token

Where to find the endpoint URL and secret token in your customer dashboard, and how to use each one in backend vs browser code.

Every Triton subscription ships with one or more endpoints. Each endpoint has a **URL** and a **secret token**. You'll use both for every request.

## Find them in the dashboard

1. Open the [customer dashboard](https://customers.triton.one) and sign in.
2. In the sidebar, click **Endpoints** (or pick the endpoint from the dashboard home).
3. The endpoint detail page shows:
   - **Endpoint URL** -- `<your-endpoint>.mainnet.rpcpool.com` (or `.devnet.rpcpool.com` for devnet)
   - **Secret token** -- a long random string. Click **Reveal** to view, **Copy** to copy.

If you don't have an endpoint yet, click **Create endpoint** in the top right, pick **Solana mainnet** (or devnet for testing), and choose a region.

## Use them

The token is appended directly to the endpoint URL for HTTP and WebSocket calls. For gRPC, the token goes in the `x-token` metadata header.

```text Backend (HTTP)
https://<your-endpoint>.mainnet.rpcpool.com/<your-token>
```

```text Backend (WebSocket / Whirligig)
wss://<your-endpoint>.mainnet.rpcpool.com/<your-token>/whirligig
```

```text Backend (gRPC)
endpoint: https://<your-endpoint>.mainnet.rpcpool.com:443
header:   x-token: <your-token>
```

## Browser apps: don't ship the token

Anything visible in DevTools is public. For frontend code, leave the token out of the URL and configure an **origin allowlist** in the dashboard instead. Triton serves requests only from the domains you've whitelisted.

```text Browser (no token)
https://<your-endpoint>.mainnet.rpcpool.com/
```

Setup steps and the full token-leak playbook are in [Auth and security](../../documentation/get-started/auth-and-security.md).

## Rotate or revoke

The dashboard's endpoint page has **Rotate token** (issues a new token, old one becomes invalid immediately) and **Delete endpoint** (revokes everything tied to the endpoint). Use rotation if you suspect a leak; use delete to retire an unused endpoint.

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-rocket">:rocket:</i> <strong>Quickstart</strong></td><td>Sign up, deposit, get an endpoint, send your first request.</td><td><a href="../../documentation/get-started/quickstart.md">../../documentation/get-started/quickstart.md</a></td></tr><tr><td><i class="fa-shield">:shield:</i> <strong>Auth and security</strong></td><td>Endpoint, token, and spend security. What Triton handles and what you configure.</td><td><a href="../../documentation/get-started/auth-and-security.md">../../documentation/get-started/auth-and-security.md</a></td></tr><tr><td><i class="fa-user-plus">:user-plus:</i> <strong>How to sign up</strong></td><td>Step-by-step from clicking signup to a live Triton endpoint.</td><td><a href="how-to-sign-up.md">how-to-sign-up.md</a></td></tr><tr><td><i class="fa-credit-card">:credit-card:</i> <strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="../../documentation/get-started/plans-and-billing.md">../../documentation/get-started/plans-and-billing.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
