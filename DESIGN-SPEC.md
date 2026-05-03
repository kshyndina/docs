# Triton One docs — design spec

The visual contract for [docs.triton.one](https://docs.triton.one) (Mintlify v3, theme `luma`). Read this before changing `docs.json`, `custom.css`, `custom.js`, or component-level styling. Numbered sections in `custom.css` map to the section labels here; keep them in sync.

Current checkpoint: branch [`final-design`](https://github.com/kshyndina/docs/tree/final-design) — frozen reference. Working branch is `proposed-structure`.

## Brand tokens

| Token | Value | Source |
|---|---|---|
| Primary | `#7A4BA0` | `docs.json` |
| Light primary | `#B591D3` | `docs.json` |
| Dark primary | `#492D60` | `docs.json` |
| Light bg | `#F7F7F7` | `docs.json` background.color.light |
| Dark bg | `#171717` | `docs.json` background.color.dark |
| Light gray fill | `#F7F7F7` | search input, code surfaces |
| Brand purple wash 6% | `rgba(122, 75, 160, 0.06)` | hover states |
| Brand purple wash 10% | `rgba(122, 75, 160, 0.10)` | active states, table headers |
| Brand purple border | `rgba(122, 75, 160, 0.18)` | secondary buttons, dropdowns, search outline |
| Dark mode purple wash | `rgba(181, 145, 211, 0.08–0.14)` | parallel range for dark theme |

Background uses Mintlify's `gradient` decoration over the flat color. The gradient is a `position: fixed` overlay (pinned to viewport so short pages don't scroll into the gradient void — see custom.css §18).

## Typography

| Surface | Family | Weight | Size | Tracking |
|---|---|---|---|---|
| Body | Work Sans | 400 | 15–16px | normal |
| Headings | DM Sans | 500–600 | per Mintlify default | normal |
| Eyebrow / breadcrumb | Geist Mono, SF Mono, ui-monospace | 500 | 0.75rem (12px) | 0.08em, uppercase |
| Code | inherits Mintlify's mono stack | — | — | — |
| Sidebar group labels | DM Sans | 500 | 0.9375rem (15px) | sentence case |

Sentence case everywhere: "Get started", not "Get Started". Active sidebar items go to weight 500 (not 600 — Mintlify's text-shadow already adds optical bolding).

## Logo

- Source: `/logo/mark.svg` (light + dark mode share the same mark)
- `href`: `https://triton.one`
- Rendered size: **3rem (48px)** height — 2× Mintlify's default `h-6` / 24px
- Container: the logo wrapper has Tailwind `flex-1` baked in by Mintlify; we override with `flex-grow: 0` so the tab nav sits flush against it instead of being pushed ~400px to the right (see custom.css §9)

## Sidebar

| Setting | Value |
|---|---|
| Width | `18rem` (`--sidebar-w` CSS variable) — overrides Mintlify's default `w-56` (14rem / 224px) |
| Top padding | extra padding so the first group label clears the taller navbar |
| Group label case | sentence case |
| Top-level groups | non-collapsible header (Mintlify default) |
| Nested groups | collapsible with chevron, click label → root page |
| Active page (in nested group) | brand-purple stripe + weight 500 |
| Top-level active page | weight 500, no stripe |
| Group hover | `rgba(122, 75, 160, 0.06)` |
| Active group (contains current page) | `rgba(122, 75, 160, 0.08)` |
| Vertical guide line under nested groups | `1px solid rgba(122, 75, 160, 0.16)` |

**The 14rem trap**: Mintlify's content-column auto-centring formula `lg:ml-[max(0px,calc(50vw-348px-14rem))]` hard-codes `14rem`. When you widen the sidebar to 18rem, the formula adds a phantom ~64px left margin. Always pair sidebar resize with `[class*="lg:ml-[max"] { margin-left: 0 !important }`.

## Navbar

### Desktop (lg, ≥1024px)

```
[ Logo ]  [ Solana ▼ ] [ Documentation | API ref | Guides | FAQs ]   [ … ]   [ search circle ] [ AI circle ] [ Log in ] [ Sign up ] [ Get an endpoint ]
```

- Search and AI render as 36×36 icon circles (Mintlify default ships them as wider buttons; see custom.css §6 for the override). `kbd` shortcut chips inside are hidden.
- Tab pills sit immediately right of the logo.
- Right cluster (`.topbar-right-container`) gets the leftover flex space.

### Tablet (md, 768–1023px)

- Same as desktop except: hamburger remains hidden (sidebar still visible at lg+ via Mintlify default — confirm).
- 3-dots overflow ("More actions") is hidden at md+.

### Mobile (xs, <768px)

```
[ Logo ]   [ search circle ] [ AI circle ] [ Sign-up icon circle ] [ Log-in icon circle ]            [ ☰ icon, fixed top-right, no background ]
```

- Hamburger: positioned **fixed top-right** (no circle background, plain icon, 2.75rem tap target).
- Original Mintlify hamburger row collapses because the button leaves flow layout via `position: fixed`.
- `Get an endpoint` primary CTA is hidden (too wide for mobile navbar).
- `Log in` and `Sign up` styled as 36×36 person-icon circles using SVG `mask` — Log-in is a person silhouette, Sign-up is a person-plus.

### Mobile drawer (opened by hamburger)

```
─────────────────────────
  Solana ▼          (chain selector)
  ─────────────────
  ┌───────────────────┐
  │ Documentation  ✓  │   ← active tab, purple wash
  └───────────────────┘
  ┌───────────────────┐
  │ API reference     │
  └───────────────────┘
  ┌───────────────────┐
  │ Guides            │
  └───────────────────┘
  ┌───────────────────┐
  │ FAQs              │
  └───────────────────┘
  ─────────────────
  [ groups for the active tab ]
─────────────────────────
```

`custom.js` replaces the original "Documentation / API reference / Guides / FAQs" Radix Select with 4 `.triton-mobile-tab-btn` siblings. Each is a full-width pill (rounded 0.5rem, 1px brand-purple border, light-purple wash on hover, darker wash + bold weight on the active tab).

Click → navigate to first page of that tab + set `triton-drawer-was-open` sessionStorage flag → drawer auto-reopens on next page load.

Tab → first-page mapping (Solana only — other chains have no tabs):

| Tab | Destination |
|---|---|
| Documentation | `/solana/welcome` |
| API reference | `/solana-api/api-overview` |
| Guides | `/solana-guides/error-handling` |
| FAQs | `/solana-faqs/general` |

Update [`custom.js`](custom.js) `TAB_DESTINATIONS` if these change.

## Page header

```
Eyebrow (Geist Mono, uppercase, 0.75rem)
H1 page title           [ Copy page ▼ ]   ← inline at sm+ AND xs
─────────────────────────────────────────
[ Note / Info / Warning callout ]
[ body content ]
```

- Eyebrow shows only the first breadcrumb segment (`.breadcrumb-list .breadcrumb-item:not(:first-child)` hidden) — matches the GitBook docs.triton.one convention.
- On mobile, the duplicate `#page-context-menu` below the title is hidden; the in-row variant is forced visible (Mintlify ships it as `hidden sm:flex` — see GOTCHAS in mintlify skill).
- Mobile copy-page: icon + chevron only, no "Copy page" text.

## Tables

- Border-collapse: separate, border-spacing 0
- Outer radius: 12px
- Header: `rgba(122, 75, 160, 0.10)` wash, DM Sans uppercase 14px, 0.02em tracking, weight 600
- Body: Work Sans 15px
- Border: `rgba(23, 23, 23, 0.10)` 1px

## Buttons

| Button | Style |
|---|---|
| Primary CTA (`navbar.primary`, "Get an endpoint") | Mintlify default solid purple |
| Secondary (Copy page first-half, sidebar pill triggers) | Transparent, 1px brand-purple-18% border, brand-dark text 85%, 0.5rem radius, 36px height |
| Tab pill (mobile drawer) | Same as secondary, with active-state purple wash + bold |
| Quickstart "Next step" / Steps final CTA | 0.5rem radius (Mintlify ships rounded-xl by default — overridden) |

All split buttons (e.g. Copy page) lock both halves to 36px height — Mintlify's defaults render them at 33px and 34px, which makes the seam visible.

## Floating "Ask a question" chat input

- **Desktop**: respects sidebar (`left: var(--sidebar-w, 18rem)`) and AI panel width.
- **Mobile (<1024px)**: position fixed full-width, soft gradient mask underneath (`F7F7F7` → transparent in light, `171717` → transparent in dark).
- The 200px white pseudo-wash Mintlify ships via `before:content-[""]` is killed unconditionally — looks like a hard white bar against any non-white background.
- "Powered by Mintlify" disclaimer hidden everywhere.

## Footer

Hidden entirely. Mintlify renders an empty `<footer>` even when no footer is configured; its wrapper has its own padding, leaving a tall white slab. Both the `<footer>` and any empty wrapper div are `display: none`.

## Code blocks

- Themes: `github-light` / `github-dark` (set in `docs.json`)
- Per-block wrap available via Mintlify's ` ```rust wrap ` syntax
- Content uses Mintlify's native horizontal scroll — no global wrap override (the `overflow-x: visible` workaround is a trap; see mintlify skill GOTCHAS)

## Theme toggle behaviour

The theme toggle is Mintlify's built-in. Don't reimplement. Both light and dark variants are styled to brand spec across all sections — when adding new components, always include a `html.dark body …` override block.

## File-by-file map

| File | Purpose | When to edit |
|---|---|---|
| [`docs.json`](docs.json) | Site config, navigation, theme tokens | Adding pages/groups, changing colors, navbar links, contextual menu options |
| [`custom.css`](custom.css) | All styling overrides (1300+ lines, 27 numbered sections) | Visual tweaks — find the section by topic, edit in place. Don't append duplicate rules. |
| [`custom.js`](custom.js) | Mobile drawer 4-button row + persist-drawer-after-nav | Drawer behaviour, anything that needs DOM transform CSS can't express |
| [`favicon.png`](favicon.png) | Browser tab icon | Brand changes |
| [`logo/`](logo/) | Logo + chain icons | New chain dropdowns, brand updates |
| [`images/`](images/) | Page assets | Per-page imagery |

## Adding a new chain dropdown

1. Add to `docs.json` `navigation.dropdowns[]` with `dropdown`, `icon` (path under `/logo/chains/`), and `groups` (or `tabs` if multi-section like Solana).
2. Create the content directory at the repo root (e.g. `monad/`) with the MDX files referenced in `pages`.
3. Drop the chain icon at `/logo/chains/<chain>.svg`.
4. If the chain has tabs (Documentation / API ref / Guides / FAQs), update `custom.js` `TAB_DESTINATIONS` with the new chain's first-page URLs OR keep the dropdown fallback.

## Adding a new tab to an existing chain

1. Add a `tab` entry in `docs.json` under the chain's `tabs` array.
2. Create the content directory and pages.
3. Update `TAB_LABELS` and `TAB_DESTINATIONS` in `custom.js` so the mobile drawer 4-button row picks it up. Without this, the new tab will fall back to the original Radix Select dropdown on mobile.

## What to NOT change without alignment

- Brand colors and primary/light/dark triplet — set across hundreds of CSS rules
- Sidebar width (18rem) — paired with the `lg:ml-[max…]` 14rem-trap override
- Logo height (3rem) — paired with the `flex-grow: 0` on the logo wrapper
- The `min-h: 0` cascade on layout wrappers (custom.css §18) — fixes the short-page scroll-into-void bug
- Background gradient `position: fixed` (custom.css §18) — paired with the above

These exist as a tightly-coupled set; changing one breaks the others.

## References

- Mintlify reference docs: [mintlify.com/docs](https://mintlify.com/docs)
- Mintlify skill (gotchas, components, configuration): `~/.claude/skills/mintlify/`
- Live preview: [tritonone-proposed-structure.mintlify.app](https://tritonone-proposed-structure.mintlify.app)
- Production: [docs.triton.one](https://docs.triton.one)
