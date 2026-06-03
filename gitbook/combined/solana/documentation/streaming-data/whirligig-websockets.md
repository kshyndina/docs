# Whirligig WebSockets

Better, faster Solana WebSockets. Whirligig is a Rust-based proxy between Dragon's Mouth gRPC and a WebSocket client, with intra-slot updates at processed commitment.

{% hint style="warning" %}
**Work in progress.** This page is being reviewed -- don't reference it yet, copy isn't final.
{% endhint %}

## What is Whirligig

Whirligig is a Rust-based proxy between a Dragon's Mouth gRPC server and a WebSocket client. It lets clients send requests over a WebSocket connection rather than over gRPC. Useful when WebSockets are preferred, such as in a Web3 application.

At the `processed` commitment level most traders use, Whirligig delivers intra-slot updates. Account updates arrive up to 400ms faster than the previous Solana WebSocket subscriptions.

For a backend that can speak gRPC, [Dragon's Mouth gRPC](dragon-s-mouth-grpc.md) is the lower-latency path. Whirligig exists for browsers and any client that can't use gRPC.

## Features and benefits

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-plug">:plug:</i> <strong>Solana WebSocket compatible</strong></td><td>Drop-in replacement for the standard Solana WebSocket API. All native methods plus Triton-only extensions.</td><td></td></tr><tr><td><i class="fa-bell">:bell:</i> <strong>transactionSubscribe extension</strong></td><td>Triton-only subscription for filtered transaction notifications over WebSocket.</td><td></td></tr><tr><td><i class="fa-signal-high">:signal-high:</i> <strong>All commitment levels</strong></td><td>Subscribe at processed, confirmed, or finalized. Pick the trade-off that fits the workload.</td><td></td></tr><tr><td><i class="fa-network">:network:</i> <strong>Reliability and limits at scale</strong></td><td>Higher reliability and connection limits at scale, backed by Yellowstone gRPC.</td><td></td></tr></tbody></table>
## Endpoint and connection

The default endpoint is:

```text
wss://<your-endpoint>.rpcpool.com/<token>/whirligig
```

To use Whirligig, append `/whirligig` to your RPC endpoint. With `web3.js`, pass a custom WS endpoint:

```javascript
new web3.Connection('rpc_endpoint', { wsEndpoint: 'ws_endpoint' })
```

{% hint style="info" %}
Some client software requires a trailing slash, like `/whirligig/`.
{% endhint %}

{% hint style="info" %}
Connections inactive for over 60 seconds get closed. To keep a connection alive, ping the server with `{"jsonrpc":"2.0","method":"ping"}`.
{% endhint %}

### WebSocket API

Whirligig aims for full compatibility with the [Solana WebSocket API](https://docs.solana.com/api/websocket). Note one extended subscription Triton introduced: `transactionSubscribe`. This subscription may not be compatible with other providers.

### Commitment levels

Whirligig supports all three commitment levels: `processed`, `confirmed`, `finalized`. You can also [manage commitment levels](dragon-s-mouth-grpc.md) in your app, the same way as for Dragon's Mouth gRPC. Each subscribe method has a corresponding unsubscribe method that takes the subscription id returned by `subscribe`.

Reference: [Solana cluster commitments](https://docs.solana.com/cluster/commitments).

| Level | Definition |
| --- | --- |
| **Processed** | The highest slot of the heaviest fork processed by the node. Ledger state at this slot is not derived from a confirmed or finalized block, but if multiple forks are present, is from the fork the validator believes is most likely to finalize. |
| **Confirmed** | The highest slot voted on by a supermajority of the cluster. Confirmation incorporates votes from gossip and replay. It does not count votes on descendants of a block, only direct votes on that block, and upholds "optimistic confirmation" guarantees in release 1.3 and onwards. |
| **Finalized** | The highest slot having reached max vote lockout, as recognised by a supermajority of the cluster. |

## Unsubscribe

Every subscription request returns the subscription `id` on success:

```json
{
  "jsonrpc": "2.0",
  "result": 42,
  "id": 1
}
```

Use that `id` to unsubscribe:

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "slotUnsubscribe",
  "params": [42]
}
```

The result is `true` if the subscription was active and removed, `false` if it didn't exist:

```json
{
  "jsonrpc": "2.0",
  "result": true,
  "id": 1
}
```

The same pattern applies to `accountUnsubscribe`, `blockUnsubscribe`, `logsUnsubscribe`, `programUnsubscribe`, `signatureUnsubscribe`, `transactionUnsubscribe` -- pass the `id` from the matching subscribe call.

## Subscription methods

The JSON below is the wire format sent over the WebSocket. The same pattern works in any client language: open a WebSocket to the endpoint above, send the JSON request, parse JSON notifications. Concrete `accountSubscribe` connect-and-consume examples in TypeScript and Rust are in the [streaming quickstart](quickstart.md). For the full reference of every method, see [Solana's WebSocket API](https://docs.solana.com/api/websocket) -- Whirligig is wire-compatible plus the `transactionSubscribe` extension below.

### accountSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.account_subscribe).

```json Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "accountSubscribe",
  "params": [
    "SysvarC1ock11111111111111111111111111111111",
    {
      "encoding": "base58",
      "commitment": "finalized"
    }
  ]
}
```

`base58` stream data example:

```json Response
{
  "jsonrpc": "2.0",
  "method": "accountNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206122916
      },
      "value": {
        "data": [
          "9AAG2zomYcUVKQfondw13yz193crQ5R5zmzdEojhMPXiyYEjD8viLrb",
          "base58"
        ],
        "executable": false,
        "lamports": 1169280,
        "owner": "Sysvar1111111111111111111111111111111111111",
        "rentEpoch": 361,
        "space": 40
      }
    },
    "subscription": 0
  }
}
```

### blockSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.block_subscribe).

```json Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "blockSubscribe",
  "params": [
    "all",
    {
      "commitment": "finalized",
      "maxSupportedTransactionVersion": 1,
      "showRewards": false,
      "transactionDetails": "none"
    }
  ]
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "blockNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206125999
      },
      "value": {
        "block": {
          "blockHeight": 188652385,
          "blockTime": 1689709529,
          "blockhash": "74iqy9xdFvenLkFizkoBkkLRWTyygEeCiiN3B8Z8ma2D",
          "parentSlot": 206125998,
          "previousBlockhash": "Cq5nfgu9Y5KF47J9qj5CTYmt8D5CxBpw8HCRqQZ7o7i9"
        },
        "err": null,
        "slot": 206125999
      }
    },
    "subscription": 0
  }
}
```

### logsSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.logs_subscribe).

```json Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "logsSubscribe",
  "params": [
    {
      "mentions": ["8BnEgHoWFysVcuFFX7QztDmzuH8r5ZFvyP3sYwn1XTh6"]
    },
    {
      "commitment": "finalized"
    }
  ]
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "logsNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206126709
      },
      "value": {
        "err": null,
        "logs": [
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj invoke [1]",
          "Program log: process_instruction: FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj: 3 accounts, data=[12]",
          "Program log: Instruction: UpdateLendingPool",
          "Program log: current_borrow_rate: 73081853393945351",
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj consumed 23800 of 1000000 compute units",
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj success",
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj invoke [1]",
          "Program log: process_instruction: FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj: 3 accounts, data=[12]",
          "Program log: Instruction: UpdateLendingPool",
          "Program log: current_borrow_rate: 82164236984041212",
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj consumed 28159 of 976200 compute units",
          "Program FC81tbGt6JWRXidaWYFXxGnTk4VgobhJHATvTRVMqgWj success",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N invoke [1]",
          "Program log: Instruction: LiquidateUnstakeLp",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
          "Program log: Instruction: Transfer",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4740 of 879873 compute units",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N consumed 79765 of 948041 compute units",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N success",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N invoke [1]",
          "Program log: Instruction: RemoveLiquidity",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N consumed 24767 of 868276 compute units",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N success",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N invoke [1]",
          "Program log: Instruction: SwapAndWithdraw",
          "Program log: withdraw_type: 2,\\n            user_info.pending_repay_0: 0,\\n            user_info.pending_repay_1: 0,\\n            user_info.tkn_0: 0,\\n            user_info.tkn_1: 0,\\n            ",
          "Program log: swap_direction: 0,\\n            amount_in: 0\\n            ",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
          "Program log: Instruction: Transfer",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4785 of 815778 compute units",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
          "Program log: Instruction: Transfer",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4831 of 807689 compute units",
          "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N consumed 47497 of 843509 compute units",
          "Program 2nAAsYdXF3eTQzaeUQS3fr4o782dDg8L28mX39Wr5j8N success"
        ],
        "signature": "5UPB2AEWgUafVDEw2xTkup8CUedxCMNL4k7EMuxtcyi1WnYLmpXeYUfBANpnPnpSz6LRwwLnBQf7tViKSFT7ojiB"
      }
    },
    "subscription": 0
  }
}
```

### programSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.program_subscribe).

```json Request
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "programSubscribe",
  "params": [
    "srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX",
    {
      "encoding": "base64+zstd",
      "commitment": "finalized"
    }
  ]
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "programNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206127070
      },
      "value": {
        "account": {
          "data": [
            "KLUv/QBYDQEAkHNlcnVtQQABAAQAcGFkZGluZwUA03+gI0CxQgAYeABG",
            "base64+zstd"
          ],
          "executable": false,
          "lamports": 457104960,
          "owner": "srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX",
          "rentEpoch": 0,
          "space": 65548
        },
        "pubkey": "5qRKrGPYaQmazdtMnia1iC3gFbpgW4CT7KPrHq9nJGm5"
      }
    },
    "subscription": 0
  }
}
```

### signatureSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.signature_subscribe).

```json Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "signatureSubscribe",
  "params": [
    "2EBVM6cB8vAAD93Ktr6Vd8p67XPbQzCJX47MpReuiCXJAtcjaxpvWpcg9Ege1Nr5Tk3a2GFrByT7WPBjdsTycY9b",
    {
      "commitment": "finalized"
    }
  ]
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "signatureNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206127070
      },
      "value": {
        "err": null
      }
    },
    "subscription": 24006
  }
}
```

### slotSubscribe

Fully compatible with the Solana WebSocket API. [API details](https://docs.rs/solana-client/latest/solana_client/nonblocking/pubsub_client/struct.PubsubClient.html#method.slot_subscribe).

```json Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "slotSubscribe"
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "slotNotification",
  "params": {
    "result": {
      "parent": 206128153,
      "root": 206128115,
      "slot": 206128154
    },
    "subscription": 0
  }
}
```

### transactionSubscribe

{% hint style="warning" %}
The Solana WebSocket API does not support this kind of subscription. It is a Triton extension and may not be compatible with other providers.
{% endhint %}

Accepts two arguments: `filter` (all fields optional) and `config` (equivalent to [`RpcBlockSubscribeConfig`](https://docs.rs/solana-client/latest/solana_client/rpc_config/struct.RpcBlockSubscribeConfig.html)).

```json Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "transactionSubscribe",
  "params": [
    {
      "vote": false,
      "failed": false,
      "signature": "2EBVM6cB8vAAD93Ktr6Vd8p67XPbQzCJX47MpReuiCXJAtcjaxpvWpcg9Ege1Nr5Tk3a2GFrByT7WPBjdsTycY9b",
      "accounts": {
        "include": ["5qRKrGPYaQmazdtMnia1iC3gFbpgW4CT7KPrHq9nJGm5"],
        "exclude": ["srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX"],
        "required": ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"]
      }
    },
    {
      "commitment": "processed",
      "encoding": "base58",
      "transactionDetails": "full",
      "showRewards": false,
      "maxSupportedTransactionVersion": 1
    }
  ]
}
```

```json Response
{
  "jsonrpc": "2.0",
  "method": "transactionNotification",
  "params": {
    "result": {
      "context": {
        "apiVersion": "1.16.1",
        "slot": 206132915
      },
      "value": {
        "slot": 241068727,
        "signature": "2EBVM6cB8vAAD93Ktr6Vd8p67XPbQzCJX47MpReuiCXJAtcjaxpvWpcg9Ege1Nr5Tk3a2GFrByT7WPBjdsTycY9b",
        "transaction": {
          "meta": {
            "computeUnitsConsumed": 27426,
            "err": null,
            "fee": 5000,
            "innerInstructions": [
              {
                "index": 3,
                "instructions": [
                  {
                    "accounts": [7, 3, 11],
                    "data": "3DTZbgwsozUF",
                    "programIdIndex": 15,
                    "stackHeight": null
                  },
                  {
                    "accounts": [9, 8, 11],
                    "data": "3DTZbgwsozUF",
                    "programIdIndex": 15,
                    "stackHeight": null
                  }
                ]
              }
            ],
            "loadedAddresses": {
              "readonly": [],
              "writable": []
            },
            "logMessages": [
              "Program ComputeBudget111111111111111111111111111111 invoke [1]",
              "Program ComputeBudget111111111111111111111111111111 success",
              "Program GDDMwNyyx8uB6zrqwBFHjLLG3TBYk2F8Az4yrQC5RzMp invoke [1]",
              "Program log: Sequence in order | sequence_num=755609 | last_known=755608",
              "Program GDDMwNyyx8uB6zrqwBFHjLLG3TBYk2F8Az4yrQC5RzMp consumed 3398 of 300000 compute units",
              "Program GDDMwNyyx8uB6zrqwBFHjLLG3TBYk2F8Az4yrQC5RzMp success",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX invoke [1]",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX consumed 3820 of 296602 compute units",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX success",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX invoke [1]",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
              "Program log: Instruction: Transfer",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4740 of 285091 compute units",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
              "Program log: Instruction: Transfer",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 4740 of 277786 compute units",
              "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX consumed 20208 of 292782 compute units",
              "Program srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX success"
            ],
            "postBalances": [
              10194778999, 1224960, 457104960, 2039280, 23357760, 1825496640,
              3591360, 2039280, 2039280, 2039280, 457104960, 0, 1, 1141440,
              1141440, 934087680
            ],
            "postTokenBalances": [
              {
                "accountIndex": 3,
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "ASx1wk74GLZsxVrYiBkNKiViPLjnJQVGxKrudRgPir4A",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "4973704995974757",
                  "decimals": 5,
                  "uiAmount": 49737049959.74757,
                  "uiAmountString": "49737049959.74757"
                }
              },
              {
                "accountIndex": 7,
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "3oQLKk1TyyXMT14p2i8p95v5jKqsQ5qzZGwxZCTnFC7p",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "3167826900000000",
                  "decimals": 5,
                  "uiAmount": 31678269000,
                  "uiAmountString": "31678269000"
                }
              },
              {
                "accountIndex": 8,
                "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "owner": "ASx1wk74GLZsxVrYiBkNKiViPLjnJQVGxKrudRgPir4A",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "148629334218",
                  "decimals": 6,
                  "uiAmount": 148629.334218,
                  "uiAmountString": "148629.334218"
                }
              },
              {
                "accountIndex": 9,
                "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "owner": "3oQLKk1TyyXMT14p2i8p95v5jKqsQ5qzZGwxZCTnFC7p",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "5797710875",
                  "decimals": 6,
                  "uiAmount": 5797.710875,
                  "uiAmountString": "5797.710875"
                }
              }
            ],
            "preBalances": [
              10194783999, 1224960, 457104960, 2039280, 23357760, 1825496640,
              3591360, 2039280, 2039280, 2039280, 457104960, 0, 1, 1141440,
              1141440, 934087680
            ],
            "preTokenBalances": [
              {
                "accountIndex": 3,
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "ASx1wk74GLZsxVrYiBkNKiViPLjnJQVGxKrudRgPir4A",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "4973704995974757",
                  "decimals": 5,
                  "uiAmount": 49737049959.74757,
                  "uiAmountString": "49737049959.74757"
                }
              },
              {
                "accountIndex": 7,
                "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "owner": "3oQLKk1TyyXMT14p2i8p95v5jKqsQ5qzZGwxZCTnFC7p",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "3167826900000000",
                  "decimals": 5,
                  "uiAmount": 31678269000,
                  "uiAmountString": "31678269000"
                }
              },
              {
                "accountIndex": 8,
                "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "owner": "ASx1wk74GLZsxVrYiBkNKiViPLjnJQVGxKrudRgPir4A",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "148629334218",
                  "decimals": 6,
                  "uiAmount": 148629.334218,
                  "uiAmountString": "148629.334218"
                }
              },
              {
                "accountIndex": 9,
                "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "owner": "3oQLKk1TyyXMT14p2i8p95v5jKqsQ5qzZGwxZCTnFC7p",
                "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                "uiTokenAmount": {
                  "amount": "5797710875",
                  "decimals": 6,
                  "uiAmount": 5797.710875,
                  "uiAmountString": "5797.710875"
                }
              }
            ],
            "rewards": null,
            "status": {
              "Ok": null
            }
          },
          "transaction": [
            "nMXJYDy61Acdo2FY39i2ENUwNCMDYBWgRi6dNBgJdMHv7NgY4jUS6uwa9YMzyen1nzANm35qQSr189ykkvNzEFRhrULEwNxXA39HRS8JjYwEdUQ7ziXT2bqnFCeJc5rtk2uS7rbrrvEANjeDJ8PVkdJW9ZrxTcpg3nY3S5uVi6t7N2aB2eDmyju1cyRRU5T1aiT9vH1MHornT53XSe9UzuXFEP4sXfJjHovtucUkjqpJqU1PnKcrfK98wNT1Li6zjS8XGreRYNz5N8nNuxhVxFUM9CxQVurQQ3mhAiSYUmsptNgM5RqwSsy1CwebfZRpc35qThUtyu55TGyXh7MAgA8sJCfBrTDCgtWChaDkyqpggKPQ8VnCgLQdPBMwaady3cF3GgMvCpue5ryFW2p3EYgZxME7j6FTgBRjYRd6LuyeyhWp68fsNscYbMY8eZnV6WVVpSoBUpxg9FnyEpCatgS9ZNiTX3Wb8K3Dg4ncxmVutegbxn9uKbEvBNUWn5KV5m2jbmJmSafmMAJrFW3m4pv2HAKHezcEPfNNMCrK5J4Jjjg2JqQBKK9Z1PddhAX4CConAnbF7ZY4xkFnpWVpVi8cJrR6Wsa6VPDMpgzraukYmnwHgrBNx2bQokeZxmpyb7j2f6mWkreQcLZFFDx5tP33XbwSQqNFvtQZzUDJ2zYwMhZmCuN3E4vFgWQgU3Sb9jepy8ev9LniReyPdJRRRGbkJegdxYkbE2XDb3R2p9PF3um3LrKP35MeJgKoDrNBG6UAe6M5Q3cP7JfZGgZVud9GQcVGdnBa9ZbQJyojHnMbV4TDNmi2526dXoi5XqfUhNkrc1PgnAzrKzwZmNyiCX12SSUZLKzgzJTnk7C4gavYNSvhpNcupQyrLEnJf9FkQwhv1uN4WAsYdym6rR5oLuZet9bnebNvJCPWRCT4H59Yrm8y1QTF64hiB9zWazhLawAKAtYdBKteW9gr8BstGDUuo8QRMTyb3jBJYhdoeiKMqZWo",
            "base58"
          ]
        },
        "error": null
      }
    },
    "subscription": 0
  }
}
```

## Whirligig CLI client

The Whirligig CLI client lives on GitHub: [yellowstone-whirligig-client](https://github.com/rpcpool/yellowstone-whirligig-client).

## Related

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><i class="fa-play">:play:</i> <strong>Streaming quickstart</strong></td><td>Test every Triton streaming service in under five minutes.</td><td><a href="quickstart.md">quickstart.md</a></td></tr><tr><td><i class="fa-radio">:radio:</i> <strong>Dragon's Mouth gRPC</strong></td><td>Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC.</td><td><a href="dragon-s-mouth-grpc.md">dragon-s-mouth-grpc.md</a></td></tr><tr><td><i class="fa-layer-group">:layer-group:</i> <strong>Fumarole reliable streams</strong></td><td>Redundant streaming layer with 96h of stored data and built-in cursor resume.</td><td><a href="fumarole-persistent-streams.md">fumarole-persistent-streams.md</a></td></tr><tr><td><i class="fa-compass">:compass:</i> <strong>Streaming overview</strong></td><td>Compare every Triton streaming service side by side.</td><td><a href="overview.md">overview.md</a></td></tr></tbody></table>
---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
