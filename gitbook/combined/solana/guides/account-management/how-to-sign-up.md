# How to sign up

Step by step from zero to a Triton endpoint. Self-serve via the customer portal, $125 minimum deposit, no card required.

{% stepper %}
{% step %}
#### Open the customer portal

Go to [customers.triton.one/users/sign-up](https://customers.triton.one/users/sign-up). Sign up with email, GitHub, or Google.
{% endstep %}
{% step %}
#### Verify your email

Click the link in the verification email. The portal will open to your dashboard.
{% endstep %}
{% step %}
#### Top up the $125 minimum

Open Billing, then Buy credits. Pay in stablecoins (USDC, USDT, DAI) via Wallet Connect or any external wallet/exchange. The deposit is prepaid, non-refundable, and valid for 12 months. There is no free trial -- the deposit replaces it.

For card or wire payment, switch to [invoiced billing](../../documentation/get-started/plans-and-billing.md) -- contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).
{% endstep %}
{% step %}
#### Create your first endpoint

Click **Create endpoint**, pick **Solana mainnet** (or devnet for testing), and choose a region. The portal returns:

- **Endpoint URL** -- `<your-endpoint>.mainnet.rpcpool.com`
- **Secret token** -- a long random string

Keep the token server-side. For browser apps, set up an [origin allowlist](../../documentation/get-started/auth-and-security.md) instead of using the token.
{% endstep %}
{% step %}
#### Send your first request

Follow the [Quickstart](../../documentation/get-started/quickstart.md) to call `getSlot` and confirm the endpoint is live. About five minutes end to end.
{% endstep %}
{% endstepper %}

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Quickstart</strong></td><td>Sign up, deposit, get an endpoint, send your first request.</td><td><a href="../../documentation/get-started/quickstart.md">../../documentation/get-started/quickstart.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/rocket.svg">rocket</a></td></tr><tr><td><strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="../../documentation/get-started/plans-and-billing.md">../../documentation/get-started/plans-and-billing.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/credit-card.svg">credit-card</a></td></tr><tr><td><strong>Auth and security</strong></td><td>Endpoint, token, and spend security. What Triton handles and what you configure.</td><td><a href="../../documentation/get-started/auth-and-security.md">../../documentation/get-started/auth-and-security.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/shield.svg">shield</a></td></tr><tr><td><strong>Account management</strong></td><td>Customer dashboard tour: endpoints, billing, team, and support.</td><td><a href="../../documentation/get-started/platform-overview.md">../../documentation/get-started/platform-overview.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/user-cog.svg">user-cog</a></td></tr></tbody></table>
---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
