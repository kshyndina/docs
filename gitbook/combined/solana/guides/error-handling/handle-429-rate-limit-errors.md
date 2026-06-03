# Handle 429 rate-limit errors

What HTTP 429 means on Triton, why you hit it, and how to back off and retry without losing requests.

When your traffic exceeds the per-IP rate budget on a Triton endpoint, the server returns `HTTP 429 Too Many Requests`. The request didn't reach the validator -- you can safely retry it once the window resets.

## The 10-second window

Triton's shared infrastructure enforces two budgets on every IP, both reset every 10 seconds:

- **Total RPS** -- the budget across every method.
- **Per-method RPS** -- a separate budget for each individual RPC method (most often hit on `getProgramAccounts`, `sendTransaction`, or `getBlock`).

A 429 means at least one of those budgets was exceeded. See [Rate and connection limits](../../documentation/get-started/rate-and-connection-limits.md) for the exact defaults and how to read your endpoint's live limits.

## Read the response headers

Every JSON-RPC response carries `X-Ratelimit-*` headers. Watch them in your client to back off **before** you hit a 429:

| Header | Meaning |
| --- | --- |
| `X-Ratelimit-Limit` | Total budget for the current 10-second window |
| `X-Ratelimit-Remaining` | How many total requests you have left |
| `X-Ratelimit-Reset` | Seconds until the window resets |
| `X-Ratelimit-Method-Limit` | Per-method cap for this RPC |
| `X-Ratelimit-Method-Remaining` | How many of this method you have left |

## Backoff and retry

When you do hit a 429, the right pattern is:

1. **Pause for at least 10 seconds** so the window can reset.
2. **Retry the same request** -- it didn't reach the validator, so resending is safe.
3. **Use exponential backoff** if the retry also 429s -- double the wait each attempt up to a cap (e.g. 30 seconds).
4. **Reset the backoff** once a request succeeds.

### TypeScript example

```typescript Backoff and retry
async function rpcWithBackoff(url: string, body: unknown, maxAttempts = 5) {
  let delay = 10_000; // start at 10s, the rate-limit window
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (res.status !== 429) return res.json();
    if (attempt === maxAttempts) {
      throw new Error(`429 after ${maxAttempts} attempts`);
    }
    const reset = Number(res.headers.get("X-Ratelimit-Reset")) * 1000 || delay;
    await new Promise((r) => setTimeout(r, reset));
    delay = Math.min(delay * 2, 30_000);
  }
}
```

## Reduce 429s before they happen

- **Batch reads** -- `getMultipleAccounts` instead of N parallel `getAccountInfo` calls
- **Cache hot reads** at your application layer
- **Move heavy reads** (program scans, signature crawls) to your backend
- **Lower your concurrency** until the per-method headers stop ticking near zero
- **Ask support** to raise your tier if you're consistently against the cap on legitimate traffic. Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).

## What's next

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Rate and connection limits</strong></td><td>Per-endpoint and method rate limits, plus streaming connection caps.</td><td><a href="../../documentation/get-started/rate-and-connection-limits.md">../../documentation/get-started/rate-and-connection-limits.md</a></td></tr><tr><td><strong>Common Solana errors</strong></td><td>Solana JSON-RPC error codes and how to handle each one.</td><td><a href="common-solana-errors.md">common-solana-errors.md</a></td></tr><tr><td><strong>Triton RPC error codes</strong></td><td>Triton-specific error codes you might see and what they mean.</td><td><a href="triton-rpc-error-codes.md">triton-rpc-error-codes.md</a></td></tr><tr><td><strong>How to troubleshoot</strong></td><td>The full debug flow when something's not working as expected.</td><td><a href="how-to-troubleshoot.md">how-to-troubleshoot.md</a></td></tr></tbody></table>
---
Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
Sales questions? [Contact sales](https://triton.one/contact)  
AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
