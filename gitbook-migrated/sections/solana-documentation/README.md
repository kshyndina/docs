# Solana quickstart

Got your endpoint? Here's the fastest path to your first Solana response on Triton.

1. Grab your endpoint URL and token from the customer portal (see **Get started**).
2. Make your first call:

```bash
curl https://your-endpoint.rpcpool.com/<token> -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getBalance","params":["11111111111111111111111111111111"]}'
```

3. From here, pick the product that matches what you're building: real-time streaming, reading account state, historical data, or sending transactions.
