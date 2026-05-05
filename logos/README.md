# Customer logos

Logos referenced from `solana/welcome.mdx` (`.customer-logo-grid` block).

## Files needed

Drop SVG files at these exact paths (slugs match the `<img src>` in welcome.mdx):

- `solana.svg` ✓ (seeded from `logo/chains/solana.svg`)
- `jupiter.svg`
- `phantom.svg`
- `kamino.svg`
- `wintermute.svg`
- `orca.svg`
- `metaplex.svg`
- `solflare.svg`
- `squads.svg`
- `arcium.svg`

## Display behaviour

Logos render at 32px max-height, greyscale + 65% opacity by default, full colour + 100% on hover. Dark mode auto-inverts (configured in `custom.css`).

## Sizing

SVG preferred. Aim for clean monochrome marks; busy logos look weak at 32px. If you only have PNG, drop it as `<slug>.png` and update the `<img src>` in welcome.mdx accordingly.

## To add or remove a logo

Edit the `.customer-logo-grid` block in [`solana/welcome.mdx`](../solana/welcome.mdx). Grid is currently 5 cols × 2 rows on desktop, 2 cols on mobile.
