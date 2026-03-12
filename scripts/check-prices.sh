#!/bin/bash
# Pre-commit hook: verify prices match between SKILL.md, index.html, and README.md
# Also warns about description sync and suggests SEO/marketing opportunities.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
SKILL="$REPO_ROOT/SKILL.md"
INDEX="$REPO_ROOT/index.html"
README="$REPO_ROOT/README.md"

errors=0

# --- Price checks ---

# Extract promo price from SKILL.md
skill_promo=$(grep -oP '\$\d+/hour' "$SKILL" | head -1)
skill_standard=$(grep -oP '\$\d+/hour' "$SKILL" | tail -1)

# Extract promo price from index.html (from the price-amount div)
index_promo=$(grep -oP '\$\d+ <small>/ hour' "$INDEX" | head -1 | grep -oP '\$\d+')
index_standard=$(grep -oP '\$\d+ <small>/ hour' "$INDEX" | tail -1 | grep -oP '\$\d+')

# Extract prices from README.md
readme_promo=$(grep -oP '\$\d+/hour' "$README" | head -1)
readme_standard=$(grep -oP '\$\d+/hour' "$README" | tail -1)

# Normalize
skill_promo_num=$(echo "$skill_promo" | grep -oP '\d+')
skill_standard_num=$(echo "$skill_standard" | grep -oP '\d+')
readme_promo_num=$(echo "$readme_promo" | grep -oP '\d+')
readme_standard_num=$(echo "$readme_standard" | grep -oP '\d+')

if [ "$index_promo" != "\$$skill_promo_num" ]; then
    echo "ERROR: Promo price mismatch — index.html ($index_promo) != SKILL.md ($skill_promo)"
    errors=1
fi

if [ "$index_standard" != "\$$skill_standard_num" ]; then
    echo "ERROR: Standard price mismatch — index.html ($index_standard) != SKILL.md ($skill_standard)"
    errors=1
fi

if [ "$skill_promo_num" != "$readme_promo_num" ]; then
    echo "ERROR: Promo price mismatch — SKILL.md ($skill_promo) != README.md ($readme_promo)"
    errors=1
fi

if [ "$skill_standard_num" != "$readme_standard_num" ]; then
    echo "ERROR: Standard price mismatch — SKILL.md ($skill_standard) != README.md ($readme_standard)"
    errors=1
fi

if [ $errors -eq 0 ]; then
    echo "Price check passed: promo=$index_promo, standard=$index_standard"
fi

# --- Description sync warning ---
STAGED=$(git diff --cached --name-only)
modified_count=0
for f in index.html SKILL.md README.md; do
    if echo "$STAGED" | grep -q "^${f}$"; then
        modified_count=$((modified_count + 1))
    fi
done

if [ $modified_count -gt 0 ] && [ $modified_count -lt 3 ]; then
    echo ""
    echo "WARNING: You modified $modified_count of 3 content files."
    echo "  Keep descriptions in sync across: index.html, SKILL.md, README.md"
    echo "  (This is a warning, not blocking the commit.)"
    echo ""
fi

# --- SEO article price consistency check ---
SEO_DIR="/root/space2/hababru/content/products/vibers-code-review/seo_pages"
if [ -d "$SEO_DIR" ]; then
    article_errors=0
    for source in "$SEO_DIR"/*/source.md; do
        [ -f "$source" ] || continue
        slug=$(basename "$(dirname "$source")")
        # Check Vibers-specific price mentions (near "promo", "Vibers", or in pricing tables)
        article_promo=$(grep -iP '(promo|промо|Vibers).*\$\d+/h' "$source" 2>/dev/null | grep -oP '\$\d+' | head -1 | grep -oP '\d+' || true)
        article_standard=$(grep -iP '(standard|стандарт).*\$\d+/h' "$source" 2>/dev/null | grep -oP '\$\d+' | head -1 | grep -oP '\d+' || true)

        if [ -n "$article_promo" ] && [ "$article_promo" != "$skill_promo_num" ]; then
            echo "WARNING: SEO article '$slug' has promo price \$$article_promo (canonical: \$$skill_promo_num)"
            article_errors=$((article_errors + 1))
        fi
        if [ -n "$article_standard" ] && [ "$article_standard" != "$skill_standard_num" ]; then
            echo "WARNING: SEO article '$slug' has standard price \$$article_standard (canonical: \$$skill_standard_num)"
            article_errors=$((article_errors + 1))
        fi
    done
    if [ $article_errors -eq 0 ]; then
        echo "SEO article price check passed ($(ls -d "$SEO_DIR"/*/source.md 2>/dev/null | wc -l) articles)"
    fi
fi

# --- SEO opportunities suggestion ---
# Only show when content files are being modified
if [ $modified_count -gt 0 ]; then
    echo ""
    echo "=== SEO & Marketing Suggestions ==="

    # Check diff for new features/comparisons mentioned
    DIFF=$(git diff --cached -- index.html SKILL.md README.md 2>/dev/null || true)

    # Detect new competitor mentions
    for competitor in "CodeRabbit" "SonarQube" "Codacy" "DeepSource" "PullRequest.com" "Copilot" "Cursor" "Snyk" "Semgrep" "Qodana"; do
        if echo "$DIFF" | grep -qi "+.*$competitor" 2>/dev/null; then
            slug=$(echo "$competitor" | tr '[:upper:]' '[:lower:]' | tr ' .' '-')
            existing=$(find "$SEO_DIR" -name "source.md" -path "*${slug}*" 2>/dev/null | wc -l)
            if [ "$existing" -eq 0 ]; then
                echo "  IDEA: New competitor '$competitor' mentioned — consider writing '$slug-vs-vibers' comparison article"
            fi
        fi
    done

    # Detect new feature keywords
    for keyword in "security" "spec" "hallucination" "visual" "UI" "mobile" "accessibility" "testing" "CI/CD" "monorepo"; do
        if echo "$DIFF" | grep -qi "+.*$keyword" 2>/dev/null; then
            echo "  IDEA: '$keyword' mentioned in changes — check if SEO articles cover this topic"
        fi
    done

    # Count planned vs published articles
    if [ -f "/root/space2/hababru/content/products/vibers-code-review.yaml" ]; then
        planned=$(grep -c "status: planned" "/root/space2/hababru/content/products/vibers-code-review.yaml" 2>/dev/null || echo 0)
        published=$(grep -c "status: published" "/root/space2/hababru/content/products/vibers-code-review.yaml" 2>/dev/null || echo 0)
        echo "  STATUS: $published published / $planned planned SEO articles"
    fi

    # Suggest PR opportunities
    echo ""
    echo "  PR opportunities to consider:"
    echo "    - awesome-claude-skills repos (43K+ stars)"
    echo "    - r/vibecoding, r/startups, r/SaaS (Reddit)"
    echo "    - Hacker News (Show HN: Human code review for vibecoded projects)"
    echo "    - Product Hunt launch"
    echo ""
fi

exit $errors
