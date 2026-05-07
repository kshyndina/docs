#!/usr/bin/env python3
"""
Replace inline Account Management API cards with snippet imports across
the eight AMA pages.

Idempotent: runs safely against pages that have already been migrated.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# (snippet path under /snippets/cards/, page-side import name, page-side title)
AMA_CARDS = {
    "auth-and-headers": ("ama/auth-and-headers.mdx", "AmaAuthAndHeadersCard"),
    "accounts":         ("ama/accounts.mdx",         "AmaAccountsCard"),
    "endpoints":        ("ama/endpoints.mdx",        "AmaEndpointsCard"),
    "tokens":           ("ama/tokens.mdx",           "AmaTokensCard"),
    "subscriptions":    ("ama/subscriptions.mdx",    "AmaSubscriptionsCard"),
    "subscription-types": ("ama/subscription-types.mdx", "AmaSubscriptionTypesCard"),
    "address-watch-lists": ("ama/address-watch-lists.mdx", "AmaAddressWatchListsCard"),
    "rate-tiers":       ("ama/rate-tiers.mdx",       "AmaRateTiersCard"),
}

# Match an inline AMA Card and capture the slug
INLINE = re.compile(
    r'<Card\s+[^>]*?href="/solana/get-started/account-management/account-management-api/(?P<slug>[a-z\-]+)"[^>]*>\s*[^<]+\s*</Card>',
    re.DOTALL,
)

PAGES = [
    "solana/get-started/account-management/account-management-api/accounts.mdx",
    "solana/get-started/account-management/account-management-api/auth-and-headers.mdx",
    "solana/get-started/account-management/account-management-api/address-watch-lists.mdx",
    "solana/get-started/account-management/account-management-api/endpoints.mdx",
    "solana/get-started/account-management/account-management-api/overview.mdx",
    "solana/get-started/account-management/account-management-api/subscription-types.mdx",
    "solana/get-started/account-management/account-management-api/subscriptions.mdx",
    "solana/get-started/account-management/account-management-api/tokens.mdx",
    "solana/get-started/account-management/account-management-api/rate-tiers.mdx",
]


def add_imports(text: str, needed: set[str]) -> str:
    """Insert any missing AMA snippet imports just after the last existing import."""
    have = set()
    for m in re.finditer(r"^import\s+(\w+)\s+from\s+'([^']+)'", text, re.MULTILINE):
        have.add(m.group(1))

    new_imports = []
    for slug in sorted(needed):
        snippet, var = AMA_CARDS[slug]
        if var in have:
            continue
        new_imports.append(f"import {var} from '/snippets/cards/{snippet}'")

    if not new_imports:
        return text

    # Insert after the last existing import line.
    matches = list(re.finditer(r"^import\s+\w+\s+from\s+'[^']+'\s*$", text, re.MULTILINE))
    if matches:
        last = matches[-1]
        insertion = "\n" + "\n".join(new_imports)
        return text[: last.end()] + insertion + text[last.end():]
    # No existing imports — drop after frontmatter
    fm_end = text.find("\n---\n", 4)
    if fm_end == -1:
        return "\n".join(new_imports) + "\n" + text
    insertion = "\n\n" + "\n".join(new_imports) + "\n"
    return text[: fm_end + 5] + insertion + text[fm_end + 5:]


def replace_inline(text: str) -> tuple[str, set[str]]:
    """Swap each inline AMA Card for a snippet import. Returns (text, slugs_used)."""
    used = set()

    def sub(m: re.Match) -> str:
        slug = m.group("slug")
        if slug not in AMA_CARDS:
            return m.group(0)
        used.add(slug)
        var = AMA_CARDS[slug][1]
        return f"<{var} />"

    new = INLINE.sub(sub, text)
    return new, used


def main() -> None:
    edited = 0
    for rel in PAGES:
        path = BASE / rel
        if not path.exists():
            continue
        text = path.read_text()
        new, used = replace_inline(text)
        if used:
            new = add_imports(new, used)
        if new != text:
            path.write_text(new)
            edited += 1
            print(f"  {rel}: replaced cards for {sorted(used)}")
    print(f"Edited {edited} files")


if __name__ == "__main__":
    main()
