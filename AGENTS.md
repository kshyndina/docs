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

### Snippets (footer, customer logos, FAQs)

Reusable blocks live in `/snippets`. Two rules:

1. **Import once, render once.** A page that imports `<FooterLinks />` should render it exactly once, at the bottom, after a `---` divider. Never paste the snippet's inner HTML inline -- always use the component.
2. **Before saving, search the file for duplicates.** Run `grep -c "<FooterLinks" path/to/file.mdx` -- the answer must be `1`. Same for `<CustomerLogoMarquee />` and any other snippet. Mintlify's visual editor sometimes appends a copy of the snippet rather than replacing it; agents that paste large blocks can also accidentally duplicate snippets. The visual difference between rendered output and the source markdown can hide this -- always check the source.

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
