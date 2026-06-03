# Common Solana errors

Standard list of common JSON-RPC error codes you may experience, plus uncommon Web3JS errors we have previously helped customers resolve.

## Common Solana JSON-RPC codes

This is a standard list of common JSON-RPC error codes you may experience. For a comprehensive list, please refer to [Anza's kit repository](https://github.com/anza-xyz/kit).

| Error code | Suggested action |
| --- | --- |
| -32001 | Ensure your transaction uses the latest Solana transaction version. |
| -32002 | Ensure all required signatures are present and valid. |
| -32003 | Verify keypair, rebuild the transaction with a current blockhash and sign it immediately before submission, check signatures format, and simulate first. |
| -32601 | Method not found > the method you are trying to use is either invalid or does not exist. Verify the method is enabled in your custom RPC configuration. |
| -32602 | Invalid method parameter(s). Double-check your request format against Solana's JSON-RPC spec. |
| -32603 | Internal JSON-RPC error. Retry the request after a short delay. |
| -32604 | Procedure is method > ID field not provided in the request, please check your configuration. |
| -32700 | JSON parse error > JSON received from the server fails to be parsed. Check your JSON structure. |

## List of uncommon Web3JS errors

Here are some uncommon `@solana/web3.js` errors we have previously helped our customers with, which might help you troubleshoot your problem.

### Port exhaustion in NodeJS

Suppose you're running high-throughput asynchronous loads in a NodeJS environment. In that case, you might find yourself getting persistent socket and connection errors such as: `ECONNREFUSED`, `ECONNRESET`, Connection Timeout Error, other side closed, fetch failed.

If so, Triton One provides a comprehensive guide on why this occurs and a list of steps you can take to fix the problem in its documentation.

---
<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
<i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
<i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)  
<i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
<i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
