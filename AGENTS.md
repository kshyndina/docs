# Triton One docs -- agent instructions

Instructions for Claude (and any other AI agent) working on this repository.

## About this project

- Documentation site for [Triton One](https://triton.one), Solana's largest independent RPC infrastructure provider
- Built on [Mintlify](https://mintlify.com) -- pages are MDX with YAML frontmatter, config lives in `docs.json`
- Live site: docs.triton.one (production = `main` branch)
- Preview deployments: Mintlify auto-deploys every branch to its own URL
- Local preview: `mint dev`
- Link check: `mint broken-links`
- Strict build check: `mint validate`

## Voice and tone (non-negotiable)

- **Sentence case** for all headings, titles, and UI labels. Not Title Case. Proper nouns stay capitalised.
- **No em dashes.** Use `--` (two hyphens) instead.
- **British spelling**: organisation, optimise, analyse, decentralised, behaviour, colour. Never "z" forms.
- **Active voice, second person.** "You configure X" not "X is configured by the user."
- **Short sentences.** If a sentence has a comma, consider splitting it.
- **No corporate language** or AI slop. Avoid: leverage, synergy, seamless, robust, cutting-edge, world-class, empower, unlock, supercharge.
- **No filler.** Avoid: "just wanted to," "I think maybe," "in order to" (use "to"), "at this time" (use "now").
- **No emoji** in docs unless Kate explicitly adds them.
- The word "ecosystem" is fine when it literally refers to the Solana ecosystem.

## Terminology

Triton's products. Use exact casing.

| Product | What it is |
|---------|------------|
| **Yellowstone gRPC** | Our gRPC streaming protocol (we created it) |
| **Steamboat** | Indexed program state |
| **Deshred** | Transaction reconstruction for traders |
| **Hydrant** | Historical data / Get Transactions From Account (GTFA) |
| **Jet** | SWQoS routing |
| **Cascade** | Legacy SWQoS service (retired Feb 2026) |
| **Photon** | Compressed account / state-compression product |
| **Fumarole** | Streaming product |
| **Whirligig** | WebSockets streaming |
| **Vixen** | Program streams |
| **Old Faithful** | Historical archive |
| **Shield** | Policy / abuse-prevention |
| **Metis** | Swap product |
| **Titan** | Swap product |
| **Richat** | Our internal name. Helius brands it as "LaserStream" -- do not call it that in our docs |

Other usage:
- "RPC" not "rpc" or "Rpc"
- "gRPC" not "GRPC" or "grpc"
- "Solana" always capitalised
- "Web3" not "web3"
- "endpoint" not "end point" or "end-point"
- "rate limits" (two words) not "ratelimits"

## Content rules

- **Don't badmouth competitors.** Helius, QuickNode, Alchemy, dRPC, Chainstack, ERPC -- factual references only, no shade.
- **Don't reference unreleased products or confidential roadmap items.** RPC 2.0 details are confidential. If unsure, ask Kate.
- **All code blocks need a language tag.** ` ```bash `, ` ```javascript `, ` ```python ` -- never bare ` ``` `.
- **All images need descriptive alt text.**
- **Internal links use root-relative paths without extensions**: `/streaming/fumarole`, not `../streaming/fumarole.mdx`.
- **Add new pages to `docs.json` navigation** or they won't appear in the sidebar.

## Mintlify-specific

- File naming: kebab-case (`vote-account-setup.mdx`)
- Frontmatter: `title` is required; add `description` and `keywords` for SEO
- Components: use the Mintlify skill (auto-loads via the plugin) for full props reference
- Common components: `<Note>`, `<Info>`, `<Tip>`, `<Warning>`, `<Check>`, `<Danger>`, `<Steps>`, `<Tabs>`, `<CodeGroup>`, `<Cards>`, `<Columns>`, `<AccordionGroup>`

### Snippets (footer, customer logos, FAQs, product cards)

Reusable blocks live in `/snippets`. Three rules:

1. **Import once, render once.** A page that imports `<FooterLinks />` should render it exactly once, at the bottom, after a `---` divider. Never paste the snippet's inner HTML inline -- always use the component.
2. **Before saving, search the file for duplicates.** Run `grep -c "<FooterLinks" path/to/file.mdx` -- the answer must be `1`. Same for `<CustomerLogoMarquee />` and any other snippet. Mintlify's visual editor sometimes appends a copy of the snippet rather than replacing it; agents that paste large blocks can also accidentally duplicate snippets. The visual difference between rendered output and the source markdown can hide this -- always check the source.
3. **Use product-card snippets, don't write Card markup inline.** Each Triton product has a canonical card under `/snippets/cards/<product>.mdx` (icon, title, description, href all locked). When listing related products on a page, import the snippet and use `<DragonsMouthCard />`, `<DeshredCard />`, etc. inside a `<CardGroup>`. This guarantees the icon/copy stays consistent across every page and makes a future copy or icon change a one-file edit.

#### Product icon registry

Each product has ONE icon. Never reuse it for a different product on the same page. Cross-page consistency is hard-required.

| Product | Lucide icon | Snippet |
|---|---|---|
| Standard RPC | `zap` | _todo_ |
| Steamboat | `database` | _todo_ |
| DAS API | `image` | _todo_ |
| Account Sync | `refresh-cw` | _todo_ |
| ZK Compression | `shrink` | _todo_ |
| Dragon's Mouth gRPC | `radio` | `/snippets/cards/dragons-mouth.mdx` |
| Deshred transactions | `flame` | `/snippets/cards/deshred.mdx` |
| Whirligig WebSockets | `rotate-cw` | `/snippets/cards/whirligig.mdx` |
| Fumarole | `layers` | `/snippets/cards/fumarole.mdx` |
| Old Faithful streams | `archive` | `/snippets/cards/old-faithful.mdx` |
| Hermes | `activity` | _todo_ |
| Pythnet | `globe` | _todo_ |
| Hydrant | `history` | _todo_ |
| Yellowstone Jet | `send` | _todo_ |
| Priority Fees API | `trending-up` | _todo_ |
| Metis | `git-branch` | _todo_ |
| Titan Prime | `route` | _todo_ |
| Jito Bundles | `package` | _todo_ |
| Dedicated gRPC | `server` | _todo_ |
| White-label validator | `shield` | _todo_ |
| Private trusted validator | `lock` | _todo_ |

Meta cards (cross-cutting):

| Card | Lucide icon | Snippet |
|---|---|---|
| Streaming overview | `compass` | `/snippets/cards/streaming-overview.mdx` |
| Streaming quickstart | `rocket` | `/snippets/cards/streaming-quickstart.mdx` |

Common feature-card icons (page-local, must be unique within their page):

| Concept | Lucide icon |
|---|---|
| Latency / sub-slot | `gauge` |
| Filtering | `sliders-horizontal` |
| Replay / resume | `rotate-ccw` |
| Compact / Protobuf efficiency | `feather` |
| Bi-directional / live update | `repeat` |
| Connect / drop-in | `plug` |
| Transaction extension | `receipt` |
| All commitment levels | `signal-high` |
| Earliest signal | `flame` |
| Same gRPC service | `link` |
| ALT / resolved keys | `key` |

**Icons that previously broke and are banned:** `list-checks`, `key-round`, `filter`. Use `signal-high`, `key`, and `sliders-horizontal` respectively. Mintlify's Lucide bundle silently drops these despite being valid Lucide names. Always test the icon in the live preview build, not just in the source.

Use cases:

| Use case | Lucide icon |
|---|---|
| Trading and MEV | `coins` |
| DEX or DeFi | `git-merge` |
| Wallet or consumer app | `wallet` |
| NFT or compressed-asset platform | `palette` |
| Indexer or analytics | `bar-chart-3` |
| Institutional | `building` |
| Gaming | `gamepad-2` |
| AI agent | `bot` |

## docs.json schema rules (incidents we do not repeat)

The single most fragile file in this repo. A bad change in `docs.json` can take the entire site down without throwing an error. Two specific footguns from production incidents on 2026-05-08:

### Rule 1: tabs only accept `pages`, `groups`, or `openapi`

Adding `href` to a tab to make it an external link **does not work**. Mintlify silently accepts the malformed tab and breaks tab navigation entirely (no tab becomes clickable, including the valid ones).

```jsonc
// ❌ BREAKS the entire tab bar
{ "tab": "Blog", "icon": "newspaper", "href": "https://blog.triton.one" }
```

External links go in `navbar.links`, not in tabs:

```jsonc
// ✅ Correct
"navbar": {
  "links": [
    { "label": "Blog ↗", "icon": "newspaper", "href": "https://blog.triton.one" }
  ]
}
```

### Rule 2: page entries can be a string OR an object with `{page, group, icon, expanded, root, pages, openapi}` — nothing else

Adding `tag: "WIP"` (or any other property) to a page object confuses Mintlify's tab href resolver: it can't determine the tab's first page URL, so it falls back to `href="/"`. Tabs containing tagged pages become unclickable (clicking just routes home).

```jsonc
// ❌ BREAKS the parent tab's href -> "/"
{ "page": "solana/welcome", "tag": "WIP" }
```

To mark a page as a placeholder, use a `<Note>Coming soon...</Note>` callout inside the page body. Don't use `tag` on page objects.

### Enforcement

`scripts/lint-docs-json.py` runs in CI on every PR (`.github/workflows/lint-mdx.yml`) and rejects both patterns. To run locally before pushing:

```bash
python3 scripts/lint-docs-json.py
```

If you ever feel tempted to add a property to a tab or page object that's not in the allowed list above, the linter will block you. Trust it.

## Debug runbook: "the docs site is broken"

Pre-incident response checklist. Work top-down — each step rules out a layer.

### Step 1: which URL is broken?

```bash
# These three are different things. Test each:
# 1. Custom domain (production)
curl -sI https://docs.triton.one/solana/welcome | head -5

# 2. Mintlify project URL (current state of main deploy)
curl -sI https://tritonone.mintlify.app/solana/welcome | head -5

# 3. Branch preview (current state of proposed-structure)
curl -sI https://tritonone-proposed-structure.mintlify.app/solana/welcome | head -5
```

If they show different content, **the custom domain is on a different platform** (we found docs.triton.one was on GitBook in May 2026). Look for `x-gitbook-route-site` vs `x-mintlify-client-version` in headers.

### Step 2: tabs not clickable / clicking goes to wrong place

Pull the rendered HTML and extract every tab's `href` directly:

```bash
curl -s https://tritonone-proposed-structure.mintlify.app/solana/welcome -o /tmp/p.html
python3 -c "
import re
with open('/tmp/p.html') as f: html = f.read()
for label in ['Documentation', 'Guides', 'API reference', 'FAQs']:
    idx = html.find(f'>{label}</a>') if html.find(f'>{label}</a>') != -1 else html.find(f'</svg>{label}</a>')
    if idx == -1: print(f'{label}: NOT FOUND'); continue
    a_start = html.rfind('<a ', 0, idx); a_end = html.find('</a>', idx) + 4
    href = re.search(r'href=\"([^\"]+)\"', html[a_start:a_end])
    print(f'{label:18} -> {href.group(1) if href else \"?\"}')
"
```

**Any tab with `href="/"` is broken.** Mintlify could not resolve the tab's first page URL. Cause is almost always one of:
- A page object inside that tab has unsupported properties (most commonly `tag`)
- The tab itself has unsupported properties (most commonly `href`)

Run `python3 scripts/lint-docs-json.py` to confirm. The linter pinpoints the exact offending tab/page.

### Step 3: page returns 404 or wrong content

```bash
# Verify the file exists at the path docs.json says
gh api 'repos/kshyndina/docs/contents/solana/welcome.mdx?ref=proposed-structure' --jq '.name'

# Verify Mintlify's webhook is connected (must return at least 1)
gh api repos/kshyndina/docs/hooks --jq 'length'
```

If webhook count is 0, archive/unarchive cycle removed it — go to Mintlify dashboard → Git settings → reconnect.

### Step 4: home redirects to wrong place

`/` should land on `/solana/welcome`. If it lands on `/solana-api/api-overview` or somewhere else, Mintlify's "first page in nav" resolution is finding the wrong thing, usually because of Rule 2 above (a tag-laden page object earlier in the nav broke its parent's href, so Mintlify skipped past it to find the next valid first-page).

```bash
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://tritonone-proposed-structure.mintlify.app/
```

### Step 5: rendered HTML looks correct but Kate's browser shows old version

Browser has a stale Next.js bundle cached. Two fixes:
1. **Hard refresh** (Cmd-Shift-R) — clears most cases
2. **Force a fresh deploy** with new asset hashes by pushing a trivial commit (e.g., touch `.mintlify-cache-bust`)

### Quick-reference table

| Symptom | First check | Likely cause |
|---|---|---|
| Site shows old/wrong content on docs.triton.one | `curl -sI` on docs.triton.one | Domain on a different platform (GitBook vs Mintlify) |
| `/` redirects to wrong tab | curl `/` and look at `redirect_url` | First page of first tab not resolving — usually a page-object property bug |
| All tabs unclickable | Check tab anchors in rendered HTML | Tab schema violation (`href` on a tab) |
| Some tabs go to `/` | Same as above | Page-object property bug (`tag` etc) |
| 404 on a known page | gh api content check | File missing, or wrong path in docs.json |
| Push goes through but no rebuild | `gh api repos/X/hooks --jq length` | Mintlify webhook removed (e.g., after archive) |

### Don't do these (lessons learned)

- ❌ **Don't archive `kshyndina/docs` while Mintlify is connected to it.** GitHub disables webhooks on archive and doesn't restore them on unarchive. Mintlify stops getting push notifications. Disconnect Mintlify first, then archive.
- ❌ **Don't add a `redirects` block to docs.json to "fix" tab href issues.** It papers over the real bug (page-object schema violation) and adds confusion for the next debugger.
- ❌ **Don't add new properties to docs.json tabs or page objects without checking the lint passes.** The linter has the canonical list.

## Workflow

- Production branch: `main` -- merges deploy to docs.triton.one
- Working branch: `claude/edits` -- gets its own Mintlify preview URL, edited freely
- Kate can also edit the same branches in Mintlify's web editor; merge or cherry-pick when ready
- Don't push directly to `main` without confirmation
- Commits should describe the user-visible change, not the mechanic ("fix Fumarole port number" not "update mdx file")

## When in doubt

Ask Kate. She's at kate.shyndina@triton.one and reports to Kendra Ross (marketing lead). Other people who may need to review specific topics:

- **Kendra** -- marketing strategy, messaging
- **Petya** -- technical writing, depth
- **Wilfred** -- SDK / dev content
- **Tyler** -- email/frontend
- **Steve** -- BD / partnerships
- **Pia** -- design, visual content
