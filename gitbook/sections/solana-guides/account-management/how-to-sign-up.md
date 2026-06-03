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

For card or wire payment, switch to [invoiced billing](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/plans-and-billing) -- contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).
{% endstep %}
{% step %}
#### Create your first endpoint

Click **Create endpoint**, pick **Solana mainnet** (or devnet for testing), and choose a region. The portal returns:

- **Endpoint URL** -- `<your-endpoint>.mainnet.rpcpool.com`
- **Secret token** -- a long random string

Keep the token server-side. For browser apps, set up an [origin allowlist](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security) instead of using the token.
{% endstep %}
{% step %}
#### Send your first request

Follow the [Quickstart](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/quickstart) to call `getSlot` and confirm the endpoint is live. About five minutes end to end.
{% endstep %}
{% endstepper %}

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-rocket">:rocket:</i> <strong>Quickstart</strong></td><td>Sign up, deposit, get an endpoint, send your first request.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/quickstart">https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/quickstart</a></td></tr><tr><td><i class="fa-credit-card">:credit-card:</i> <strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/plans-and-billing">https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/plans-and-billing</a></td></tr><tr><td><i class="fa-shield">:shield:</i> <strong>Auth and security</strong></td><td>Endpoint, token, and spend security. What Triton handles and what you configure.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security">https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security</a></td></tr><tr><td><i class="fa-user-gear">:user-gear:</i> <strong>Account management</strong></td><td>Customer dashboard tour: endpoints, billing, team, and support.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/platform-overview">https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/platform-overview</a></td></tr></tbody></table>
<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
