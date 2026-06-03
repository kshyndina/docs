# General

Common questions about Triton, our products, plans, payments, and how to start using our services.

## About Triton

What Triton is, what we build, and how Project Yellowstone fits into the stack.

<details>
<summary>What is Triton One?</summary>

Triton is a high-performance infrastructure provider running RPC nodes, private validators, and data streaming systems across Solana, Sui, Monad, and other networks.

It delivers reliable, fast, and feature-rich blockchain infrastructure trusted by developers, validators, and traders that can't afford downtime.

Triton powers everything from real-time trading and market-making to large-scale data indexing and validator operations.

</details>

<details>
<summary>What is Project Yellowstone?</summary>

Project Yellowstone is Triton's suite of high-performance tools and open-source frameworks designed to enhance RPC and data infrastructure for the Solana ecosystem.

It addresses critical infrastructure challenges: real-time data streaming, historical ledger access, ultra-low latency queries, and custom indexing.

Key components:

| Tool | Description |
| --- | --- |
| Dragon's Mouth | Core gRPC streaming engine for Solana. Delivers raw real-time data directly from the validator with ultra-low latency using Protobuf. |
| Whirligig | WebSocket counterpart to Dragon's Mouth -- built for front-end or browser-based apps needing live account and transaction feeds. |
| Fumarole | Persistent streaming layer with automatic redundancy and 4-day caching. Ensures no data loss even if the connection drops. |
| Steamboat | Custom indexing engine that accelerates heavy gPA queries by up to 99%, cutting latency for large programs. |
| Old Faithful | Full-ledger archival service providing access to Solana's complete historical transaction data -- ideal for analytics, re-indexing, and backtesting. |
| Jet | A transaction submission software that lets you add Stake Weight to your transactions to route them through a priority lane during network congestion. |
| Shield | Anti-MEV protection layer integrated with Jet. Allows configurable allow- and block-lists to prevent sandwiching and other frontrunning behaviours. |

</details>

<details>
<summary>What are other products outside of Project Yellowstone?</summary>

Beyond the famous Project Yellowstone, Triton operates additional infrastructure and integrations across multiple networks:

| Service | Description |
| --- | --- |
| Sui & Monad | RPC infrastructure for Mainnet and Testnet. |
| Eclipse & PythNet | RPC infrastructure for Mainnet. |
| Photon | Indexer for ZK compression. |
| Metaplex DAS API | Optimised API for fast access to fungible and non-fungible asset data on Solana. |
| Pyth Hermes | Real-time price feed for financial market data. |
| Jito | Dedicated Jito deployments for bundle simulation and MEV-related infrastructure. |
| Titan Swap API | Swap API for various trading and protocol needs. |
| Cascade Marketplace | A bandwidth marketplace where trusted validators sell SWQoS bandwidth to consumers. |

</details>

## Getting started

How to set up an account, decide on a plan, and add users to your customer dashboard.

<details>
<summary>How can I get started with Triton services? / How do I get an account?</summary>

You can self-onboard at [customers.triton.one](https://customers.triton.one/users/sign-up) in about 2 minutes. For a dedicated gRPC node or other custom requirements, [contact sales](https://triton.one/contact).

</details>

<details>
<summary>How can I decide which service fits my traffic needs best?</summary>

Our docs cover comparisons for [streaming](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/overview), [reading state](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/overview), and [sending transactions](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/overview), so you can match the service to your traffic shape. If you want more tailored guidance, [contact sales](https://triton.one/contact). If you already have an account, contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).

</details>

<details>
<summary>How can I add a user to my Triton customer dashboard?</summary>

Open your [customer dashboard](https://customers.triton.one), scroll to the **Users** section in the main tab, click **Add users**, and invite a teammate by email.

</details>

<details>
<summary>Do you require long-term contracts?</summary>

On pay-as-you-go, there's no commitment beyond your $125 prepaid deposit, which is valid for one year of usage.

    For invoiced customers, standard billing is month-to-month. To cancel, give one calendar month's notice.

</details>

<details>
<summary>Can I change my plan later?</summary>

On Triton's shared infrastructure, there are no plan tiers. Every customer gets the same features, services, and flexible limits regardless of subscription size. So there's nothing to "upgrade" between.

    For pay-as-you-go, you can top up your balance at any time. For invoiced customers, we'll adjust your plan based on actual usage at any point.

</details>

<details>
<summary>Does Triton offer a free trial to test its services?</summary>

We don't run a separate free trial. The $125 pay-as-you-go deposit serves the same purpose: you get a year of testing and running on production infrastructure at standard rates. Sign up at [customers.triton.one](https://customers.triton.one/users/sign-up).

    Trials aren't available on dedicated nodes because the infrastructure runs on custom bare-metal servers with significant upfront cost and multi-month vendor commitments. If you want to evaluate Triton on shared first before moving to dedicated, that path is open by default.

</details>

<details>
<summary>Can I run custom software on Triton's nodes?</summary>

No. We offer managed services, so no one outside the Triton team has access to the infrastructure, and we don't provide SSH access. If you have a dedicated node, we can set up supported add-ons on request.

</details>

## Products and services

Questions about Triton's services beyond Solana RPC.

<details>
<summary>What Pyth oracle products do you offer?</summary>

We provide infrastructure for PythNet RPC and Hermes for streaming price updates. We don't offer benchmarks. For publishers, we offer dedicated RPC to publish onto PythNet and Validators to bolster the Pyth Network.

We work closely with Douro Labs (Pyth Team) to ensure a smooth onboarding and service experience.

</details>

<details>
<summary>How can I access Pyth Hermes?</summary>

To access Hermes, you need to point your endpoint to access Hermes and Pythnet. Make sure your path looks like:

```text
https://<endpoint>.mainnet.pythnet.rpcpool.com/<secret token>/hermes/v2/<rest of the call>
```

The most common mistake is omitting the token, `v2`, or `hermes` parts of the path.

</details>

<details>
<summary>Does Triton have a validator?</summary>

Yes. You can stake directly with our [Private Trusted Validator](https://kate-6.gitbook.io/triton-one-docs/documentation/validator-services/white-label-validators/overview) and earn weekly USDC rewards. The minimum delegation is 2,500 SOL.

    This is built for people or teams with larger delegations who want steady income to cover operating expenses, with white-glove setup for custodians and stake pools.

</details>

---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
