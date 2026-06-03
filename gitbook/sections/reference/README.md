# Section overview template

Reference layout for a section landing page (Reading state, Streaming, History, etc). The page positions every product in the section and helps the reader pick.

> **What this is.** A template for a section landing / overview page that lives at `/solana/<section>/overview` (e.g. `/solana/reading-state/overview`). The page introduces the section and routes the reader to one of the products underneath it. Replace placeholder copy and remove comment blocks before shipping.

## When to use this template

- Section has 2+ products underneath (otherwise just send the reader straight to the product page).
- You want the reader to compare options before clicking through.
- Use sparingly — too many overview pages add navigation, not content.

---

## Reading state

> Title is the section name, plain. The subtitle below is one sentence framing the whole section.

**Every way to read on-chain state on Solana, from sub-100 ms reads to 50x-faster custom indexes.**

> 1-2 paragraphs orienting the reader. What does this section cover, what's the problem it solves, what's the strategic frame Triton takes here.

Solana's account model is read-heavy: most apps spend most of their RPC budget on `getAccountInfo`, `getMultipleAccounts`, and `getProgramAccounts`. Triton splits the read layer into purpose-built components so each one can be tuned: vanilla JSON-RPC stays close to the native validator behaviour, indexed reads return in milliseconds, NFT data has its own DAS-spec endpoint, and live account state is mirrored without polling.

The right product depends on the access pattern: one-off lookups vs scans, reads vs subscriptions, and whether the data is account state, token state, or NFT metadata. The decision tree below lays it out.

## Pick the right product

> Cards or table. Cards work better when each option has a clear use case; table works better when the comparison is dimensional. Pick one.

[Standard RPC](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/standard-rpc)

[Steamboat](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/steamboat-indexed-accounts)

[DAS API](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/metaplex-das-api)

[Account Sync](https://kate-6.gitbook.io/triton-one-docs/documentation/reading-state/account-sync)

### Decision matrix

> Optional but high-impact. A small comparison table so the reader can pick at a glance.

| Need | Pick | Why |
| --- | --- | --- |
| One-off `getBalance` / `getAccountInfo` | Standard RPC | Lowest setup cost, fastest path to first byte. |
| `getProgramAccounts` over a 100k-account program | Steamboat | Native scan is O(n); Steamboat reads off a hot index. |
| NFT and cNFT collection feeds | DAS API | Triton helped author the spec. |
| Always-current account state for a watch list | Account Sync | Push-based, no polling, no rate-limit pressure. |
| Real-time slot-by-slot account updates | [Dragon's Mouth gRPC](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/dragon-s-mouth-grpc) | Streaming sits in the next section, but it's often the right answer. |

## How these fit together

> Optional architecture diagram. Use when it actually clarifies — skip if it's just a label-shuffle.

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#F2EDF6','primaryBorderColor':'#7A4BA0','primaryTextColor':'#171717','lineColor':'#956FB3','tertiaryColor':'#D7C9E3'}}}%%
flowchart LR
    Validator[Validator Geyser] --> Stream[gRPC stream]
    Stream --> Steamboat
    Stream --> Sync[Account Sync]
    Validator --> Std[Standard RPC]
    Validator --> DAS[DAS API]
    YourApp[Your app] --> Std
    YourApp --> Steamboat
    YourApp --> DAS
    YourApp --> Sync
```

> One paragraph explaining what the diagram shows. The diagram is the visual; the paragraph is the read.

All four read paths share the same underlying validator. Standard RPC and DAS API hit the validator's account database directly. Steamboat and Account Sync derive from the gRPC stream, which lets them serve queries the native RPC can't (custom indexes, push subscriptions). You can mix freely on the same endpoint — there's no separate setup per product.

## Quickstart

> One CTA per overview page. Send the reader to the most likely first stop.

[Quickstart: get reading in 5 minutes](https://kate-6.gitbook.io/triton-one-docs/documentation/get-started/quickstart)

## Related sections

> Cross-link siblings. Helps users navigate without going back to the top-level nav.

[Streaming data](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/overview)

[Historical data](https://kate-6.gitbook.io/triton-one-docs/documentation/historical-data/hydrant-archive)

---
🛟 Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
⚙️ Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
💼 Sales questions? [Contact sales](https://triton.one/contact)  
✨ AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
📡 Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
