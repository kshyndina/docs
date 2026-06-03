# Verify your gRPC endpoint

Use Triton's known-good Linux test client to figure out whether a gRPC error is on your endpoint or in your application code.

If your gRPC subscription is throwing errors and you're not sure whether the endpoint or your code is at fault, use Triton's prebuilt test client. It's a small CLI we ship for exactly this purpose -- known-good code that runs on your machine and hits your endpoint with the same gRPC subscription patterns your app does.

**The logic:** if the test client errors, the issue is on the endpoint and we should look at it. If it streams cleanly, the issue is in your application code.

## Download

The client is a prebuilt binary for Ubuntu 22.04 and 24.04. Download from the [yellowstone-grpc releases page](https://github.com/rpcpool/yellowstone-grpc/releases).

It runs on Linux only. If your backend runs on a different OS, run the client on a temporary Linux box (a small VM or container is enough) -- the goal is just to send a known-good request from anywhere and see what comes back.

## Run a subscription

Subscribe to all account writes and slot updates:

```shell
./client-ubuntu-22.04 --endpoint https://<your-endpoint> --x-token <your-token> subscribe --accounts --slots
```

Subscribe to a specific program (e.g. Raydium):

```shell
./client-ubuntu-22.04 --endpoint https://<your-endpoint> --x-token <your-token> subscribe --accounts --slots --accounts-owner 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8
```

Add `--stats` to see total accounts, slots, and bandwidth in real time:

```shell
./client-ubuntu-22.04 --endpoint https://<your-endpoint> --x-token <your-token> subscribe --accounts --slots --stats
```

## Interpreting the result

- **Stream is healthy, events are flowing.** The endpoint is fine. The error is in your application code -- most often a filter that doesn't match what you think it does, an outdated client SDK version, or a parser that mis-handles a Protobuf field. Re-check your subscribe request and your data handler.
- **Stream errors or won't connect.** Open a chat in your [customer dashboard](https://customers.triton.one) and include the exact `client-ubuntu` command you ran plus the error output. Because the client is our code, we know where to look on our end.

## Why we ship this

A common support ticket pattern: a customer reports a gRPC error, we ask for their code, and we end up debugging hundreds of lines of someone else's application. The test client cuts through that. It's a baseline -- when both sides know the client itself is correct, the conversation jumps straight to whether the endpoint or the customer's code has the issue.

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Click the chat icon in the bottom right of your [dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
