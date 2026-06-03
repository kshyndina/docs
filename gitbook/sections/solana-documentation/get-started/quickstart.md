# Quickstart

Just got your endpoint? This is a good place to start. You'll learn how to send your first RPC request, and where to go next based on what you're building.

{% stepper %}
{% step %}
#### Sign up and deposit $125

Sign up at [customers.triton.one](https://customers.triton.one/users/sign-up), verify your email, and top up the $125 minimum (stablecoins only).
{% endstep %}
{% step %}
#### Set up an endpoint

Open the dashboard, click **Create endpoint**, and pick **Solana mainnet** (or devnet for testing). The portal returns two things you'll use everywhere:

- **Endpoint URL**: `<your-endpoint>.mainnet.rpcpool.com`
- **Secret token**: a long random string

Keep the token server-side only. Frontend code uses an origin allowlist instead. See [Auth and security](auth-and-security.md). Full walkthrough: [Set up your account](platform-overview.md).
{% endstep %}
{% step %}
#### Send your first request

Call `getSlot` to confirm the endpoint is live. Pick your stack:

{% tabs %}
{% tab title="curl" %}
```bash
curl https://<endpoint>.mainnet.rpcpool.com/<token> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getSlot"}'
```
{% endtab %}
{% tab title="Solana Kit" %}
```javascript
import { createSolanaRpc } from "@solana/kit";

const rpc = createSolanaRpc("https://<endpoint>.mainnet.rpcpool.com/<token>");
const slot = await rpc.getSlot().send();
console.log(slot);
```
{% endtab %}
{% tab title="web3.js" %}
```javascript
import { Connection } from '@solana/web3.js';

const conn = new Connection(
  'https://<endpoint>.mainnet.rpcpool.com/<token>',
  'confirmed'
);
console.log(await conn.getSlot());
```
{% endtab %}
{% tab title="python" %}
```python
import requests

r = requests.post(
    'https://<endpoint>.mainnet.rpcpool.com/<token>',
    json={'jsonrpc': '2.0', 'id': 1, 'method': 'getSlot'},
)
print(r.json()['result'])
```
{% endtab %}
{% tab title="rust" %}
```rust
use solana_client::rpc_client::RpcClient;

let client = RpcClient::new(
    "https://<endpoint>.mainnet.rpcpool.com/<token>".to_string(),
);
println!("{}", client.get_slot()?);
```
{% endtab %}
{% endtabs %}

If you got back something like `{ "jsonrpc": "2.0", "result": 311340987, "id": 1 }`, you're connected. If you hit a 401, 429, timeout, or gRPC 403, see the [Error handling guide](https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/how-to-troubleshoot) for the full debug flow.
{% endstep %}
{% endstepper %}

## Where to next

Two ways in. Pick the tab that fits.

{% tabs %}
{% tab title="By product (I know what I want)" %}
Each product is purpose-built for one job. Pick what you need.

### Reading state

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Standard RPC</strong></td><td>Solana JSON-RPC over HTTPS. Every standard method, served from the regional fleet.</td><td><a href="../reading-state/standard-rpc.md">../reading-state/standard-rpc.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/zap.svg">zap</a></td></tr><tr><td><strong>Steamboat</strong></td><td>Custom indexes for `getProgramAccounts` and token-account hot paths. Up to 50x faster, no premium.</td><td><a href="../reading-state/steamboat-indexed-accounts.md">../reading-state/steamboat-indexed-accounts.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/database.svg">database</a></td></tr><tr><td><strong>DAS API</strong></td><td>Fastest read for NFT and cNFT ownership, proofs, and metadata.</td><td><a href="../reading-state/metaplex-das-api.md">../reading-state/metaplex-das-api.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/image.svg">image</a></td></tr><tr><td><strong>Account Sync</strong></td><td>Streaming-backed local cache for account reads. No polling, no code changes.</td><td><a href="../reading-state/account-sync.md">../reading-state/account-sync.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/refresh-cw.svg">refresh-cw</a></td></tr></tbody></table>
### Streaming

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Dragon's Mouth gRPC</strong></td><td>Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC.</td><td><a href="../streaming-data/dragon-s-mouth-grpc.md">../streaming-data/dragon-s-mouth-grpc.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/radio.svg">radio</a></td></tr><tr><td><strong>Whirligig WebSockets</strong></td><td>Drop-in for native Solana WebSockets. Fastest real-time data for frontends, backed by gRPC.</td><td><a href="../streaming-data/whirligig-websockets.md">../streaming-data/whirligig-websockets.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/rotate-cw.svg">rotate-cw</a></td></tr><tr><td><strong>Fumarole reliable streams</strong></td><td>Redundant streaming layer with 96h of stored data and built-in cursor resume.</td><td><a href="../streaming-data/fumarole-persistent-streams.md">../streaming-data/fumarole-persistent-streams.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/layers.svg">layers</a></td></tr><tr><td><strong>Hermes</strong></td><td>Pyth Hermes API. Real-time price feeds across hundreds of markets over REST and WebSocket.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes">https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/activity.svg">activity</a></td></tr></tbody></table>
### History

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Hydrant</strong></td><td>History with developer-shaped indexes. Millisecond reads from genesis across the full ledger.</td><td><a href="../historical-data/hydrant-archive.md">../historical-data/hydrant-archive.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/history.svg">history</a></td></tr><tr><td><strong>Old Faithful streams</strong></td><td>Replay every block from genesis through the same gRPC interface as live streams.</td><td><a href="../streaming-data/old-faithful-streams.md">../streaming-data/old-faithful-streams.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/archive.svg">archive</a></td></tr></tbody></table>
### Sending transactions

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Yellowstone Jet</strong></td><td>Direct-to-leader forwarding over QUIC with leader scheduling, connection pooling, and retries built in.</td><td><a href="../sending-transactions/yellowstone-jet.md">../sending-transactions/yellowstone-jet.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/send.svg">send</a></td></tr><tr><td><strong>Priority Fees API</strong></td><td>Smart fee estimation with tail-aware percentiles. Reliable landing without overpaying.</td><td><a href="../sending-transactions/priority-fees-api.md">../sending-transactions/priority-fees-api.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/trending-up.svg">trending-up</a></td></tr><tr><td><strong>Metis swap API</strong></td><td>Swap routing across 20+ DEXes with exact-out and platform-fee support built in.</td><td><a href="../sending-transactions/metis-swap-api.md">../sending-transactions/metis-swap-api.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/git-branch.svg">git-branch</a></td></tr><tr><td><strong>Titan swap API</strong></td><td>Streaming quotes and routes via DART live re-optimisation or the Prime API for high-volume desks.</td><td><a href="../sending-transactions/titan-swap-api.md">../sending-transactions/titan-swap-api.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/route.svg">route</a></td></tr><tr><td><strong>Jito bundles</strong></td><td>Jito bundle simulation through Triton endpoints. Test bundle ordering before submitting.</td><td><a href="../sending-transactions/jito-bundles.md">../sending-transactions/jito-bundles.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/package.svg">package</a></td></tr></tbody></table>
### Dedicated and validator services

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Dedicated gRPC node</strong></td><td>Private node with isolated CPU and unlimited concurrent gRPC connections. For latency-sensitive or heavy streaming workloads.</td><td><a href="../dedicated-nodes/overview.md">../dedicated-nodes/overview.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/server.svg">server</a></td></tr><tr><td><strong>White-label validator</strong></td><td>Branded validator with full key separation, zero ops overhead, and high availability.</td><td><a href="../validator-services/white-label-validators/overview.md">../validator-services/white-label-validators/overview.md</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/landmark.svg">landmark</a></td></tr></tbody></table>
{% endtab %}
{% tab title="By use case (I'm not sure yet)" %}
Pick the kind of app you're building. Each card jumps to the matching setup guide.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Trading or market making</strong></td><td>Live prices, sub-slot tx landing, anti-MEV. Stack: Dragon's Mouth, Jet, Priority Fees, Shield.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/trading-and-market-making-with-triton">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/trading-and-market-making-with-triton</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/coins.svg">coins</a></td></tr><tr><td><strong>DeFi protocols (Lending, DEXs)</strong></td><td>Pool state, swap activity, tx landing, historical fills. Stack: Dragon's Mouth, Jet, Hydrant, Titan.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/dex-or-defi-protocol">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/dex-or-defi-protocol</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/git-merge.svg">git-merge</a></td></tr><tr><td><strong>Wallet or consumer app</strong></td><td>Balances, history, NFT portfolio, live updates. Stack: Standard RPC, DAS API, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/wallet-or-consumer-app">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/wallet-or-consumer-app</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/smartphone.svg">smartphone</a></td></tr><tr><td><strong>NFT marketplace</strong></td><td>Mints, metadata, collection feeds, sale events. Stack: DAS API, ZK Compression, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/nft-or-compressed-asset-platform">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/nft-or-compressed-asset-platform</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/palette.svg">palette</a></td></tr><tr><td><strong>Indexer or analytics</strong></td><td>Custom indexes, historical backfill, parsed transactions. Stack: Steamboat, Hydrant, Old Faithful, Fumarole.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/indexer-or-analytics">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/indexer-or-analytics</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/bar-chart-3.svg">bar-chart-3</a></td></tr><tr><td><strong>Gaming</strong></td><td>On-chain item state, real-time updates, fast reads. Stack: Standard RPC, DAS API, Dragon's Mouth, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/gaming">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/gaming</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/gamepad-2.svg">gamepad-2</a></td></tr><tr><td><strong>AI agent or LLM app</strong></td><td>MCP access, llms.txt context, autonomous setup. Stack: MCP, llms.txt, Standard RPC, DAS API.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/ai-agent-or-llm-app">https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/ai-agent-or-llm-app</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/bot.svg">bot</a></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
