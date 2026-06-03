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

Keep the token server-side only. Frontend code uses an origin allowlist instead. See [Auth and security](authentication.md). Full walkthrough: [Set up your account](platform-overview.md).
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
{% tab title="By product" %}
Each product is purpose-built for one job. Pick what you need.

### Reading state

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-database">:database:</i> <strong>Steamboat</strong></td><td>Custom indexes for `getProgramAccounts` and token-account hot paths. Up to 50x faster, no premium.</td><td><a href="../reading-state/steamboat-indexed-accounts.md">../reading-state/steamboat-indexed-accounts.md</a></td></tr><tr><td><i class="fa-image">:image:</i> <strong>DAS API</strong></td><td>Fastest read for NFT and cNFT ownership, proofs, and metadata.</td><td><a href="../reading-state/metaplex-das-api.md">../reading-state/metaplex-das-api.md</a></td></tr><tr><td><i class="fa-arrows-rotate">:arrows-rotate:</i> <strong>Account Sync</strong></td><td>Streaming-backed local cache for account reads. No polling, no code changes.</td><td><a href="../reading-state/account-sync.md">../reading-state/account-sync.md</a></td></tr></tbody></table>

### Streaming

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-radio">:radio:</i> <strong>Dragon's Mouth gRPC</strong></td><td>Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC.</td><td><a href="../streaming-data/dragon-s-mouth-grpc.md">../streaming-data/dragon-s-mouth-grpc.md</a></td></tr><tr><td><i class="fa-rotate-right">:rotate-right:</i> <strong>Whirligig WebSockets</strong></td><td>Drop-in for native Solana WebSockets. Fastest real-time data for frontends, backed by gRPC.</td><td><a href="../streaming-data/whirligig-websockets.md">../streaming-data/whirligig-websockets.md</a></td></tr><tr><td><i class="fa-layer-group">:layer-group:</i> <strong>Fumarole reliable streams</strong></td><td>Redundant streaming layer with 96h of stored data and built-in cursor resume.</td><td><a href="../streaming-data/fumarole-persistent-streams.md">../streaming-data/fumarole-persistent-streams.md</a></td></tr><tr><td><i class="fa-chart-line">:chart-line:</i> <strong>Hermes</strong></td><td>Pyth Hermes API. Real-time price feeds across hundreds of markets over REST and WebSocket.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes">https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes</a></td></tr></tbody></table>

### History

### Sending transactions

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-paper-plane">:paper-plane:</i> <strong>Jet sender</strong></td><td>Direct-to-leader forwarding over QUIC with leader scheduling, connection pooling, and retries built in.</td><td><a href="../sending-transactions/jet-sender.md">../sending-transactions/jet-sender.md</a></td></tr><tr><td><i class="fa-arrow-trend-up">:arrow-trend-up:</i> <strong>Priority Fees API</strong></td><td>Smart fee estimation with tail-aware percentiles. Reliable landing without overpaying.</td><td><a href="../sending-transactions/priority-fees-api.md">../sending-transactions/priority-fees-api.md</a></td></tr><tr><td><i class="fa-code-branch">:code-branch:</i> <strong>Metis swap API</strong></td><td>Swap routing across 20+ DEXes with exact-out and platform-fee support built in.</td><td><a href="../sending-transactions/3rd-party-apis/metis-swap-api.md">../sending-transactions/3rd-party-apis/metis-swap-api.md</a></td></tr><tr><td><i class="fa-route">:route:</i> <strong>Titan swap API</strong></td><td>Streaming quotes and routes via DART live re-optimisation or the Prime API for high-volume desks.</td><td><a href="../sending-transactions/3rd-party-apis/titan-swap-api.md">../sending-transactions/3rd-party-apis/titan-swap-api.md</a></td></tr><tr><td><i class="fa-box">:box:</i> <strong>Jito bundles</strong></td><td>Jito bundle simulation through Triton endpoints. Test bundle ordering before submitting.</td><td><a href="../sending-transactions/3rd-party-apis/jito-bundles.md">../sending-transactions/3rd-party-apis/jito-bundles.md</a></td></tr></tbody></table>

### Dedicated and validator services

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-server">:server:</i> <strong>Dedicated gRPC node</strong></td><td>Private node with isolated CPU and unlimited concurrent gRPC connections. For latency-sensitive or heavy streaming workloads.</td><td><a href="../dedicated-nodes/overview.md">../dedicated-nodes/overview.md</a></td></tr><tr><td><i class="fa-landmark">:landmark:</i> <strong>White-label validator</strong></td><td>Branded validator with full key separation, zero ops overhead, and high availability.</td><td><a href="../validator-services/white-label-validators/overview.md">../validator-services/white-label-validators/overview.md</a></td></tr></tbody></table>

{% endtab %}
{% tab title="By use case" %}
Pick the kind of app you're building. Each card jumps to the matching setup guide.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-coins">:coins:</i> <strong>Trading or market making</strong></td><td>Live prices, sub-slot tx landing, anti-MEV. Stack: Dragon's Mouth, Jet, Priority Fees, Shield.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/trading-and-market-making">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/trading-and-market-making</a></td></tr><tr><td><i class="fa-code-merge">:code-merge:</i> <strong>DeFi protocols (Lending, DEXs)</strong></td><td>Pool state, swap activity, tx landing, historical fills. Stack: Dragon's Mouth, Jet, Hydrant, Titan.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/dex-or-defi-protocol">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/dex-or-defi-protocol</a></td></tr><tr><td><i class="fa-mobile-screen">:mobile-screen:</i> <strong>Wallet or consumer app</strong></td><td>Balances, history, NFT portfolio, live updates. Stack: Standard RPC, DAS API, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/wallet-or-consumer-app">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/wallet-or-consumer-app</a></td></tr><tr><td><i class="fa-palette">:palette:</i> <strong>NFT marketplace</strong></td><td>Mints, metadata, collection feeds, sale events. Stack: DAS API, ZK Compression, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/nft-or-compressed-asset-platform">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/nft-or-compressed-asset-platform</a></td></tr><tr><td><i class="fa-chart-column">:chart-column:</i> <strong>Indexer or analytics</strong></td><td>Custom indexes, historical backfill, parsed transactions. Stack: Steamboat, Hydrant, Old Faithful, Fumarole.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/indexer-or-analytics">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/indexer-or-analytics</a></td></tr><tr><td><i class="fa-gamepad">:gamepad:</i> <strong>Gaming</strong></td><td>On-chain item state, real-time updates, fast reads. Stack: Standard RPC, DAS API, Dragon's Mouth, Whirligig.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/gaming">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/gaming</a></td></tr><tr><td><i class="fa-robot">:robot:</i> <strong>AI agent or LLM app</strong></td><td>MCP access, llms.txt context, autonomous setup. Stack: MCP, llms.txt, Standard RPC, DAS API.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/ai-agent-or-llm-app">https://kate-6.gitbook.io/triton-one-docs/guides/quickstart-on-triton/ai-agent-or-llm-app</a></td></tr></tbody></table>

{% endtab %}
{% endtabs %}
