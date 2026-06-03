# Shield MEV protection

Yellowstone Shield lets you control which validators can process your Solana transactions via on-chain allowlists or blocklists. Anti-sandwich, anti-frontrunning, anti-MEV at the routing layer.

{% hint style="warning" %}
**Work in progress.** This page is being reviewed -- don't reference it yet, copy isn't final.
{% endhint %}

## What is Shield

Create a list of validators you trust (allowlist) or don't trust (blocklist). Your transactions only go to validators that match your criteria.

**Why use Shield?** Some validators engage in practices that hurt users:

- **Sandwich attacks** -- inserting transactions before and after yours to extract value
- **Frontrunning** -- copying and executing your transaction idea before you
- **Other harmful MEV** -- various techniques to extract value at users' expense

Shield helps you avoid these validators by simply not sending your transactions to them.

## How it works

1. **Create a policy.** An on-chain list of validators (either "allow these validators" or "block these validators").
2. **Own your policy.** When you create a policy, you receive a special SPL token that gives you control over it.
3. **Use the policy.** Add your policy's address to your transactions.
4. **Automatic filtering.** The RPC checks each validator against your policy and only sends transactions to approved validators.

**What happens to blocked transactions?** If the current validator doesn't meet your criteria, the transaction is dropped -- it won't be sent to that validator. The system doesn't hold or queue transactions.

{% hint style="warning" %}
**Time-critical transactions.** Shield can drop transactions when no eligible validators are available. Be careful using strict policies with time-sensitive operations like arbitrage or liquidations.
{% endhint %}

{% hint style="info" %}
Shield only works with Shield-enabled RPCs (like those using [Yellowstone Jet](yellowstone-jet.md)). Standard Solana RPCs ignore the policy parameter.
{% endhint %}

## Quickstart

If you're already using a Shield-enabled RPC (like Triton's), add the policy to your transaction.

### RPC method parameter

```json sendTransaction with policy
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendTransaction",
  "params": [
    "<base64_encoded_transaction>",
    {
      "encoding": "base64",
      "skipPreflight": true,
      "forwardingPolicies": ["<your_policy_pda>"]
    }
  ]
}
```

### HTTP header alternative

```text Header
Solana-ForwardingPolicies: "<your_policy_pda>,<your_policy_pda2>"
```

### Full TypeScript example

```typescript TypeScript

const transaction = new Transaction().add(/* your instructions */);
const signedTx = await wallet.signTransaction(transaction);
const serializedTx = bs58.encode(signedTx.serialize());

const response = await fetch('https://<your-endpoint>.mainnet.rpcpool.com/<your-token>', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'sendTransaction',
    params: [
      serializedTx,
      {
        encoding: 'base58',
        skipPreflight: true,
        forwardingPolicies: ['<policy_pda>']
      }
    ]
  })
});

const result = await response.json();
const signature = result.result;
```

Shield policies require RPCs that support the `forwardingPolicies` parameter -- standard `@solana/web3.js` `connection.sendTransaction()` doesn't surface it, so use `fetch` directly.

## Policies and tokens

When you create a Shield policy:

- An SPL token (using Token Extensions) is created
- You receive 1 token in your wallet
- This token gives you control over the policy
- As the creator, you keep the mint authority and can mint more tokens if needed
- Anyone holding the token can manage the policy (add/remove validators)
- The policy lives on-chain and can be used by anyone who knows its address

The token is fungible and more can be minted, so you can share policy management by minting and sending tokens to others.

## Protection limitations

{% hint style="warning" %}
Shield policies are **not automatic protection** against harmful validator practices. Policies only block validators that are on your blocklist (or not on your allowlist). New validators join Solana every epoch, and harmful validators can appear at any time. **Policy maintainers must actively update their lists** to catch them.
{% endhint %}

Think of it as a filter, not a guarantee. The quality of protection depends entirely on how well the policy is maintained.

## Finding existing policies

[validators.app/yellowstone-shield](https://www.validators.app/yellowstone-shield?locale=en\&network=mainnet) is the policy explorer. You can:

- Browse all existing policies
- See which validators are included or excluded
- Copy policy addresses for your transactions
- Check when policies were last updated

Common policy types:

| Type | Pattern |
| --- | --- |
| **Allow lists** | Top validators by stake, geographically distributed validators, performance-based selection |
| **Block lists (deny lists)** | Validators known for sandwich attacks or frontrunning, poor-performing validators, community-flagged validators |

## Create your own policy

### Prerequisites

- Solana CLI installed and configured
- SOL for transaction fees
- A list of validator addresses you want to allow or block

### 1. Install Shield CLI

```bash
git clone https://github.com/rpcpool/yellowstone-shield
cd yellowstone-shield
cargo build --release --bin yellowstone-shield-cli
```

### 2. Prepare metadata

Create a JSON file describing your policy:

```json policy.json
{
  "name": "My Validator Policy",
  "symbol": "MVP",
  "description": "Blocks validators known for sandwich attacks",
  "image": "https://your-image-url.com/image.png",
  "external_url": "https://your-website.com",
  "attributes": []
}
```

Upload to IPFS or Arweave and save the URL.

### 3. Create the policy

{% tabs %}
{% tab title="Blocklist (deny)" %}
```bash
yellowstone-shield-cli policy create \
  --strategy deny \
  --name "My Validator Policy" \
  --symbol "MVP" \
  --uri "https://your-metadata-url.json"
```
{% endtab %}
{% tab title="Allowlist (allow)" %}
```bash
yellowstone-shield-cli policy create \
  --strategy allow \
  --name "My Validator Policy" \
  --symbol "MVP" \
  --uri "https://your-metadata-url.json"
```
{% endtab %}
{% endtabs %}

The CLI outputs your policy's mint address -- save this. You receive 1 token and keep mint authority (so you can mint more later to share policy management).

### 4. Add validators

Create a text file with validator addresses (one per line):

```text validators.txt
ValidatorAddress1...
ValidatorAddress2...
ValidatorAddress3...
```

Then add them to your policy:

```bash
yellowstone-shield-cli identities add \
  --mint <your_mint_address> \
  --identities-path validators.txt
```

### Manage your policy

To manage a policy (add/remove validators), you must hold at least 1 token in your wallet. If you've transferred all your tokens to others, you'll lose the ability to manage the policy.

{% tabs %}
{% tab title="Replace the entire list" %}
```bash
yellowstone-shield-cli identities update \
  --mint <mint_address> \
  --identities-path new_validators.txt
```
{% endtab %}
{% tab title="Remove specific validators" %}
```bash
yellowstone-shield-cli identities remove \
  --mint <mint_address> \
  --identities-path validators_to_remove.txt
```
{% endtab %}
{% tab title="View policy details" %}
```bash
yellowstone-shield-cli policy show --mint <mint_address>
```
{% endtab %}
{% endtabs %}

## For RPC providers

If you're running your own RPC and want to support Shield:

- **Using Yellowstone Jet** -- Shield support is built in.
- **Custom integration** -- use the [yellowstone-shield-store](https://crates.io/crates/yellowstone-shield-store) crate to cache policies locally, check validators against policies, and integrate with your transaction forwarding logic.

## Key points

1. **Policies need maintenance.** New validators appear every epoch. Lists must be updated regularly.
2. **It's a filter, not a guarantee.** Shield prevents transactions from going to certain validators -- it doesn't guarantee protection from sandwich attacks or transaction failures.
3. **Token = control.** When you create a policy, you get an SPL token. Anyone with this token can manage the policy. You can mint more tokens to share control.
4. **Anyone can use your policy.** Once created, anyone who knows the policy address can use it in their transactions.
5. **Shield-enabled RPC required.** Only Shield-enabled RPCs (like those using Yellowstone Jet) honour the `forwardingPolicies` parameter.

## What's next

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-paper-plane">:paper-plane:</i> <strong>Yellowstone Jet</strong></td><td>Direct-to-leader forwarding over QUIC with leader scheduling, connection pooling, and retries built in.</td><td><a href="yellowstone-jet.md">yellowstone-jet.md</a></td></tr><tr><td><i class="fa-arrow-trend-up">:arrow-trend-up:</i> <strong>Priority Fees API</strong></td><td>Smart fee estimation with tail-aware percentiles. Reliable landing without overpaying.</td><td><a href="priority-fees-api.md">priority-fees-api.md</a></td></tr><tr><td><i class="fa-box">:box:</i> <strong>Jito bundles</strong></td><td>Jito bundle simulation through Triton endpoints. Test bundle ordering before submitting.</td><td><a href="jito-bundles.md">jito-bundles.md</a></td></tr><tr><td><i class="fa-book-open">:book-open:</i> <strong>Yellowstone Shield blog post</strong></td><td>The full architecture and design rationale behind Shield's allow/blocklist model.</td><td><a href="https://blog.triton.one/introducing-yellowstone-shield">https://blog.triton.one/introducing-yellowstone-shield</a></td></tr></tbody></table>
<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
