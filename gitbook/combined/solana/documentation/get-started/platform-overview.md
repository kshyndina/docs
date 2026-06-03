# Platform overview

Triton customer portal is where you get your endpoint and token, monitor usage, and top up the balance. This page is a quick tour so you know where to find everything.

{% hint style="warning" %}
**Work in progress.** This page is being reviewed -- don't reference it yet, copy isn't final.
{% endhint %}

## What's in the portal

**Endpoints and tokens**

Monitor and configure every endpoint. Manage tokens, origin allowlists, and IP allowlists per endpoint.

**Usage**

Live RPS, bandwidth, and method latency. Daily billing by product and endpoint.

**Billing and top-ups**

Deposits, balance, payment methods, and how usage builds your bill.

**Members**

Invite teammates and colleagues to your organisation.

**Security and profile**

Your name, email, password, and account preferences.

**Support**

Your main channel for direct chat with Triton engineering.

## Common tasks

Here's where to go in the dashboard for the things you'll do most often. What you can do depends on your role -- new members default to **Standard**, which covers almost everything. Expand a role below to see what it includes.

<details>
<summary>Standard (default)</summary>

Read-mostly access plus self-serve actions: view usage and cost, top up credits, set low-balance notifications, contact support, add domains to the origin allowlist, invite teammates.

</details>

<details>
<summary>Operator</summary>

Everything Standard does, plus provisioning new endpoints and rotating tokens.

Need Operator? Ask in the dashboard chat -- support can upgrade you.

</details>

<details>
<summary>Admin</summary>

Organisation owner. Full access to billing, endpoints, members, and dangerous actions like deleting an endpoint or transferring ownership. Contact support to add or transfer the Admin role.

</details>

| Task | Where |
| --- | --- |
| See live usage and cost | **v3 Billing** tab on the dashboard |
| Find a token | Click the subscription, then the endpoint name -- token shows under **Auth** |
| Top up credits | **Billing** &rarr; **Buy credits** |
| Set low-balance notifications | **Billing** &rarr; toggle alerts &rarr; set threshold |
| Add a domain to the origin allowlist | Endpoint &rarr; **Auth** &rarr; **Allowed origins** &rarr; `+` |
| Invite a teammate | **Members** &rarr; **Invite** |
| Open a support ticket | Chat icon, bottom right of any dashboard page |
| Provision a new endpoint | **Endpoints** &rarr; **New** *(Operator only -- Standard contacts support)* |
| Rotate a token | Endpoint &rarr; **Auth** &rarr; **Rotate token** *(Operator only -- Standard contacts support)* |
| Raise a rate limit | 📩 Contact support |
| Stake-weighted QoS for sending transactions | 📩 Contact support |

## Walkthroughs

Short clips to walk you through the most common tasks, from sign-up onward.

  <video autoPlay muted loop playsInline >
    <source src="../../../images/sign-up.mp4" type="video/mp4" />
  </video>

### Sign up

    1. Go to [customers.triton.one/users/sign-up](https://customers.triton.one/users/sign-up) with your work email
    2. Click the verification link in your inbox
    3. Name your organisation (the billing root for everything)
    4. Provision your first endpoint -- pick **Solana mainnet** and your closest region

### Add a teammate

    1. Open **Members** in the sidebar
    2. Click **Invite**
    3. Enter the teammate's email
    4. Click **Send** -- they get a one-click join link

  <video autoPlay muted loop playsInline >
    <source src="../../../images/add-user.mp4" type="video/mp4" />
  </video>

  <video autoPlay muted loop playsInline >
    <source src="../../../images/add-allow-origin.mp4" type="video/mp4" />
  </video>

### Add a domain to the origin allowlist

    1. Click into the mainnet subscription
    2. Click the endpoint name to open its settings
    3. Under **Allowed origins**, hit `+`
    4. Add the domain and save -- all subdomains are allowed automatically

### View usage

    1. Open the **v3 Billing** tab
    2. Review the per-product totals (requests and bandwidth)
    3. Drill into per-endpoint breakdowns below
    4. Click **Export CSV** in the top-right to download

  <video autoPlay muted loop playsInline >
    <source src="../../../images/view-usage.mp4" type="video/mp4" />
  </video>

  <video autoPlay muted loop playsInline >
    <source src="../../../images/top-up.mp4" type="video/mp4" />
  </video>

### Top up credits

    1. Open **Billing** in the sidebar
    2. Click **Buy credits**
    3. Pay in stablecoins via Wallet Connect, or transfer from any external wallet
    4. Card or wire? Switch to invoiced billing -- contact support

### Set up low-balance notifications

    1. Open **Billing** in the sidebar
    2. Toggle alerts on
    3. Set the threshold (for example, $10)
    4. Save -- every user on the account gets notified when balance hits that amount

  <video autoPlay muted loop playsInline >
    <source src="../../../images/add-notifications.mp4" type="video/mp4" />
  </video>

  <video autoPlay muted loop playsInline >
    <source src="../../../images/contact-support.mp4" type="video/mp4" />
  </video>

### Contact support

    1. Click the chat icon in the bottom right of any dashboard page
    2. Describe what's happening
    3. Include your endpoint URL and the timestamp of the issue
    4. Your message goes straight to engineering -- not a tier-1 queue

## What's next

{% content-ref url="quickstart.md" %}
[Quickstart](quickstart.md)
{% endcontent-ref %}

{% content-ref url="../streaming-data/overview.md" %}
[Streaming overview](../streaming-data/overview.md)
{% endcontent-ref %}

{% content-ref url="../streaming-data/quickstart.md" %}
[Streaming quickstart](../streaming-data/quickstart.md)
{% endcontent-ref %}

{% content-ref url="../reading-state/overview.md" %}
[Reading state overview](../reading-state/overview.md)
{% endcontent-ref %}

---

---

Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  
Sales questions? [Contact sales](https://triton.one/contact).  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
