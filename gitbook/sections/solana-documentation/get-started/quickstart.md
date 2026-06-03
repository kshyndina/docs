# Quickstart

Just got your endpoint? This is a good place to start. You'll learn how to send your first RPC request, and where to go next based on what you're building.

{% stepper %}
{% step %}
#### Sign up and deposit $125

Sign up at [customers.triton.one](https://customers.triton.one/users/sign-up), verify your email, and top up the {"$"}125 minimum (stablecoins only).
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

{% content-ref url="../reading-state/standard-rpc.md" %}
[Standard RPC](../reading-state/standard-rpc.md)
{% endcontent-ref %}

{% content-ref url="../reading-state/steamboat-indexed-accounts.md" %}
[Steamboat](../reading-state/steamboat-indexed-accounts.md)
{% endcontent-ref %}

{% content-ref url="../reading-state/metaplex-das-api.md" %}
[DAS API](../reading-state/metaplex-das-api.md)
{% endcontent-ref %}

{% content-ref url="../reading-state/account-sync.md" %}
[Account Sync](../reading-state/account-sync.md)
{% endcontent-ref %}

### Streaming

{% content-ref url="../streaming-data/dragon-s-mouth-grpc.md" %}
[Dragon's Mouth gRPC](../streaming-data/dragon-s-mouth-grpc.md)
{% endcontent-ref %}

{% content-ref url="../streaming-data/whirligig-websockets.md" %}
[Whirligig WebSockets](../streaming-data/whirligig-websockets.md)
{% endcontent-ref %}

{% content-ref url="../streaming-data/fumarole-persistent-streams.md" %}
[Fumarole reliable streams](../streaming-data/fumarole-persistent-streams.md)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes" %}
[Hermes](https://kate-6.gitbook.io/triton-one-docs/pyth/pyth/pyth-hermes)
{% endcontent-ref %}

### History

{% content-ref url="../historical-data/hydrant-archive.md" %}
[Hydrant](../historical-data/hydrant-archive.md)
{% endcontent-ref %}

{% content-ref url="../streaming-data/old-faithful-streams.md" %}
[Old Faithful streams](../streaming-data/old-faithful-streams.md)
{% endcontent-ref %}

### Sending transactions

{% content-ref url="../sending-transactions/yellowstone-jet.md" %}
[Yellowstone Jet](../sending-transactions/yellowstone-jet.md)
{% endcontent-ref %}

{% content-ref url="../sending-transactions/priority-fees-api.md" %}
[Priority Fees API](../sending-transactions/priority-fees-api.md)
{% endcontent-ref %}

{% content-ref url="../sending-transactions/metis-swap-api.md" %}
[Metis swap API](../sending-transactions/metis-swap-api.md)
{% endcontent-ref %}

{% content-ref url="../sending-transactions/titan-swap-api.md" %}
[Titan swap API](../sending-transactions/titan-swap-api.md)
{% endcontent-ref %}

{% content-ref url="../sending-transactions/jito-bundles.md" %}
[Jito bundles](../sending-transactions/jito-bundles.md)
{% endcontent-ref %}

### Dedicated and validator services

{% content-ref url="../dedicated-nodes/overview.md" %}
[Dedicated gRPC node](../dedicated-nodes/overview.md)
{% endcontent-ref %}

{% content-ref url="../validator-services/white-label-validators/overview.md" %}
[White-label validator](../validator-services/white-label-validators/overview.md)
{% endcontent-ref %}

{% endtab %}
{% tab title="By use case (I'm not sure yet)" %}
Pick the kind of app you're building. Each card jumps to the matching setup guide.

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/trading-and-market-making-with-triton" %}
[Trading or market making](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/trading-and-market-making-with-triton)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/dex-or-defi-protocol" %}
[DeFi protocols (Lending, DEXs)](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/dex-or-defi-protocol)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/wallet-or-consumer-app" %}
[Wallet or consumer app](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/wallet-or-consumer-app)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/nft-or-compressed-asset-platform" %}
[NFT marketplace](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/nft-or-compressed-asset-platform)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/indexer-or-analytics" %}
[Indexer or analytics](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/indexer-or-analytics)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/gaming" %}
[Gaming](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/gaming)
{% endcontent-ref %}

{% content-ref url="https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/ai-agent-or-llm-app" %}
[AI agent or LLM app](https://kate-6.gitbook.io/triton-one-docs/guides/set-up-your-rpc-for/ai-agent-or-llm-app)
{% endcontent-ref %}

{% endtab %}
{% endtabs %}

---

---

Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  
Sales questions? [Contact sales](https://triton.one/contact).  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
