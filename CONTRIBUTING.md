# Contributing to Triton docs

Thanks for fixing or extending these docs. The repo is public; anyone can fork, edit, and open a PR. Triton-side reviewers will check it and merge.

## How to send a change

1. **Fork** this repo (top-right of GitHub).
2. **Create a branch** off `proposed-structure` (the working branch). Don't branch off `main` -- that's the production branch and only takes merges from `proposed-structure`.
3. **Make your change.** For small fixes (typo, broken link, copy tweak), the GitHub web editor is fine. For anything bigger, clone locally and use a code editor.
4. **Open a PR** against `proposed-structure`. The `Lint MDX` GitHub Action will run automatically -- if it fails, the error output points at the line.
5. **A Triton reviewer will respond.** Most copy fixes merge same day.

## Don't edit fragile pages in the Mintlify visual editor

The Mintlify web editor parses MDX → React tree → re-serializes. That round-trip breaks on:

- Pages with snippet imports (e.g. `<FooterLinks />`, `<DragonsMouthCard />`)
- Pages with mermaid blocks
- Pages with custom HTML divs (e.g. the pricing calculator, customer logo marquee)
- Pages > 500 lines

Symptoms: section headings duplicated, paragraphs duplicated inline within the same line, headings concatenated like `## Pings Pings`, 3+ consecutive blank lines.

**For those pages, edit in code (GitHub web editor or local).** The lint Action catches every signature listed above before merge.

The known-fragile pages today:

- `solana/welcome.mdx`
- `solana/get-started/plans-and-billing.mdx`
- `solana/streaming/dragons-mouth-g-rpc.mdx`
- `solana/streaming/overview.mdx`
- `solana/streaming/quickstart.mdx`

## Style essentials

- **Sentence case** for all headings, titles, UI labels. Not Title Case.
- **No em dashes.** Use `--`.
- **British spelling**: organisation, optimise, analyse, decentralised.
- **Active voice, second person.**
- **Lucide icons only.** Banned icons that don't render in Mintlify's bundle: `list-checks` (use `signal-high`), `key-round` (use `key`), `filter` (use `sliders-horizontal`).
- **Card body length uniform per CardGroup** (±5 chars).
- **Footer pattern**: every page imports `<FooterLinks />` from `/snippets/footer-links.mdx` and renders it once at the bottom after a `---` divider.

The full rules live in `AGENTS.md`.

## Reusable components (snippets)

Reusable blocks live in `/snippets/`. **Don't paste the same block on a second page** -- import the snippet.

- `/snippets/footer-links.mdx` -- the footer at the bottom of every page
- `/snippets/customer-logo-marquee.mdx` -- the customer-logo strip
- `/snippets/cards/<product>.mdx` -- one canonical Card per Triton product. Import + render.
- `/snippets/streaming-prerequisites.mdx` -- the "before you subscribe" block used on Dragon's Mouth and Deshred.
- `/snippets/faqs/<topic-slug>.mdx` -- one Accordion per file. Mirrored across the canonical FAQ page (`/solana-faqs/...`) and any docs page that needs the same Q+A.

To change copy on a card or FAQ that appears on multiple pages, edit the snippet file once -- every page updates on next deploy.

## Local development

```bash
git clone https://github.com/kshyndina/docs.git
cd docs
npm i -g mint
mint dev
```

Preview at `http://localhost:3000`.

## Support

For doc questions, open an issue or PR. For product / account / billing questions, contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one).
