# My account

Questions about your Triton account, sign-in, allowed origins, billing, top-ups, invoices, and cancellation.

## Sign-in and getting help

Logging in, recovering your username, and where to find support when something breaks.

<details>
<summary>Where can I get help with my Triton account?</summary>

You can contact us anytime through the support channel on your [customer dashboard](https://customers.triton.one).

</details>

<details>
<summary>Why can't I sign in with Google?</summary>

Google single sign-on is reserved for Triton One employees and isn't available on customer accounts. Sign in with your Triton username and password instead.

</details>

<details>
<summary>Why won't my email work to sign in?</summary>

The login form takes your username, not your email address. If you've forgotten your username, click **Forgot your username** at the bottom of the form, enter your email, and we'll send it to you.

</details>

## Account security

Configuring allowed origins on your endpoints, and what to do if an API key leaks.

<details>
<summary>How can I add domains to the allowed origins?</summary>

In your customer dashboard, click into the mainnet subscription. On the right, click the endpoint name to open its settings. Under **Allowed origins**, hit `+` to add a new one and save. All subdomains are automatically allowed.

</details>

<details>
<summary>I exposed my API key. What should I do?</summary>

Please contact us ASAP through the support channel on your customer dashboard. We will urgently provide you with a new one and decommission the exposed key.

</details>

## Billing and usage

Topping up, low-balance alerts, reading usage, and gRPC drawdown timing.

<details>
<summary>How do I top up my balance?</summary>

Open your customer dashboard, go to **Billing**, and click **Buy credits**. You can pay in stablecoins via:

- **Wallet Connect.** Connect your wallet and pay with any supported token.
- **Transfer from anywhere.** Send stablecoins from any external wallet or exchange.

If you'd rather pay by card or wire, switch to invoiced billing.

</details>

<details>
<summary>Can I set up low-balance notifications?</summary>

Yes. Open your customer dashboard, go to **Billing**, toggle alerts on, and set a threshold (for example, $10). When your balance hits that amount, every user on the account gets a notification.

</details>

<details>
<summary>Where can I see my usage?</summary>

In your customer dashboard, open the **v3 Billing** tab. You'll see total requests and GB used (the two dimensions you're billed on), plus a per-service breakdown table below with product-level detail. To export it, click **Export CSV** in the top-right corner.

</details>

<details>
<summary>Why did my gRPC bill spike all at once?</summary>

gRPC streaming is metered when the connection closes. If you hold a stream open for several hours or a day, the full bandwidth charge is applied to your account once it disconnects.

Also, usage data refreshes every \~4 hours, so you can expect a lag between actual traffic and what's reflected in the dashboard.

</details>

## Invoicing and payments

Invoice cycles, accepted payment methods, and how to cancel.

<details>
<summary>When will I receive my invoice, and what period does it cover?</summary>

If you're on a pay-as-you-go plan, you can top up your account in the [customer dashboard](https://customers.triton.one) any time.

If you receive invoices, we send two kinds:

- **Invoices for dedicated nodes and expected monthly use of shared RPC** are sent on the first day of each month as prepayment for the upcoming month's services.
- **Any overages** are invoiced early in the following month, covering the previous month's usage.

We're working on getting both of these onto a single monthly invoice, but for right now, you could receive two.

</details>

<details>
<summary>Is there a due date for paying the invoice?</summary>

Yes, all invoices are due within 7 days of the issue date.

</details>

<details>
<summary>What payment methods do you support?</summary>

For invoiced customers, we accept:

    - USDC (SPL on Solana, ERC-20 on Ethereum, Tron, Polygon)
    - Payments through hel.io (USDC)
    - Credit cards via Coinflow
    - Wire transfers in GBP and USD

    For pay-as-you-go, we accept stablecoins only.

</details>

<details>
<summary>How do I cancel my subscription?</summary>

For pay-as-you-go customers, you can just stop using the service. Your prepaid balance stays valid for one year and expires after that. There's nothing to cancel.

    For invoiced customers, give one calendar month's notice through the support channel in your [customer dashboard](https://customers.triton.one).

</details>
