#!/bin/bash
# Pre-commit hook: verify prices match between SKILL.md and index.html
# Extracts prices from both files and compares them.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
SKILL="$REPO_ROOT/SKILL.md"
INDEX="$REPO_ROOT/index.html"

errors=0

# Extract promo price from SKILL.md
skill_promo=$(grep -oP '\$\d+/hour' "$SKILL" | head -1)
# Extract standard price from SKILL.md
skill_standard=$(grep -oP '\$\d+/hour' "$SKILL" | tail -1)

# Extract promo price from index.html (from the price-amount div)
index_promo=$(grep -oP '\$\d+ <small>/ hour' "$INDEX" | head -1 | grep -oP '\$\d+')
index_standard=$(grep -oP '\$\d+ <small>/ hour' "$INDEX" | tail -1 | grep -oP '\$\d+')

# Normalize skill prices
skill_promo_num=$(echo "$skill_promo" | grep -oP '\d+')
skill_standard_num=$(echo "$skill_standard" | grep -oP '\d+')

if [ "$index_promo" != "\$$skill_promo_num" ]; then
    echo "PRICE MISMATCH: Promo price in index.html ($index_promo) != SKILL.md ($skill_promo)"
    errors=1
fi

if [ "$index_standard" != "\$$skill_standard_num" ]; then
    echo "PRICE MISMATCH: Standard price in index.html ($index_standard) != SKILL.md ($skill_standard)"
    errors=1
fi

if [ $errors -eq 0 ]; then
    echo "Price check passed: promo=$index_promo, standard=$index_standard"
fi

exit $errors
