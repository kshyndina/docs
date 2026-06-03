# Trading and market making with Triton

End-to-end stack for a market-making or trading bot on Solana: real-time DEX data, earliest signal, priority fees, reliable transaction landing.

## Overview

This guide walks you through setting up Triton's trading infrastructure stack for a market-making or trading bot on Solana. You'll connect to real-time DEX data, get the earliest on-chain signal, estimate competitive priority fees, and land transactions reliably under congestion.

By the end you'll have a working setup that covers the full path from signal to fill.

## Products used in this guide

Five Triton products work together in this stack. Each card below opens the full product docs -- useful when you want to tune defaults, see every option, or troubleshoot something specific to that product.

[Dragon's Mouth](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/dragon-s-mouth-grpc)

[Deshred](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/deshred-transactions)

[Priority Fee API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/priority-fees-api)

[Jet](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/yellowstone-jet)

[Shield](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/shield-mev-protection)

## Prerequisites

{% stepper %}
{% step %}
#### A Triton account with an active endpoint

You'll need your **endpoint URL** and **token** from the [customer dashboard](https://customers.triton.one).
{% endstep %}
{% step %}
#### Basic familiarity with Solana

Accounts, transactions, compute units.
{% endstep %}
{% endstepper %}

## Step 0: Install the dependencies

{% tabs %}
{% tab title="TypeScript" %}
```bash
npm install @triton-one/yellowstone-grpc bs58 @solana/web3.js
```
{% endtab %}
{% tab title="Rust (Cargo.toml)" %}
```toml
[dependencies]
yellowstone-grpc-client = "2"
yellowstone-grpc-proto = "2"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
bs58 = "0.5"
anyhow = "1"
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
solana-client = "2"
solana-sdk = "2"
```
{% endtab %}
{% tab title="Python" %}
```bash
pip install grpcio grpcio-tools base58 solana httpx

# Generate yellowstone gRPC stubs from the proto files:
# python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. geyser.proto
# Proto files: https://github.com/rpcpool/yellowstone-grpc/tree/master/yellowstone-grpc-proto/proto
```
{% endtab %}
{% endtabs %}

## Step 1: Stream real-time DEX data with Dragon's Mouth

Dragon's Mouth delivers account and transaction updates as the node processes them, at processed commitment. For a trading bot you'll subscribe to the pool accounts and transactions of the DEX programs you're trading on.

{% tabs %}
{% tab title="stream-dex.ts" %}
```typescript

  CommitmentLevel,
  SubscribeRequest,
} from "@triton-one/yellowstone-grpc";

const ENDPOINT = "https://your-endpoint.rpcpool.com";
const TOKEN = "your-token";

// Raydium AMM v4 program -- replace with the DEX program you're trading
const RAYDIUM_AMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8";

async function streamDexData() {
  const client = new Client(ENDPOINT, TOKEN, {});
  await client.connect();
  const stream = await client.subscribe();

  const request: SubscribeRequest = {
    accounts: {
      pool_accounts: {
        account: [],
        owner: [RAYDIUM_AMM],
        filters: [],
      },
    },
    transactions: {
      dex_transactions: {
        vote: false,
        failed: false,
        accountInclude: [RAYDIUM_AMM],
        accountExclude: [],
        accountRequired: [],
      },
    },
    slots: {},
    transactionsStatus: {},
    entry: {},
    blocks: {},
    blocksMeta: {},
    commitment: CommitmentLevel.PROCESSED,
    accountsDataSlice: [],
    ping: undefined,
  };

  stream.on("data", (data) => {
    if (data.account) {
      const pubkey = bs58.encode(data.account.account!.pubkey);
      console.log("Pool state updated:", pubkey);
      // Decode and act on the account data here
    }

    if (data.transaction) {
      const sig = bs58.encode(data.transaction.transaction!.signature);
      console.log("Transaction processed:", sig);
      // Parse the transaction and look for arbitrage / copy-trade signals
    }
  });

  stream.on("error", (err) => {
    console.error("Stream error:", err);
  });

  await new Promise<void>((resolve, reject) => {
    stream.write(request, (err: Error | null) => {
      if (err) reject(err);
      else resolve();
    });
  });

  // Keep stream alive with periodic pings
  setInterval(() => {
    stream.write({ ping: { id: 1 } } as SubscribeRequest, () => {});
  }, 30_000);
}

streamDexData().catch(console.error);
```
{% endtab %}
{% tab title="stream_dex.rs" %}
```rust
use std::collections::HashMap;
use futures::StreamExt;
use yellowstone_grpc_client::GeyserGrpcClient;
use yellowstone_grpc_proto::prelude::{
    subscribe_update::UpdateOneof, CommitmentLevel, SubscribeRequest,
    SubscribeRequestFilterAccounts, SubscribeRequestFilterTransactions,
};

const ENDPOINT: &str = "https://your-endpoint.rpcpool.com";
const TOKEN: &str = "your-token";
const RAYDIUM_AMM: &str = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8";

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut client = GeyserGrpcClient::build_from_shared(ENDPOINT.to_string())?
        .x_token(Some(TOKEN.to_string()))?
        .connect()
        .await?;

    let mut accounts = HashMap::new();
    accounts.insert(
        "pool_accounts".to_string(),
        SubscribeRequestFilterAccounts {
            owner: vec![RAYDIUM_AMM.to_string()],
            ..Default::default()
        },
    );

    let mut transactions = HashMap::new();
    transactions.insert(
        "dex_transactions".to_string(),
        SubscribeRequestFilterTransactions {
            vote: Some(false),
            failed: Some(false),
            account_include: vec![RAYDIUM_AMM.to_string()],
            ..Default::default()
        },
    );

    let request = SubscribeRequest {
        accounts,
        transactions,
        commitment: Some(CommitmentLevel::Processed as i32),
        ..Default::default()
    };

    let (_tx, mut stream) = client.subscribe_with_request(Some(request)).await?;

    while let Some(Ok(msg)) = stream.next().await {
        match msg.update_oneof {
            Some(UpdateOneof::Account(acct)) => {
                let pubkey = bs58::encode(acct.account.unwrap().pubkey).into_string();
                println!("Pool state updated: {pubkey}");
            }
            Some(UpdateOneof::Transaction(tx)) => {
                let sig = bs58::encode(tx.transaction.unwrap().signature).into_string();
                println!("Transaction processed: {sig}");
            }
            _ => {}
        }
    }

    Ok(())
}
```
{% endtab %}
{% tab title="stream_dex.py" %}
```python

from grpc import aio

# Requires yellowstone gRPC Python stubs generated from the proto files.
# After running grpc_tools.protoc (see Prerequisites), the output is geyser_pb2.py
# in whatever --python_out directory you specified. Adjust the import if you placed
# it inside a package folder.
from geyser_pb2 import (
    SubscribeRequest,
    SubscribeRequestFilterAccounts,
    SubscribeRequestFilterTransactions,
    CommitmentLevel,
    SubscribeRequestPing,
)
from geyser_pb2_grpc import GeyserStub

ENDPOINT = "your-endpoint.rpcpool.com:443"
TOKEN = "your-token"
RAYDIUM_AMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

async def stream_dex_data():
    credentials = grpc.ssl_channel_credentials()
    async with aio.secure_channel(ENDPOINT, credentials) as channel:
        stub = GeyserStub(channel)
        metadata = (("x-token", TOKEN),)

        async def request_iterator():
            yield SubscribeRequest(
                accounts={
                    "pool_accounts": SubscribeRequestFilterAccounts(
                        owner=[RAYDIUM_AMM],
                    )
                },
                transactions={
                    "dex_transactions": SubscribeRequestFilterTransactions(
                        vote=False,
                        failed=False,
                        account_include=[RAYDIUM_AMM],
                    )
                },
                commitment=CommitmentLevel.PROCESSED,
            )
            while True:
                await asyncio.sleep(30)
                yield SubscribeRequest(ping=SubscribeRequestPing(id=1))

        async for update in stub.Subscribe(request_iterator(), metadata=metadata):
            if update.HasField("account"):
                pubkey = base58.b58encode(bytes(update.account.account.pubkey)).decode()
                print(f"Pool state updated: {pubkey}")
            elif update.HasField("transaction"):
                sig = base58.b58encode(bytes(update.transaction.transaction.signature)).decode()
                print(f"Transaction processed: {sig}")

asyncio.run(stream_dex_data())
```
{% endtab %}
{% endtabs %}

**Verify it works:** you should see pool state updates and transactions printing to the console within a few seconds of starting the script. If nothing appears, check your endpoint URL and token.

**What the output looks like:**

An account update prints something like:

```text Account update output
Pool state updated: 58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2
```

This is the pool's public key encoded in base58 -- the standard human-readable format for Solana addresses. The raw pool state (reserves, fees, prices) is in `data.account.account.data` as raw bytes. To use it in your trading logic, decode it against the program's account layout -- for example, the Raydium SDK or the program's Anchor IDL.

A transaction update prints:

```text Transaction update output
Transaction processed: 5Vk5mYDpFq3vQtXm8ZkRj2PnCwBsHeLfY6gNuoA1T9KdEpRsuW3HqXjc...
```

The signature is base58-encoded (64 bytes → 88 characters). The full transaction is in `data.transaction` as raw protobuf bytes. To decode it into readable JSON for parsing instructions, accounts, and token balance changes:

```typescript decode-tx.ts

const decoded = txEncode.encode(
  data.transaction.transaction!,  // SubscribeUpdateTransactionInfo (not the outer wrapper)
  txEncode.encoding.JsonParsed,
  255,  // max transaction version
  true  // include rewards
);

// decoded.transaction.message.instructions contains the swap instructions
// decoded.meta.preTokenBalances / postTokenBalances shows what changed
console.log(JSON.stringify(decoded, null, 2));
```

## Step 2: Get the earliest signal with Deshred

Deshred reconstructs transactions from shreds before execution, delivering them approximately 20 ms ahead of standard Dragon's Mouth gRPC at p90 (p50 is \~6.3 ms). It uses a separate RPC method -- `SubscribeDeshred` -- on the same endpoint and token as Dragon's Mouth.

Important limitations to understand before using Deshred:

- **No execution metadata** -- you receive intent only. There are no logs, balance changes, status, or compute unit data.
- **No finality guarantee** -- the transaction may fail, get dropped, or land on a dead fork. Always confirm with your Dragon's Mouth `processed` stream.
- **Requires Agave 4.0+** on the validator (available on Triton's paid beta).

{% tabs %}
{% tab title="stream-deshred.ts" %}
```typescript

  SubscribeRequestFilterDeshredTransactions,
} from "@triton-one/yellowstone-grpc";

const ENDPOINT = "https://your-endpoint.rpcpool.com";
const TOKEN = "your-token";
const RAYDIUM_AMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8";

async function streamDeshred() {
  const client = new Client(ENDPOINT, TOKEN, {});
  await client.connect();
  const stream = await client.subscribeDeshred();

  const request = {
    deshredTransactions: {
      dex: {
        vote: false,
        accountInclude: [RAYDIUM_AMM],
        accountExclude: [],
        accountRequired: [],
      } as SubscribeRequestFilterDeshredTransactions,
    },
  };

  stream.on("data", (data) => {
    if (data.deshredTransaction) {
      const sig = bs58.encode(
        data.deshredTransaction.transaction!.signature
      );
      console.log("Deshred tx (pre-execution):", sig, "slot:", data.deshredTransaction.slot);
    }
  });

  stream.on("error", (err) => {
    console.error("Deshred stream error:", err);
  });

  await new Promise<void>((resolve, reject) => {
    stream.write(request, (err: Error | null) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

streamDeshred().catch(console.error);
```
{% endtab %}
{% tab title="stream_deshred.rs" %}
```rust
use std::collections::HashMap;
use futures::StreamExt;
use yellowstone_grpc_client::GeyserGrpcClient;
use yellowstone_grpc_proto::prelude::{
    subscribe_update_deshred, SubscribeDeshredRequest, SubscribeRequestFilterDeshredTransactions,
};

const ENDPOINT: &str = "https://your-endpoint.rpcpool.com";
const TOKEN: &str = "your-token";
const RAYDIUM_AMM: &str = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8";

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut client = GeyserGrpcClient::build_from_shared(ENDPOINT.to_string())?
        .x_token(Some(TOKEN.to_string()))?
        .connect()
        .await?;

    let mut deshred_transactions = HashMap::new();
    deshred_transactions.insert(
        "dex".to_string(),
        SubscribeRequestFilterDeshredTransactions {
            vote: Some(false),
            account_include: vec![RAYDIUM_AMM.to_string()],
            ..Default::default()
        },
    );

    let request = SubscribeDeshredRequest {
        deshred_transactions,
        ..Default::default()
    };

    let (_sink, mut stream) = client.subscribe_deshred_with_request(Some(request)).await?;

    while let Some(Ok(msg)) = stream.next().await {
        if let Some(subscribe_update_deshred::UpdateOneof::DeshredTransaction(deshred_tx)) =
            msg.update_oneof
        {
            let sig = bs58::encode(deshred_tx.transaction.unwrap().signature).into_string();
            println!("Deshred tx (pre-execution): {} slot: {}", sig, deshred_tx.slot);
        }
    }

    Ok(())
}
```
{% endtab %}
{% tab title="stream_deshred.py" %}
```python

from grpc import aio

from geyser_pb2 import (
    SubscribeDeshredRequest,
    SubscribeRequestFilterDeshredTransactions,
    SubscribeRequestPing,
)
from geyser_pb2_grpc import GeyserStub

ENDPOINT = "your-endpoint.rpcpool.com:443"
TOKEN = "your-token"
RAYDIUM_AMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

async def stream_deshred():
    credentials = grpc.ssl_channel_credentials()
    async with aio.secure_channel(ENDPOINT, credentials) as channel:
        stub = GeyserStub(channel)
        metadata = (("x-token", TOKEN),)

        async def request_iterator():
            yield SubscribeDeshredRequest(
                deshred_transactions={
                    "dex": SubscribeRequestFilterDeshredTransactions(
                        vote=False,
                        account_include=[RAYDIUM_AMM],
                    )
                }
            )
            while True:
                await asyncio.sleep(30)
                yield SubscribeDeshredRequest(ping=SubscribeRequestPing(id=1))

        async for update in stub.SubscribeDeshred(request_iterator(), metadata=metadata):
            if update.HasField("deshred_transaction"):
                sig = base58.b58encode(
                    bytes(update.deshred_transaction.transaction.signature)
                ).decode()
                print(f"Deshred tx (pre-execution): {sig} slot: {update.deshred_transaction.slot}")

asyncio.run(stream_deshred())
```
{% endtab %}
{% endtabs %}

**Verify it works:** you should see pre-execution transactions printing before they appear in your Dragon's Mouth stream. Deshred messages arrive approximately 20 ms earlier at p90 (6.3 ms at p50).

**What the output looks like:**

```text Deshred output
Deshred tx (pre-execution): 5Vk5mYDpFq3vQtXm8ZkRj2PnCwBsHeLfY6gNuoA1T9Kd... slot: 307152834
```

The signature is base58-encoded. The transaction data in `data.deshredTransaction.transaction` contains the instructions and account keys -- you can see exactly which pools and wallets are involved, and in which direction. What you **cannot** see: whether it will succeed, what the balance changes will be, or any logs.

Use this signal to detect incoming order flow and react -- for example, detecting a large swap into a pool you're quoting. Always cross-reference with your Dragon's Mouth stream to confirm the transaction actually executed.

## Step 3: Estimate a competitive priority fee

Before building your transaction, call Triton's Priority Fee API to get a fee at your target percentile. This avoids both underbidding (transaction doesn't land) and overbidding (unnecessary cost).

{% tabs %}
{% tab title="priority-fee.ts" %}
```typescript
async function getPriorityFee(
  endpoint: string,
  token: string,
  accounts: string[],
  percentile: number // 1-10000, where 5000 = median, 9000 = 90th percentile
): Promise<number> {
  const response = await fetch(`${endpoint}/${token}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "getRecentPrioritizationFees",
      params: [accounts, { percentile }],
    }),
  });

  const { result } = await response.json();
  // result is an array of { slot, prioritizationFee } -- take the most recent
  const fees: { slot: number; prioritizationFee: number }[] = result;
  const latest = fees.sort((a, b) => b.slot - a.slot)[0];
  return latest.prioritizationFee; // micro-lamports per compute unit
}

// Example: get the 90th percentile fee for a Raydium swap
const fee = await getPriorityFee(ENDPOINT, TOKEN, [RAYDIUM_AMM], 9000);
console.log("Priority fee (90th pct):", fee, "micro-lamports/CU");
```
{% endtab %}
{% tab title="priority_fee.rs" %}
```rust
use reqwest::Client;
use serde::Deserialize;

#[derive(Deserialize)]
struct PrioritizationFee {
    slot: u64,
    #[serde(rename = "prioritizationFee")]
    prioritization_fee: u64,
}

#[derive(Deserialize)]
struct RpcResponse {
    result: Vec<PrioritizationFee>,
}

async fn get_priority_fee(
    endpoint: &str,
    token: &str,
    accounts: &[&str],
    percentile: u32, // 1-10000, where 5000 = median, 9000 = 90th percentile
) -> anyhow::Result<u64> {
    let client = Client::new();
    let url = format!("{}/{}", endpoint, token);

    let body = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPrioritizationFees",
        "params": [accounts, { "percentile": percentile }]
    });

    let mut response: RpcResponse = client
        .post(&url)
        .json(&body)
        .send()
        .await?
        .json()
        .await?;

    response.result.sort_by(|a, b| b.slot.cmp(&a.slot));
    Ok(response.result[0].prioritization_fee)
}
```
{% endtab %}
{% tab title="priority_fee.py" %}
```python

async def get_priority_fee(
    endpoint: str,
    token: str,
    accounts: list[str],
    percentile: int,  # 1-10000, where 5000 = median, 9000 = 90th percentile
) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{endpoint}/{token}",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getRecentPrioritizationFees",
                "params": [accounts, {"percentile": percentile}],
            },
        )
        fees = response.json()["result"]
        fees.sort(key=lambda x: x["slot"], reverse=True)
        return fees[0]["prioritizationFee"]
```
{% endtab %}
{% endtabs %}

**When to use which percentile** (1-10,000, where 5000 = median, 10000 = 100th percentile):

- **Normal conditions:** 5000-7500
- **Congested network or time-sensitive trade:** 9000-9500
- **Emergency / must-land:** 9900+

**Verify it works:** the call should return a non-zero number. During quiet periods fees are low; during congestion they spike significantly.

**What the output looks like:**

```text Priority fee output
Priority fee (90th pct): 45000 micro-lamports/CU
```

The fee is in micro-lamports per compute unit. A typical Raydium swap uses roughly 200,000-400,000 compute units, so 45,000 micro-lamports/CU × 300,000 CU ÷ 1,000,000,000 = \~0.0135 lamports total priority fee -- a fraction of a cent at current prices.

You can layer your own strategy on top of this (for example, adding a fixed buffer during high-volatility periods), or pass it directly to `setComputeUnitPrice` in Step 4:

```typescript Apply fee to compute budget
ComputeBudgetProgram.setComputeUnitPrice({ microLamports: fee })
```

## Step 4: Send your transaction via Jet

Jet is Triton's transaction relay engine. When you send through your Triton endpoint, Jet automatically routes to the current leader over QUIC, handles connection caching, leader schedule tracking, and retry fanout. SWQoS is included -- no extra configuration needed.

{% tabs %}
{% tab title="send-jet.ts" %}
```typescript

  Connection,
  ComputeBudgetProgram,
  Transaction,
} from "@solana/web3.js";

async function sendWithJet(
  serializedTransaction: Buffer,
  endpoint: string,
  token: string
): Promise<string> {
  // Use your Triton endpoint -- Jet routing is handled automatically
  const connection = new Connection(`${endpoint}/${token}`, "confirmed");

  const signature = await connection.sendRawTransaction(
    serializedTransaction,
    {
      skipPreflight: true, // simulate separately via simulateTransaction() if needed
      maxRetries: 0,       // disable server-side retries; implement your own retry logic instead
    }
  );

  console.log("Sent:", signature);
  return signature;
}

// Add the priority fee from Step 3 to your transaction
function addPriorityFee(tx: Transaction, microLamportsPerCU: number): void {
  tx.add(
    ComputeBudgetProgram.setComputeUnitPrice({
      microLamports: microLamportsPerCU,
    })
  );
}
```
{% endtab %}
{% tab title="send_jet.rs" %}
```rust
use solana_client::rpc_client::RpcClient;
use solana_client::rpc_config::RpcSendTransactionConfig;
use solana_sdk::transaction::Transaction;

fn send_with_jet(
    transaction: &Transaction,
    endpoint: &str,
    token: &str,
) -> anyhow::Result<String> {
    let rpc_url = format!("{}/{}", endpoint, token);
    let client = RpcClient::new(rpc_url);

    let signature = client.send_transaction_with_config(
        transaction,
        RpcSendTransactionConfig {
            skip_preflight: true,
            max_retries: Some(0), // disable server-side retries; implement your own retry logic
            ..Default::default()
        },
    )?;

    println!("Sent: {}", signature);
    Ok(signature.to_string())
}
```
{% endtab %}
{% tab title="send_jet.py" %}
```python
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

def send_with_jet(serialized_tx: bytes, endpoint: str, token: str) -> str:
    client = Client(f"{endpoint}/{token}")
    response = client.send_raw_transaction(
        serialized_tx,
        opts=TxOpts(skip_preflight=True, max_retries=0),
    )
    signature = str(response.value)
    print(f"Sent: {signature}")
    return signature
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Set `maxRetries: 0` to disable server-side retries, then implement your own retry logic (re-fetch a recent blockhash and re-sign every few seconds). There is a known issue with the Agave `sendTx` library where server-side retry queues overflow under congestion -- client-managed retries are more reliable and give your strategy direct control.
{% endhint %}

**Verify it works:** the signature should appear on-chain within 1-3 slots under normal conditions. Check at solscan.io or via `getSignatureStatuses`.

**What the output looks like:**

```text Send output
Sent: 5Vk5mYDpFq3vQtXm8ZkRj2PnCwBsHeLfY6gNuoA1T9KdEpRsuW3HqXjc...
```

This is the transaction signature -- base58-encoded, 88 characters. To confirm it landed and check for errors:

```typescript confirm-tx.ts
const statuses = await connection.getSignatureStatuses([signature]);
const status = statuses.value[0];

if (status?.confirmationStatus === "confirmed" || status?.confirmationStatus === "finalized") {
  console.log("Landed:", signature);
} else if (status?.err) {
  console.error("Failed:", status.err);
  // Re-fetch a recent blockhash, re-sign, and resend
}
```

Because you set `maxRetries: 0`, retry logic is entirely in your hands. If the transaction hasn't confirmed within \~30 seconds (the blockhash expiry window), re-fetch a recent blockhash from `confirmed` or `finalized` commitment, re-sign the transaction, and resend.

## Putting it together

A minimal trading loop combining all four steps:

```typescript trading-loop.ts

const ENDPOINT = "https://your-endpoint.rpcpool.com";
const TOKEN = "your-token";
const RAYDIUM_AMM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8";

async function getPriorityFee(
  endpoint: string,
  token: string,
  accounts: string[],
  percentile: number
): Promise<number> {
  const response = await fetch(`${endpoint}/${token}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "getRecentPrioritizationFees",
      params: [accounts, { percentile }],
    }),
  });
  const { result } = await response.json();
  const fees: { slot: number; prioritizationFee: number }[] = result;
  return fees.sort((a, b) => b.slot - a.slot)[0].prioritizationFee;
}

async function tradingLoop() {
  const connection = new Connection(`${ENDPOINT}/${TOKEN}`, "confirmed");
  const client = new Client(ENDPOINT, TOKEN, {});
  await client.connect();
  const stream = await client.subscribe();

  stream.on("data", async (data) => {
    if (!data.transaction) return;

    // 1. Signal detected -- decide if you want to act
    const shouldTrade = analyseTransaction(data.transaction);
    if (!shouldTrade) return;

    // 2. Get competitive priority fee
    const fee = await getPriorityFee(ENDPOINT, TOKEN, [RAYDIUM_AMM], 9000);

    // 3. Build your transaction
    const tx = new Transaction();
    tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: fee }));
    // ... add your swap instruction here

    // 4. Send via Jet
    const sig = await connection.sendRawTransaction(tx.serialize(), {
      skipPreflight: true,
      maxRetries: 0,
    });

    console.log("Sent:", sig);
  });

  // Subscribe request (same as Step 1)
  await new Promise<void>((resolve, reject) => {
    stream.write(
      {
        accounts: {},
        transactions: {
          dex_transactions: {
            vote: false,
            failed: false,
            accountInclude: [RAYDIUM_AMM],
            accountExclude: [],
            accountRequired: [],
          },
        },
        slots: {},
        transactionsStatus: {},
        entry: {},
        blocks: {},
        blocksMeta: {},
        commitment: CommitmentLevel.PROCESSED,
        accountsDataSlice: [],
        ping: undefined,
      },
      (err: Error | null) => {
        if (err) reject(err);
        else resolve();
      }
    );
  });
}

function analyseTransaction(tx: any): boolean {
  // Your signal logic here
  return true;
}

tradingLoop().catch(console.error);
```

## Prefer a faster path to market?

If you'd rather go live without building your own routing and quoting logic, Triton's Metis and Titan APIs cover real-time routing across 20+ DEXes and RFQ providers, with DART live on-chain re-optimisation and quote streaming over WebSockets -- all out of the box.

Two paths for two types of teams:

- **This guide** -- build your own signal and execution stack. Full control, lowest latency, more engineering work.
- **Metis / Titan** -- plug in pre-built liquidity routing and quoting. Fastest time to market, less custom code.

[Metis swap API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/metis-swap-api)

[Titan swap API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/titan-swap-api)

## FAQs

<details>
<summary>Do I need all four products?</summary>

Dragon's Mouth and Jet cover the minimum -- real-time data in, transactions out. Add Deshred if your strategy depends on acting before the network processes a transaction. Priority Fee API prevents you from overbidding during quiet periods.

</details>

<details>
<summary>How do I pick the right percentile?</summary>

Start at 7500 (75th percentile) and monitor landing rate. Increase to 9000+ during congestion or when latency matters more than cost.

</details>

<details>
<summary>Should I configure retries when sending?</summary>

Set `maxRetries: 0` to disable server-side retries, then implement your own retry logic in your application code -- re-fetch a recent blockhash and re-sign every few seconds. There is a known issue with the Agave `sendTx` library where server-side retry queues overflow under congestion, making client-managed retries more reliable.

</details>

<details>
<summary>Can I use this with Orca or other DEXes?</summary>

Yes -- replace the Raydium AMM program address with the program address of any DEX.

Orca Whirlpools: `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc`

</details>

## What's next

[Deshred transactions](https://kate-6.gitbook.io/triton-one-docs/documentation/streaming-data/deshred-transactions)

[Shield MEV protection](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/shield-mev-protection)

[Metis swap API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/metis-swap-api)

[Titan swap API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/titan-swap-api)

---
🛟 Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)  
⚙️ Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)  
💼 Sales questions? [Contact sales](https://triton.one/contact)  
✨ AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)  
📡 Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
