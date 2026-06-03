# Welcome to Triton

Premium bare-metal Solana infrastructure: reads, streaming, history, trading APIs, and validator services. Built for teams running production workloads.

Here you'll find everything you need to integrate with Triton's Solana infrastructure. If you're new here, start with the Quickstart for a five-minute walk-through, or jump to the common build guides for the path that matches what you're shipping.

![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/solana.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/jupiter.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/phantom.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/orca.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/solflare.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/squads.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/arcium.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/jito-labs.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/marinade.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/binance.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/raydium.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/meteora.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/bonk.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/bitfinex.svg) ![](https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic/logos/birdeye.svg)

## Why teams pick Triton

On Solana, your RPC provider sits in the path of every read your application makes and every transaction it sends. Your app inherits whatever reliability and latency they deliver, setting the ceiling on what you can build.

Depending on the workload, four things matter at different ratios: reliability, low latency, direct engineer support, and consistent capacity. We commit to all four without compromise. Here's how:

- **Premium bare metal across 20\+ PoPs on three continents**, GeoDNS-routed with continuous health checks, load balancing, and automatic failover.
- **Hardware tuned for the workload it serves.** Read clusters, streaming nodes, historical indexers, and TPU clients all run on machines configured for their specific role.
- **Direct engineer support.** The person who replies to your ticket is on the team that built the component you're asking about.
- **Consistent capacity.** Our shared infrastructure is purpose-built to absorb spikes across the cluster without affecting your QoS.

```mermaid actions={false}
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#F2EDF6','primaryBorderColor':'#7A4BA0','primaryTextColor':'#171717','lineColor':'#956FB3','secondaryColor':'#E4DBEC','tertiaryColor':'#D7C9E3','noteBkgColor':'#FFC845','noteTextColor':'#171717','actorBkg':'#F2EDF6','actorBorder':'#7A4BA0','actorTextColor':'#171717','signalColor':'#492D60','labelBoxBkgColor':'#7A4BA0','labelTextColor':'#F7F7F7','edgeLabelBackground':'transparent'}}}%%
sequenceDiagram
    participant You as Your client
    participant Triton
    participant Net as Solana network
    Note over You,Net: Read path
    You->>Triton: getBalance, getAccount, getSlot, ...
    Net->>Triton: sends shreds (every block replayed locally)
    Triton-->>You: response
    Note over You,Net: Send path
    You->>Triton: sendTransaction
    You->>Triton: subscribe to tx status
    Triton->>Net: route to current slot leader TPU<br/>(SWQoS, QUIC)
    Net-->>Triton: leader includes tx in block
    Triton-->>You: signature confirmed
```

## Solana networks we support

Production workloads usually come last. You prototype locally, push to devnet for integration tests, then graduate to mainnet for real traffic. Triton supports every endpoint type on both networks:

- **Mainnet**: production traffic ([learn more](https://solana.com/docs/references/clusters#mainnet-beta))
- **Devnet**: free, for development and integration tests ([learn more](https://solana.com/docs/references/clusters#devnet))

| Network | HTTPS<br />RPC | Web<br />Sockets | Yellowstone<br />gRPC | Fumarole | Steamboat<br />indexed | Hydrant<br />archive |
| --- | :-: | :-: | :-: | :-: | :-: | :-: |
| Solana mainnet | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Solana devnet | ✓ | ✓ | ✓ | ✗ | v1 only | ✓ |

## Triton stack overview

For most workloads, shared is the right answer. Solana's read layer has split into purpose-built components, which makes geographic distribution and per-component scaling the dominant factors for both low latency and spike absorption.

The exception is gRPC streaming. Dragon's Mouth connects directly to Geyser, and a dedicated node gives you full bandwidth and CPU, flat costs on streaming bandwidth, and absolute minimal latency when colocated.

**Shared infrastructure**

**Reading state**

- [Standard RPC](reading-state/standard-rpc.md)

- [Steamboat](reading-state/steamboat-indexed-accounts.md)

- [DAS API](reading-state/metaplex-das-api.md)

- [ZK Compression](reading-state/zk-compression-photon.md)

- [Account Sync](reading-state/account-sync.md)

**Streaming**

- [Dragon's Mouth gRPC](streaming-data/dragon-s-mouth-grpc.md)

- [Deshred transactions](streaming-data/deshred-transactions.md)

- [Whirligig](streaming-data/whirligig-websockets.md)

- [Fumarole](streaming-data/fumarole-persistent-streams.md)

- [Hermes](https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes)

- [Pythnet](https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/overview)

**History**

- [Hydrant](historical-data/hydrant-archive.md)

- [Old Faithful](streaming-data/old-faithful-streams.md)

- [Faithful Streams](streaming-data/old-faithful-streams.md)

**Sending txs**

- [Yellowstone Jet](sending-transactions/yellowstone-jet.md)

- [Priority Fees API](sending-transactions/priority-fees-api.md)

- [Metis](sending-transactions/metis-swap-api.md)

- [Titan Prime](sending-transactions/titan-swap-api.md)

- [Jito Bundles](sending-transactions/jito-bundles.md)

**Other services**

- [Dedicated gRPC node](dedicated-nodes/overview.md)

- [White-label validator](validator-services/white-label-validators/overview.md)

- [Private trusted validator](validator-services/white-label-validators/overview.md)

## For AI agents

Triton's docs are built for humans and AI agents alike. The single-file index lives at:

```text llms.txt
https://docs.triton.one/llms.txt
```

Drop that URL into your agent's context (Claude Code, Cursor, Codex) for full Triton coverage in one fetch. Per-product `llms.txt` files are also available under each section, e.g. `/solana/streaming/dragons-mouth/llms.txt`.

A native Triton MCP server is **coming soon**, with direct access to RPC queries, gRPC streams, and account management.

## Common builds

The most-asked builder paths. Each card jumps to a working walkthrough with code.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Stream Solana with gRPC</strong></td><td>Subscribe to accounts, transactions, and blocks via Dragon's Mouth, end to end.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/stream-solana-with-grpc">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/stream-solana-with-grpc</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/antenna.svg">antenna</a></td></tr><tr><td><strong>Get token metadata</strong></td><td>Query NFT and cNFT metadata fast with a single DAS API call.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/get-token-metadata">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/get-token-metadata</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/image.svg">image</a></td></tr><tr><td><strong>Copy trade a wallet</strong></td><td>Watch any wallet in real time and mirror its trades.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/copy-trade-a-wallet">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/copy-trade-a-wallet</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/copy.svg">copy</a></td></tr><tr><td><strong>Calculate Solana fees end to end</strong></td><td>Base fees, priority fees, and account rent explained.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/calculate-solana-fees-end-to-end">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/calculate-solana-fees-end-to-end</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/calculator.svg">calculator</a></td></tr><tr><td><strong>Stream a Raydium AMM pool</strong></td><td>Subscribe to pool state and trade events sub-slot.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/stream-a-raydium-amm-pool">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/stream-a-raydium-amm-pool</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/droplet.svg">droplet</a></td></tr><tr><td><strong>Mint a Solana token</strong></td><td>Create an SPL, Token-2022, or P-Token mint. Set metadata, airdrop to test wallets.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/mint-a-solana-token">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/mint-a-solana-token</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/sparkles.svg">sparkles</a></td></tr><tr><td><strong>Integrate Titan Prime</strong></td><td>Streaming swap quotes and routes that re-optimise live as the market moves.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/integrate-titan-prime">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/integrate-titan-prime</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/route.svg">route</a></td></tr></tbody></table>
---

## What's next?

New to Triton? Four steps from here to a production endpoint.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Account management</strong></td><td>Customer dashboard tour: endpoints, billing, team, and support.</td><td><a href="get-started/platform-overview.md">get-started/platform-overview.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/user-cog.svg">user-cog</a></td></tr><tr><td><strong>Plans and billing</strong></td><td>Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups.</td><td><a href="get-started/plans-and-billing.md">get-started/plans-and-billing.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/credit-card.svg">credit-card</a></td></tr><tr><td><strong>Quickstart</strong></td><td>Sign up, deposit, get an endpoint, send your first request.</td><td><a href="get-started/quickstart.md">get-started/quickstart.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/rocket.svg">rocket</a></td></tr><tr><td><strong>How to sign up</strong></td><td>Step-by-step from clicking signup to a live Triton endpoint.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/account-management/how-to-sign-up">https://kate-6.gitbook.io/triton-one-docs/guides/account-management/how-to-sign-up</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/user-plus.svg">user-plus</a></td></tr></tbody></table>
---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
