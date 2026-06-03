# How to troubleshoot

A step-by-step process to diagnose and fix issues with your Triton One RPC.

## Reality check -- ensure your setup is correct and as expected

- Verify that you're using the correct RPC endpoint, headers, and authorization token.
- Double-check if your request format, parameters, and input data are correct.
- Ensure your code compiles without any errors and warnings with side effects.
- Review your code for possible logical bugs not caught by the compiler.

## Troubleshooting -- determine the cause of your errors

First, determine if the error is Solana-wide or specific to Triton by attempting the same method against the Solana public RPC `https://api.mainnet-beta.solana.com`.

If the same issue exists with Solana, identify the bug and resolution by following the standard list of [Common Solana JSON-RPC codes](common-solana-errors.md).

If you fail to resolve your issue on Solana's public RPC, it's time to troubleshoot with possible and known Triton One errors:

- Determine if your issue returns any of the [Triton RPC error codes](triton-rpc-error-codes.md).
- Determine if your issue exhibits any of the [possible Triton RPC symptoms](triton-rpc-error-codes.md).
- Determine if your issue fits any of the [uncommon Web3JS errors](common-solana-errors.md) we helped some of our customers resolve.

If you fail to resolve your issue despite the steps above, it's time to call in the big guns!

## Reach out -- seek help from the Triton One support team

Prepare the following information:

- Which endpoint are you using?
- Which token or origin are you using for authentication?
- Which service are you using (HTTP, WebSocket, gRPC, etc)?
- Which error are you receiving?
- When did it happen (please include the date, time and timezone)?
- What is the expected result?
- If your issue is related to latency, how did you measure it?

In your customer dashboard at the bottom right, open a chat with us. Please include all of the info above so we can investigate and get back to you with something helpful as quickly as possible!

[Log in to Triton One](https://customers.triton.one)

---
<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
<i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
<i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)  
<i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
<i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
