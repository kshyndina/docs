# API reference page template

Reference layout for a single API method or endpoint page. Built from the patterns Helius, Solana, and Stripe use.

> **What this is.** A copy-paste template for documenting a single API method (JSON-RPC, REST, gRPC). Below each section is a brief comment explaining why it matters and what to put there. Replace the placeholder text and remove the comment blocks before shipping.

## When to use this template

- One page per method, not one mega-page for the whole API.
- Use `api/openapi.json` for REST endpoints whenever possible (Mintlify auto-generates the playground from the spec). This template is for methods that don't fit OpenAPI cleanly (JSON-RPC, gRPC) or for the quick "what does this do" page that links into the playground.

---

## getMethodName

> Replace the H2 above with the actual method name. Keep it as plain text, not as code, so search ranks the page on the method name. Use **lowerCamelCase** for JSON-RPC, **REST verb plus path** for REST.

A one-sentence description of what this method does and when to use it. The user should be able to skip the rest of the page if they already know the method.

{% hint style="info" %}
**Use case.** Add a one-line use-case statement here so the user knows whether they're on the right page. Example: "Use this to fetch the lamport balance of an account before sending a transaction."
{% endhint %}

### When to use this method

> Two-to-four bullets explaining the most common use cases. Helps users decide between similar methods.

- **Live balance check** — before sending a transaction, confirm the wallet has enough lamports.
- **Account discovery** — verify a public key is funded and on chain.
- **Polling alternative** — combine with `getSignaturesForAddress` for tx-history dashboards.

### When not to use it

- For NFT or SPL token balances, use [`getTokenAccountsByOwner`](#) — `getBalance` only returns native SOL.
- For real-time updates, use [`accountSubscribe`](#) over WebSocket or [Dragon's Mouth gRPC](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/dragon-s-mouth-grpc).

### Parameters

> Always render parameters as a real `<table>` (not a description list). Columns: name, type, required/optional, description, default. The DAS API and Helius docs both use this layout.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `pubkey` | `string` | required | Base58-encoded public key of the account to query. |
| `commitment` | `"processed" \| "confirmed" \| "finalized"` | optional | Commitment level. Defaults to `finalized`. |
| `minContextSlot` | `number` | optional | Reject the request if the cluster has not processed this slot yet. |

### Response

> Show the response shape. For nested fields, indent or use a sub-table. Always note units (lamports vs SOL, microseconds vs ms).

```json
{
  "jsonrpc": "2.0",
  "result": {
    "context": { "slot": 311340987 },
    "value": 4982350
  },
  "id": 1
}
```

| Field | Type | Description |
| --- | --- | --- |
| `result.context.slot` | `number` | Slot the data was sampled at. |
| `result.value` | `number` | Account balance in **lamports** (1 SOL = 1,000,000,000 lamports). |

### Example request

> Code group with at least: curl, the language with the strongest SDK ecosystem (JavaScript / Python), and one systems language (Rust / Go). Each example must run as-is when the placeholders are filled in.

{% tabs %}
{% tab title="curl" %}
```bash
curl https://<endpoint>.mainnet.rpcpool.com/<token> \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBalance",
    "params": ["86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY"]
  }'
```
{% endtab %}
{% tab title="Solana Kit" %}
```javascript

const rpc = createSolanaRpc("https://<endpoint>.mainnet.rpcpool.com/<token>");
const { value: lamports } = await rpc
  .getBalance("86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY")
  .send();
console.log(`Balance: ${Number(lamports) / 1e9} SOL`);
```
{% endtab %}
{% tab title="python" %}
```python

resp = requests.post(
    "https://<endpoint>.mainnet.rpcpool.com/<token>",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": ["86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY"],
    },
)
lamports = resp.json()["result"]["value"]
print(f"Balance: {lamports / 1e9} SOL")
```
{% endtab %}
{% tab title="rust" %}
```rust
use solana_client::rpc_client::RpcClient;
use solana_sdk::pubkey::Pubkey;
use std::str::FromStr;

let client = RpcClient::new("https://<endpoint>.mainnet.rpcpool.com/<token>".to_string());
let pubkey = Pubkey::from_str("86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY")?;
let lamports = client.get_balance(&pubkey)?;
println!("Balance: {} SOL", lamports as f64 / 1_000_000_000.0);
```
{% endtab %}
{% endtabs %}

### Errors

> Document the errors specific to this method. Keep generic transport errors (401, 429, 500) on the central error-handling page and link there.

| Code | Message | What it means |
| --- | --- | --- |
| `-32602` | Invalid params | The pubkey isn't a valid base58 string, or commitment isn't recognised. |
| `-32602` | Account does not exist | The pubkey is valid but no account exists at that address. |

For 401, 429, timeout, and gRPC-403 patterns, see the [Error handling guide](https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/how-to-troubleshoot).

### Rate limits

> Always link to the central rate-limits page. Note any method-specific cap.

Standard tier shares the global rate limit. See [Rate and connection limits](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/rate-and-connection-limits). `getBalance` has no per-method cap above the shared limit.

### Performance notes

> Optional but valuable. Note how the response time scales with the data, and any client-side things to do or avoid.

- Median Triton response time: **~12 ms** to the closest GeoDNS region.
- Cache the result for at most a few hundred milliseconds. Balances change every slot for active wallets.
- For dashboards polling many wallets, prefer [`getMultipleAccounts`](#) over a fan-out of `getBalance` calls -- one round trip vs N.

### Related

> Always cross-link to siblings. Helps users land on the right method when they search broadly.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>getMultipleAccounts</strong></td><td>Batch balance + data for up to 100 accounts in one call.</td><td><a href="#">#</a></td></tr><tr><td><strong>getTokenAccountsByOwner</strong></td><td>SPL token balances (this method only returns native SOL).</td><td><a href="#">#</a></td></tr><tr><td><strong>accountSubscribe</strong></td><td>WebSocket subscription for live balance updates.</td><td><a href="#">#</a></td></tr><tr><td><strong>Error handling</strong></td><td>Standard transport-level error responses and the recommended retry shape.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/how-to-troubleshoot">https://kate-6.gitbook.io/triton-one-docs/guides/error-handling/how-to-troubleshoot</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
