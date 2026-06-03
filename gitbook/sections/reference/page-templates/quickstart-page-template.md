# Quickstart page template

Reference layout for a per-product quickstart. Five minutes to first response. Three numbered steps, working code, expected output, where to next.

> **What this is.** A template for a per-product quickstart: `/solana/<section>/<product>/quickstart`. The page promises five-minutes-to-first-response and delivers exactly that. Replace placeholder copy and remove comment blocks before shipping.

## When to use this template

- One quickstart per product, sitting next to the product overview.
- The page goal is **first measurable success** -- a working response, a streamed event, a confirmed transaction.
- If a product needs more than 5 steps or 10 minutes, that's a guide, not a quickstart.

---

## Dragon's Mouth quickstart

> Title is `<Product> quickstart`, sentence case. Description in frontmatter says how long this takes and what success looks like.

Stream account writes from a Triton endpoint in five minutes. By the end you'll see a live event for every transaction touching a wallet of your choice.

> Above is the **promise**. State it explicitly. Time + concrete success criterion. The reader decides whether to keep reading.

{% hint style="info" %}
**Time:** 5 minutes. **You'll need:** a Triton endpoint with a token (see [Get started](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/quickstart)), Node.js 20+ or Python 3.10+, a wallet pubkey to watch.
{% endhint %}

## Steps

> Three steps is the sweet spot. Five is the cap. If you need more, refactor: split prerequisites and "advanced" content out.

{% stepper %}
{% step %}
#### Install the client

The official Vixen Streams SDK ships in TypeScript and Python.

{% tabs %}
{% tab title="npm" %}
```bash
npm install @triton-one/vixen-stream
```
{% endtab %}
{% tab title="pip" %}
```bash
pip install triton-vixen-stream
```
{% endtab %}
{% endtabs %}

{% endstep %}
{% step %}
#### Open a subscription

Connect to your endpoint and subscribe to a single account. Replace `<endpoint>`, `<token>`, and `<pubkey>`.

{% tabs %}
{% tab title="TypeScript" %}
```typescript
import {
  ProgramStreamsServiceClient,
  credentials,
  createCallCredentials,
} from "@triton-one/vixen-stream";

const client = new ProgramStreamsServiceClient(
  "<endpoint>.mainnet.rpcpool.com:443",
  credentials.combineChannelCredentials(
    credentials.createSsl(),
    createCallCredentials("<token>"),
  ),
);

const stream = client.subscribe();
stream.write({
  transactions: {
    watch: { accountInclude: ["<pubkey>"], failed: false },
  },
});

stream.on("data", (msg) => console.log(JSON.stringify(msg, null, 2)));
```
{% endtab %}
{% tab title="Python" %}
```python
from vixen_stream import StreamsServiceClient

client = StreamsServiceClient("<endpoint>.mainnet.rpcpool.com:443", token="<token>")
for msg in client.subscribe(transactions={"watch": {"account_include": ["<pubkey>"]}}):
    print(msg)
```
{% endtab %}
{% endtabs %}

{% endstep %}
{% step %}
#### Run it

Start the script. The first event arrives the next time the wallet trades.

```bash
node stream.ts
# or:  python stream.py
```

Expected output (truncated):

```json
{
  "transaction": {
    "signature": "5Yt1...XwQz",
    "slot": 311340987,
    "isVote": false,
    ...
  }
}
```
{% endstep %}
{% endstepper %}

## How to verify it's working

> Critical and underrated. The reader needs a way to check success without external dependencies. A `getSlot` call, a known wallet, a curl command -- anything they can run today.

If the first event doesn't arrive within a minute, pick a wallet you know is active right now (from Solana Explorer's "highest activity" leaderboard, for instance). Or send yourself a tiny SOL transfer to the watched pubkey to trigger one.

If you see no events at all, see the [streaming troubleshooting checklist](/solana-guides/error-handling/streaming).

## Where to next

> Two cards: the natural next thing they'll want to do, and the deep-dive guide. Cards are not "Read more" -- they're routed at specific intents.

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Filter by program, instruction, or accounts</strong></td><td>The full subscription schema. How to scope the stream to exactly what you need.</td><td><a href="#">#</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/filter.svg">filter</a></td></tr><tr><td><strong>Build a copy-trade bot</strong></td><td>End-to-end guide combining Dragon's Mouth, Vixen parsing, and Yellowstone Jet.</td><td><a href="https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/copy-trade-a-wallet">https://kate-6.gitbook.io/triton-one-docs/guides/end-to-end-builds/copy-trade-a-wallet</a></td><td><a href="https://unpkg.com/lucide-static@latest/icons/copy.svg">copy</a></td></tr></tbody></table>
## Footer

> Standard footer pattern across all quickstarts -- support, account, sales. Keeps the reader unstuck.

 Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)

 Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)

---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
