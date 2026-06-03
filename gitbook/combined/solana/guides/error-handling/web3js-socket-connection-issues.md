# Web3JS socket/connection issues

Why high-throughput Solana web3.js apps in NodeJS hit ECONNREFUSED, ECONNRESET, fetch failed, and how to fix it with connection pooling.

If you are running high-throughput applications using [`@solana/web3.js`](https://www.npmjs.com/package/@solana/web3.js) in a NodeJS environment, you may encounter persistent socket or connection errors, especially under heavy asynchronous load. This guide explains the root cause of these issues and provides several effective solutions.

## Common errors

These errors often manifest with messages like `fetch failed`, `Connect Timeout Error`, `ECONNREFUSED`, `ECONNRESET`, or `other side closed`. They are a strong indicator that your application is hitting local system limits for network connections.

<details>
<summary>Click to see full error examples</summary>

```text
cause: ConnectTimeoutError: Connect Timeout Error
code: 'UND_ERR_CONNECT_TIMEOUT'
```

```text
cause: Error: connect ECONNREFUSED 1.2.3.4:443
code: 'ECONNREFUSED'
```

```text
cause: Error: Client network socket disconnected before secure TLS connection was established
code: 'ECONNRESET'
```

```text
cause: SocketError: other side closed
code: 'UND_ERR_SOCKET'
```

</details>

## The root cause: port exhaustion in NodeJS

These errors are not caused by the RPC node or the [`@solana/web3.js`](https://www.npmjs.com/package/@solana/web3.js) library itself. They stem from **NodeJS's implementation of `fetch`**, which uses the `undici` HTTP client. By default, [`undici`](https://www.npmjs.com/package/undici) aggressively opens a new TCP socket for each outgoing request.

Under heavy, concurrent load, this behaviour can quickly **exhaust the available ephemeral ports** on your operating system, leading to the connection failures you see.

## Diagnosing the issue

You can check how many ports your Node process is using on a UNIX-based system with the following command. A high number (in the thousands) is a clear sign of this issue.

```bash
lsof -i -n -P | grep node | awk '{print $9}' | awk -F '->' '{print $1}' | \
awk -F ':' '{print $2}' | sort -u | wc -l
```

## External references

This is a known issue related to connection management in `undici`. You can find more context in these community discussions and articles:

- [GitHub Issue: `undici` hangs/times out when under heavy load](https://github.com/nodejs/undici/issues/583)
- [GitHub Issue: `UND_ERR_SOCKET` on `fetch`](https://github.com/nodejs/undici/issues/2412)
- [Blog Post: Fixing `UND_ERR_SOCKET` in NodeJS](https://sg.wantedly.com/companies/rightcode/post_articles/871110)
- [StackExchange Post: `UND_ERR_SOCKET`](https://ethereum.stackexchange.com/questions/130028/hardhat-deploy-script-on-rsk-throws-und-err-socket)

## Recommended solutions

The fundamental solution is to stop creating a new connection for every request and instead **reuse a pool of connections**.

### Why limit connections?

Establishing a new TCP connection requires a TLS handshake, which is a time-consuming process. [More details here](https://www.cloudflare.com/en-gb/learning/ssl/what-happens-in-a-tls-handshake/). By reusing a smaller pool of persistent connections, your application will be more performant, and it will place significantly less load on both your client machine and our RPC servers.

### What is an ideal connection count?

We recommend starting with a limit of **50 connections**. You can monitor your port usage with the `lsof` command above. If you see that all 50 connections are consistently in use and your application could benefit, you can gradually increase this limit.

### 1. Limit connections with a global agent (recommended)

This is the best solution for most applications. You configure NodeJS to use a global agent with a connection pool, forcing the HTTP client to reuse connections.

**For `undici` (Node's default `fetch`):**

Install [`undici`](https://www.npmjs.com/package/undici) and set the global dispatcher at the very beginning of your application's entry point.

```javascript
// At the top of your main application file

setGlobalDispatcher(
  new Agent({
    connections: 50, // Recommended starting default
  })
);
```

**For `axios`:**

If you prefer [`axios`](https://www.npmjs.com/package/axios), you can create a client with a dedicated `https.Agent`. The [`@solana/web3.js`](https://www.npmjs.com/package/@solana/web3.js) `Connection` object allows you to pass a custom fetch implementation. A full example can be found at [this Gist](https://gist.github.com/WilfredAlmeida/9adea27abb5958178c4370c5656e89b7).

```javascript

const agent = new https.Agent({
  maxSockets: 50, // Recommended starting default
  keepAlive: true,
});

const axiosInstance = axios.create({
  httpsAgent: agent,
});
```

### 2. Use an alternative runtime (Bun)

The [Bun](https://bun.sh/) runtime is a modern alternative to NodeJS. Based on our testing, its internal HTTP client handles connection pooling more efficiently and does not exhibit this socket exhaustion issue. This is a great option for new projects but may be a larger change for existing codebases.

### 3. Using the new version of `@solana/web3.js`

Anza Labs is developing a new and improved [version of the library](https://github.com/solana-labs/solana-web3.js/tree/master/packages/library) which, as of this writing, is in technical preview. It uses the [`undici`](https://www.npmjs.com/package/undici) library and the errors are less frequent in it. If encountered, with the configuration mentioned in [section 1](#1-limit-connections-with-a-global-agent-recommended) they should be resolved. Do note that the library is not compatible with the current version, meaning that it'll be a ground up rewrite of your codebase.

### 4. A note on other libraries

If you're using SDKs like [jito-ts](https://www.npmjs.com/package/jito-ts) which uses [node-fetch](https://www.npmjs.com/package/node-fetch) underneath, or some other libraries, you may encounter errors like `ERR_STREAM_PREMATURE_CLOSE` which have this same underlying issue and limiting the number of connections for NodeJS has resolved the issue for our customers. The number of connections for libraries like `node-fetch` and others can be limited by providing an `http(s).Agent` configuration. For example:

```javascript
new https.Agent({
  maxSockets: 50,
});
```

---

<hr>

<i class="fa-life-ring">:life-ring:</i> Need help? Contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one)<br><i class="fa-gear">:gear:</i> Manage endpoints, billing, team: [Customer portal](https://customers.triton.one)<br><i class="fa-briefcase">:briefcase:</i> Sales questions? [Contact sales](https://triton.one/contact)<br><i class="fa-sparkles">:sparkles:</i> AI agent? [Read llms.txt](https://docs.triton.one/llms.txt)<br><i class="fa-rss">:rss:</i> Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · [YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · [GitHub](https://github.com/rpcpool)
