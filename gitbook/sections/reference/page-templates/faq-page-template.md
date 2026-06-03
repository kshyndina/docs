# FAQ page template

Reference layout for a FAQ page. Grouped by topic, accordion per question, code examples inline where useful.

> **What this is.** A template for FAQ pages -- the Solana FAQs landing, per-product FAQs, billing FAQs, etc. Replace placeholder copy and remove comment blocks before shipping.

## When to use this template

- The questions are **real** ones support has answered repeatedly. Don't write FAQs from imagination.
- Questions group naturally into 2-5 topics. If you only have 3 questions, those should live on the relevant product/guide page, not on a FAQ.
- Use one accordion per question. No long pages of plain headings.

---

## Solana FAQs

> Title is the topic + "FAQs". Subtitle gives the reader a sense of what's covered and what's not. Keep it short.

The most common questions developers hit when shipping on Triton's Solana infrastructure. If your question isn't here, the [customer dashboard chat](https://customers.triton.one) goes straight to engineering.

> One paragraph orienting the reader. What's covered, what isn't, where to ask if their question is missing.

This page covers connection setup, errors, performance, and billing. For walkthroughs, see [Guides](/solana-guides). For exact endpoint behaviour, see the [API reference](/solana-api).

---

## Connection and setup

> H2 per topic group. Then `` containing one `
<details>
<summary>Details</summary>

` per question.

  <Accordion title="Where do I get my endpoint URL and token?">
    Both come from the [customer dashboard](https://customers.triton.one). Sign up, deposit the {`$`}125 minimum, click **Create endpoint**, pick **Solana mainnet** (or devnet for testing), and the portal returns:

    - **Endpoint URL** -- `<your-endpoint>.mainnet.rpcpool.com`
    - **Secret token** -- a long random string

    Full walkthrough: [Set up your account](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/platform-overview).

</details>

<details>
<summary>Can I use the token client-side, in browser code?</summary>

No. The token is a server-side secret. For browser apps, set up an **origin allowlist** in the dashboard so requests are authorised by the page origin, not the token. See [Auth and security](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security).

</details>

<details>
<summary>Does Triton support devnet and testnet?</summary>

Mainnet and devnet are available out of the box. Devnet is free for development and integration tests. Testnet is available on request -- contact sales.

</details>

## Errors

> Cross-link to the central error-handling guide. The FAQ is the "what does this mean and what do I do" version of the same content.

<details>
<summary>I'm getting 401 Unauthorized</summary>

Three causes, in order of likelihood:

1. The token is expired or rotated. Check the dashboard.
2. The request origin isn't on the allowlist. See [Auth and security](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/auth-and-security).
3. The token is being passed in a header that isn't `Authorization: Bearer <token>` -- check your client.

Full debug flow: [Error handling -- RPC](/solana-guides/error-handling/rpc).

</details>

<details>
<summary>Bursty workload triggers 429 Too Many Requests</summary>

Standard tier shares a global rate limit. Two routes:

- **Smooth the burst** -- batch with `getMultipleAccounts`, cache for a few hundred milliseconds, exponential backoff on retry.
- **Move to dedicated** -- isolated bandwidth, no shared limit. See the [pricing calculator](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/plans-and-billing).

</details>

<details>
<summary>gRPC stream returns 403</summary>

The token is correct but the **gRPC scope** isn't enabled for the endpoint. Open the dashboard, find the endpoint, and toggle **Streaming**. Detail: [Error handling -- streaming](/solana-guides/error-handling/streaming).

</details>

## Performance

<details>
<summary>What's the median read latency?</summary>

Median Triton response time, closest GeoDNS region: **~12 ms** for `getBalance` and `getAccountInfo`. End-to-end will depend on your client's distance from the closest region; the dashboard shows your live region.

</details>

<details>
<summary>Why is `getProgramAccounts` slow at scale?</summary>

The native Solana RPC scans the validator's account index linearly. For programs with >100k accounts that's tens of seconds. Use [Steamboat](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/steamboat-indexed-accounts) for a hot index keyed exactly on the lookup pattern your app uses; reads return in milliseconds.

</details>

## Billing

<details>
<summary>Is the {`$`}125 deposit refundable?</summary>

No. The deposit is prepaid, non-refundable, and valid for 12 months. It burns down at the per-service rates as you use the platform; unused balance carries over until the year is up.

</details>

<details>
<summary>What does 'overage billed at the base rate' mean?</summary>

If usage exceeds the credit you've deposited, the next requests still go through and accrue at the same per-call / per-GB rate. No surge pricing, no different overage tier. Top up at any time.

</details>

<details>
<summary>Can I move from PAYG to dedicated mid-month?</summary>

Yes. Dedicated nodes are billed monthly per node. Switching keeps your endpoint URL and tokens; usage from the day of switch is on the dedicated rate.

</details>

---

## Still have questions?

> Always end with a routed escape. Don't make the reader hunt.

{% content-ref url="https://customers.triton.one" %}
[Customer dashboard](https://customers.triton.one)
{% endcontent-ref %}

{% content-ref url="https://triton.one/contact" %}
[Sales questions](https://triton.one/contact)
{% endcontent-ref %}

---

---

Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  
Sales questions? [Contact sales](https://triton.one/contact).  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
