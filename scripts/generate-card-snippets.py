#!/usr/bin/env python3
"""
Generate the canonical 76 card snippets per Kate's allowed list.

Run from repo root:
    python3 scripts/generate-card-snippets.py
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SNIPPETS = BASE / "snippets" / "cards"


# Each entry: (relative_path, title, icon, href, copy)
# href="" means no link (descriptive card)
CARDS = [
    # ── Products (20) ───────────────────────────────────────────────
    ("standard-rpc.mdx", "Standard RPC", "zap",
     "/solana/reading-state/standard-rpc",
     "Solana JSON-RPC over HTTPS. Every standard method, served from the regional fleet."),

    ("das-api.mdx", "DAS API", "image",
     "/solana/reading-state/metaplex-das-api",
     "Fastest read for NFT and cNFT ownership, proofs, and metadata."),

    ("account-sync.mdx", "Account Sync", "refresh-cw",
     "/solana/reading-state/account-sync",
     "Streaming-backed local cache for account reads. No polling, no code changes."),

    ("steamboat.mdx", "Steamboat", "database",
     "/solana/reading-state/steamboat-indexed-accounts",
     "Custom indexes for `getProgramAccounts` and token-account hot paths. Up to 50x faster, no premium."),

    ("zk-compression.mdx", "ZK Compression", "binary",
     "/solana/reading-state/zk-compression-photon",
     "Photon-backed reads for compressed accounts, cNFTs, and compressed tokens via Light Protocol indexes."),

    ("dragons-mouth.mdx", "Dragon's Mouth gRPC", "radio",
     "/solana/streaming/dragons-mouth-g-rpc",
     "Sub-slot real-time updates for accounts, transactions, slots, and blocks via gRPC."),

    ("whirligig.mdx", "Whirligig WebSockets", "rotate-cw",
     "/solana/streaming/whirligig-websockets",
     "Drop-in for native Solana WebSockets. Fastest real-time data for frontends, backed by gRPC."),

    ("fumarole.mdx", "Fumarole reliable streams", "layers",
     "/solana/streaming/fumarole-persistent-streams",
     "Redundant streaming layer with 96h of stored data and built-in cursor resume."),

    ("deshred.mdx", "Deshred transactions", "flame",
     "/solana/streaming/deshred-transactions",
     "Pre-execution transactions reconstructed from raw shreds. Earliest intent signal for traders."),

    ("hermes.mdx", "Hermes", "activity",
     "/pyth/pyth-hermes",
     "Pyth Hermes API. Real-time price feeds across hundreds of markets over REST and WebSocket."),

    ("old-faithful.mdx", "Old Faithful streams", "archive",
     "/solana/streaming/old-faithful-streams",
     "Replay every block from genesis through the same gRPC interface as live streams."),

    ("hydrant.mdx", "Hydrant", "history",
     "/solana/history/hydrant",
     "History with developer-shaped indexes. Millisecond reads from genesis across the full ledger."),

    ("jet-sender.mdx", "Yellowstone Jet", "send",
     "/solana/sending-transactions/jet-sender",
     "Direct-to-leader forwarding over QUIC with leader scheduling, connection pooling, and retries built in."),

    ("priority-fees-api.mdx", "Priority Fees API", "trending-up",
     "/solana/sending-transactions/priority-fees-api",
     "Smart fee estimation with tail-aware percentiles. Reliable landing without overpaying."),

    ("metis-swap-api.mdx", "Metis swap API", "git-branch",
     "/solana/sending-transactions/metis-swap-api",
     "Swap routing across 20+ DEXes with exact-out and platform-fee support built in."),

    ("titan-swap-api.mdx", "Titan swap API", "route",
     "/solana/sending-transactions/titan-swap-api",
     "Streaming quotes and routes via DART live re-optimisation or the Prime API for high-volume desks."),

    ("jito-bundles.mdx", "Jito bundles", "package",
     "/solana/sending-transactions/jito-bundles",
     "Jito bundle simulation through Triton endpoints. Test bundle ordering before submitting."),

    ("shield-mev-protection.mdx", "Shield MEV protection", "shield-check",
     "/solana/sending-transactions/shield-mev-protection",
     "On-chain allowlists or blocklists with local enforcement. No added latency on the send path."),

    ("dedicated-grpc-node.mdx", "Dedicated gRPC node", "server",
     "/solana/dedicated-nodes/overview",
     "Private node with isolated CPU and unlimited concurrent gRPC connections. For latency-sensitive or heavy streaming workloads."),

    ("white-label-validator.mdx", "White-label validator", "landmark",
     "/solana/validators/introduction",
     "Branded validator with full key separation, zero ops overhead, and high availability."),

    # ── Onboarding (5) ──────────────────────────────────────────────
    ("how-to-sign-up.mdx", "How to sign up", "user-plus",
     "/solana-guides/account/how-to-sign-up",
     "Step-by-step from clicking signup to a live Triton endpoint."),

    ("access-endpoint-and-token.mdx", "Access your endpoint and token", "key",
     "/solana-guides/account/access-endpoint-and-token",
     "Find the endpoint URL and secret token in the customer dashboard."),

    ("quickstart.mdx", "Quickstart", "rocket",
     "/solana/get-started/quickstart",
     "Sign up, deposit, get an endpoint, send your first request."),

    ("streaming-quickstart.mdx", "Streaming quickstart", "play",
     "/solana/streaming/quickstart",
     "Test every Triton streaming service in under five minutes."),

    ("streaming-overview.mdx", "Streaming overview", "compass",
     "/solana/streaming/overview",
     "Compare every Triton streaming service side by side."),

    # ── Account and billing (5) ─────────────────────────────────────
    ("account-management.mdx", "Account management", "user-cog",
     "/solana/get-started/account-management/platform-overview",
     "Customer dashboard tour: endpoints, billing, team, and support."),

    ("account-management-api.mdx", "Account management API", "code",
     "/solana/get-started/account-management/account-management-api/overview",
     "Programmatically manage endpoints, tokens, and members."),

    ("plans-and-billing.mdx", "Plans and billing", "credit-card",
     "/solana/get-started/plans-and-billing",
     "Pay-as-you-go vs invoiced, top-ups, and the cost calculator across shared and dedicated setups."),

    ("rate-and-connection-limits.mdx", "Rate and connection limits", "gauge",
     "/solana/get-started/rate-and-connection-limits",
     "Per-endpoint and method rate limits, plus streaming connection caps."),

    ("auth-and-security.mdx", "Auth and security", "shield",
     "/solana/get-started/auth-and-security",
     "Endpoint, token, and spend security. What Triton handles and what you configure."),

    # ── Account management API resources (8) ────────────────────────
    ("ama/auth-and-headers.mdx", "Auth and headers", "id-card",
     "/solana/get-started/account-management/account-management-api/auth-and-headers",
     "Bearer tokens, organisation context, and the headers every call needs."),

    ("ama/accounts.mdx", "Accounts", "user",
     "/solana/get-started/account-management/account-management-api/accounts",
     "List, create, rotate, and revoke organisation members."),

    ("ama/endpoints.mdx", "Endpoints", "link",
     "/solana/get-started/account-management/account-management-api/endpoints",
     "Provision, list, configure, and delete endpoints."),

    ("ama/tokens.mdx", "Tokens", "lock",
     "/solana/get-started/account-management/account-management-api/tokens",
     "Issue, list, rotate, and revoke endpoint tokens."),

    ("ama/subscriptions.mdx", "Subscriptions", "rss",
     "/solana/get-started/account-management/account-management-api/subscriptions",
     "Attach plans, add-ons, or watch lists to the organisation."),

    ("ama/subscription-types.mdx", "Subscription types", "list",
     "/solana/get-started/account-management/account-management-api/subscription-types",
     "The catalogue of plans and add-ons available to attach."),

    ("ama/address-watch-lists.mdx", "Address watch lists", "bookmark",
     "/solana/get-started/account-management/account-management-api/address-watch-lists",
     "Manage reusable account lists referenced from gRPC and WebSocket subscriptions."),

    ("ama/rate-tiers.mdx", "Rate tiers", "sliders-vertical",
     "/solana/get-started/account-management/account-management-api/rate-tiers",
     "Read and configure per-endpoint rate limits programmatically."),

    # ── Dashboard tabs (6) ──────────────────────────────────────────
    ("dashboard/endpoints.mdx", "Endpoints", "monitor", "",
     "Provision, monitor, and configure every endpoint in one place."),

    ("dashboard/auth.mdx", "Auth", "fingerprint", "",
     "Manage tokens, origin allowlists, and IP allowlists per endpoint."),

    ("dashboard/usage.mdx", "Usage", "bar-chart", "",
     "Live request count, RPS, error rate, and cost-to-date with method drilldowns."),

    ("dashboard/billing.mdx", "Billing", "wallet", "",
     "Deposits, top-ups, payment methods, invoices, and credit balance."),

    ("dashboard/members.mdx", "Members", "users", "",
     "Invite teammates, set roles, rotate credentials."),

    ("dashboard/audit-log.mdx", "Audit log", "scroll", "",
     "Every config change with timestamp, actor, and before/after values."),

    # ── Use case stacks (7) ─────────────────────────────────────────
    ("use-cases/trading.mdx", "Trading or market making", "coins",
     "/solana-guides/getting-started/set-up-rpc/trading-or-market-making",
     "Live prices, sub-slot tx landing, anti-MEV. Stack: Dragon's Mouth, Jet, Priority Fees, Shield."),

    ("use-cases/defi.mdx", "DeFi protocols (Lending, DEXs)", "git-merge",
     "/solana-guides/getting-started/set-up-rpc/dex-or-defi-protocol",
     "Pool state, swap activity, tx landing, historical fills. Stack: Dragon's Mouth, Jet, Hydrant, Titan."),

    ("use-cases/wallet.mdx", "Wallet or consumer app", "smartphone",
     "/solana-guides/getting-started/set-up-rpc/wallet-or-consumer-app",
     "Balances, history, NFT portfolio, live updates. Stack: Standard RPC, DAS API, Whirligig."),

    ("use-cases/nft-marketplace.mdx", "NFT marketplace", "palette",
     "/solana-guides/getting-started/set-up-rpc/nft-or-compressed-asset-platform",
     "Mints, metadata, collection feeds, sale events. Stack: DAS API, ZK Compression, Whirligig."),

    ("use-cases/indexer.mdx", "Indexer or analytics", "bar-chart-3",
     "/solana-guides/getting-started/set-up-rpc/indexer-or-analytics",
     "Custom indexes, historical backfill, parsed transactions. Stack: Steamboat, Hydrant, Old Faithful, Fumarole."),

    ("use-cases/gaming.mdx", "Gaming", "gamepad-2",
     "/solana-guides/getting-started/set-up-rpc/gaming",
     "On-chain item state, real-time updates, fast reads. Stack: Standard RPC, DAS API, Dragon's Mouth, Whirligig."),

    ("use-cases/ai-agent.mdx", "AI agent or LLM app", "bot",
     "/solana-guides/getting-started/set-up-rpc/ai-agent-or-llm-app",
     "MCP access, llms.txt context, autonomous setup. Stack: MCP, llms.txt, Standard RPC, DAS API."),

    # ── Welcome-page walkthroughs (7) ───────────────────────────────
    ("walkthroughs/stream-grpc.mdx", "Stream Solana with gRPC", "antenna",
     "/solana-guides/end-to-end-builds/stream-solana-grpc",
     "Subscribe to accounts, transactions, and blocks via Dragon's Mouth, end to end."),

    ("walkthroughs/token-metadata.mdx", "Get token metadata", "image",
     "/solana-guides/end-to-end-builds/get-token-metadata",
     "Query NFT and cNFT metadata fast with a single DAS API call."),

    ("walkthroughs/copy-trade.mdx", "Copy trade a wallet", "copy",
     "/solana-guides/end-to-end-builds/copy-trade-wallet",
     "Watch any wallet in real time and mirror its trades."),

    ("walkthroughs/calculate-fees.mdx", "Calculate Solana fees end to end", "calculator",
     "/solana-guides/end-to-end-builds/calculate-solana-fees",
     "Base fees, priority fees, and account rent explained."),

    ("walkthroughs/stream-raydium.mdx", "Stream a Raydium AMM pool", "droplet",
     "/solana-guides/end-to-end-builds/stream-raydium-amm-pool",
     "Subscribe to pool state and trade events sub-slot."),

    ("walkthroughs/mint-token.mdx", "Mint a Solana token", "sparkles",
     "/solana-guides/end-to-end-builds/mint-solana-token",
     "Create an SPL, Token-2022, or P-Token mint. Set metadata, airdrop to test wallets."),

    ("walkthroughs/titan-prime.mdx", "Integrate Titan Prime", "route",
     "/solana-guides/end-to-end-builds/integrate-titan-prime",
     "Streaming swap quotes and routes that re-optimise live as the market moves."),

    # ── Dragon's Mouth feature highlights (4) ───────────────────────
    ("features/dm-sub-slot-latency.mdx", "Sub-slot latency", "timer", "",
     "Intra-slot updates arrive ~400 ms ahead of standard RPC, which only emits at slot boundaries."),

    ("features/dm-server-filtering.mdx", "Server-side filtering", "sliders-horizontal", "",
     "Filter by pubkey, program owner, signature, memcmp, datasize, or token-account state, all server-side."),

    ("features/dm-bidirectional-streams.mdx", "Bi-directional streams", "repeat-2", "",
     "Modify subscriptions on the fly without reconnecting. Send a new request, server swaps your filter set."),

    ("features/dm-compact-protobuf.mdx", "Compact Protobuf payloads", "feather", "",
     "Binary serialisation cuts bandwidth and CPU. Cheaper to stream, faster to parse."),

    # ── Whirligig feature highlights (4) ────────────────────────────
    ("features/wg-websocket-compatible.mdx", "Solana WebSocket compatible", "plug", "",
     "Drop-in replacement for the standard Solana WebSocket API. All native methods plus Triton-only extensions."),

    ("features/wg-transaction-subscribe.mdx", "transactionSubscribe extension", "bell", "",
     "Triton-only subscription for filtered transaction notifications over WebSocket."),

    ("features/wg-commitment-levels.mdx", "All commitment levels", "signal-high", "",
     "Subscribe at processed, confirmed, or finalized. Pick the trade-off that fits the workload."),

    ("features/wg-reliability-limits.mdx", "Reliability and limits at scale", "network", "",
     "Higher reliability and connection limits at scale, backed by Yellowstone gRPC."),

    # ── Deshred feature highlights (3) ──────────────────────────────
    ("features/ds-earliest-signal.mdx", "Earliest signal", "eye", "",
     "Pre-execution stream from raw shreds. ~20ms ahead at p75 vs confirmed transactions."),

    ("features/ds-same-grpc.mdx", "Same gRPC service", "git-fork", "",
     "Drops into your existing Dragon's Mouth pipeline. Separate method, same client."),

    ("features/ds-resolved-alt.mdx", "Resolved ALT addresses", "tags", "",
     "Includes writable and readonly addresses resolved from Address Lookup Tables."),

    # ── Blog and reference (3) ──────────────────────────────────────
    ("blog/shield.mdx", "Yellowstone Shield blog post", "book-open",
     "https://blog.triton.one/introducing-yellowstone-shield",
     "The full architecture and design rationale behind Shield's allow/blocklist model."),

    ("blog/deshred.mdx", "Deshred blog post", "book-marked",
     "https://blog.triton.one/deshred-transactions-the-fastest-path-to-solana-data/",
     "Architecture, tradeoffs, and how Deshred fits the Solana shred pipeline."),

    ("blog/thorofare.mdx", "Thorofare blog post", "book",
     "https://blog.triton.one/how-to-benchmark-solana-rpc-endpoints/",
     "Why most gRPC benchmarks are wrong, and how to do them right."),

    # ── Troubleshooting (4) ─────────────────────────────────────────
    ("troubleshooting/common-solana-errors.mdx", "Common Solana errors", "circle-help",
     "/solana-guides/error-handling/common-solana-errors",
     "Solana JSON-RPC error codes and how to handle each one."),

    ("troubleshooting/triton-rpc-error-codes.mdx", "Triton RPC error codes", "alert-triangle",
     "/solana-guides/error-handling/triton-rpc-error-codes",
     "Triton-specific error codes you might see and what they mean."),

    ("troubleshooting/how-to-troubleshoot.mdx", "How to troubleshoot", "wrench",
     "/solana-guides/error-handling/how-to-troubleshoot",
     "The full debug flow when something's not working as expected."),

    ("troubleshooting/metered-billing.mdx", "Metered billing walkthrough", "pie-chart",
     "/solana/get-started/plans-and-billing",
     "Track your usage and billing across calls and bandwidth in the customer dashboard."),
]


def render(title: str, icon: str, href: str, copy: str) -> str:
    if href:
        opener = f'<Card title="{title}" icon="{icon}" href="{href}">'
    else:
        opener = f'<Card title="{title}" icon="{icon}">'
    return f"{opener}\n  {copy}\n</Card>\n"


def main() -> None:
    written = 0
    for rel, title, icon, href, copy in CARDS:
        path = SNIPPETS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(title, icon, href, copy))
        written += 1
    print(f"Wrote {written} snippet files under {SNIPPETS}")


if __name__ == "__main__":
    main()
