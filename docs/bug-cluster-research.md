# Bug Cluster Research — VibeCheck Content Strategy
*Researched 2026-04-18 by research-agent*

## Methodology
- **Stack Overflow:** top 20 questions per tag by votes, via Stack Exchange API (`/2.3/questions?sort=votes&tagged=…&pagesize=20`). Tags: `react`, `wordpress`, `woocommerce`, `next.js`, `css-flexbox`, `css-grid`, `react-hooks`, `web3js`, `ethers.js`, `solidity`, `nft`. View counts captured directly.
- **GitHub:** REST API `/repos/{repo}/issues?labels=bug&sort=reactions&direction=desc` for `facebook/react`, `vercel/next.js`, `WordPress/gutenberg`, `woocommerce/woocommerce`, `ethers-io/ethers.js`, `Uniswap/interface`. (Gutenberg uses non-standard label scheme; surfaced 0 results — skipped.)
- **Noxon expertise verified** against `gh api users/noxonsu/repos`: top stacks are MultiCurrencyWallet (TypeScript/React, 540⭐), NFTsy (WordPress/PHP NFT plugin, 14⭐), unifactory/launchpad (Solidity), definance (DEX), LotteryFactory, swap.react. Strong: React + Web3 + WordPress crypto plugins. Weak: Next.js App Router, native Solana, Gutenberg block editor internals.
- **Volume estimate** is based on SO `view_count` as proxy: <50k = low, 50–300k = medium, >300k = high, >1M = very high.

## Summary
- Bugs analyzed: 165 SO questions across 11 tags + ~30 GitHub bug issues across 6 repos
- Recommended for articles: 30 (listed below)
- Top 3 niches by ROI = volume × Noxon credibility × VibeCheck visual-fit:
  1. **WordPress/WooCommerce visual + checkout bugs** — Noxon owns NFTsy; WooCommerce checkout is a perfect "click element → file bug" demo.
  2. **React state/effect bugs in AI-coded apps** — highest pure search volume; matches Noxon's MultiCurrencyWallet daily fight; perfect handoff to AI flow.
  3. **Web3 wallet/DEX UX bugs** (MetaMask connect, chain switch, gas estimate, ENS, allowance) — almost no other content creator has Noxon's first-hand DEX-fork credibility.

## Top 30 Bug Candidates (ranked)

### [1] React useState set method not reflecting change immediately
- **SO:** https://stackoverflow.com/questions/54069253 (928,807 views, score 908)
- **Search query:** "react usestate not updating"
- **Volume estimate:** very high (~929k views)
- **VibeCheck fit:** B (logic bug; AI-fix flow shines — paste console + repro into Claude)
- **Noxon expertise:** Yes — MultiCurrencyWallet runs deep React state
- **Article angle:** "useState not updating: the 4 patterns AI keeps generating wrong (with real PR diffs from a 540-star wallet)"
- **Banner scenario:** click stale counter on a demo page → VibeCheck captures `setCount(count+1)` in code panel + console shows old value → AI handoff with stale-closure fix

### [2] How to fix missing dependency warning when using useEffect
- **SO:** https://stackoverflow.com/questions/55840294 (1,253,172 views, 890)
- **Search query:** "react useeffect missing dependency warning"
- **Volume:** very high
- **VibeCheck fit:** B
- **Noxon expertise:** Yes
- **Angle:** "exhaustive-deps warnings: when to obey, when to silence — 6 real cases from MCW"
- **Banner:** click broken refresh button → AI proposes proper deps array

### [3] useEffect called twice with empty deps (StrictMode)
- **SO:** https://stackoverflow.com/questions/60618844 (597,842 views, 808)
- **Search query:** "useeffect runs twice"
- **Volume:** very high
- **VibeCheck fit:** B
- **Noxon expertise:** Yes
- **Angle:** "StrictMode double-fire: which side effects to make idempotent (wallet connect example)"
- **Banner:** wallet connect fires twice → VibeCheck console snapshot

### [4] React Hydration failed: initial UI does not match (Next.js / React 18)
- **SO:** https://stackoverflow.com/questions/71706064 (687,219 views, 341)
- **Search query:** "hydration failed initial ui does not match"
- **Volume:** very high
- **VibeCheck fit:** A (hydration mismatch is visually catchable — flicker of two layouts) + B
- **Noxon expertise:** Partial (React strong, Next App Router less)
- **Angle:** "hydration mismatch: the 5 culprits VibeCheck catches in 1 click (date, locale, window, theme, ad scripts)"
- **Banner:** `Date.now()` in JSX → mismatch warning auto-captured + element pinpointed

### [5] React Hook warnings for async function in useEffect
- **SO:** https://stackoverflow.com/questions/53332321 (923,217 views, 593)
- **Search query:** "useeffect async function warning"
- **Volume:** very high
- **VibeCheck fit:** B
- **Noxon expertise:** Yes
- **Angle:** "async useEffect: copy-paste pattern that doesn't break on unmount"

### [6] Invalid hook call. Hooks can only be called inside function component
- **SO:** https://stackoverflow.com/questions/56663785 (1,083,169 views, 354)
- **Search query:** "invalid hook call"
- **Volume:** very high
- **VibeCheck fit:** B
- **Noxon expertise:** Yes
- **Angle:** "Invalid hook call — 3 root causes (duplicate React, conditional, library mismatch)"

### [7] window is not defined in Next.js
- **SO:** https://stackoverflow.com/questions/55151041 (662,908 views, 332)
- **Search query:** "window is not defined nextjs"
- **Volume:** very high
- **VibeCheck fit:** C (SSR/build-time; needs human or AI with file context — VibeCheck collects URL + console)
- **Noxon expertise:** Partial
- **Angle:** "window is not defined: typeof window vs dynamic import vs useEffect — pick one (decision table)"

### [8] React-router URLs don't work when refreshing
- **SO:** https://stackoverflow.com/questions/27928372 (924,001 views, 1306)
- **Search query:** "react router 404 on refresh"
- **Volume:** very high
- **VibeCheck fit:** A (404 is visible) + C (server config fix)
- **Noxon expertise:** Yes (MCW deploys SPA)
- **Angle:** "SPA 404 on refresh: nginx, Apache, Vercel, Netlify configs that actually work"

### [9] Detect click outside React component
- **SO:** https://stackoverflow.com/questions/32553158 (1,016,024 views, 937)
- **Search query:** "react detect click outside"
- **Volume:** very high
- **VibeCheck fit:** A — perfect demo (click open menu → menu doesn't close → file bug on the menu element)
- **Noxon expertise:** Yes
- **Angle:** "Modal/dropdown won't close: ref pattern, portal pitfall, mobile touch event"

### [10] WooCommerce — Get current product id (and similar object-API bugs)
- **SO:** https://stackoverflow.com/questions/27385920 (304,692 views, 64) — and 15 sibling Q's
- **Search query:** "woocommerce get current product id" + cluster
- **Volume:** medium-high (cluster sums ~3M views)
- **VibeCheck fit:** A (broken price display, stale cart count — clickable)
- **Noxon expertise:** Yes (NFTsy is a WP/Woo plugin)
- **Angle:** Cluster pillar: "WooCommerce 9 hooks cheat sheet for vibe-coders — 10 fixes shipped from a real plugin (NFTsy)"

### [11] WooCommerce Safari autocomplete overwrites shipping address state
- **GitHub:** https://github.com/woocommerce/woocommerce/issues/60958 (8 reactions)
- **Search query:** "woocommerce safari shipping address billing autocomplete"
- **Volume:** low (niche but high-pain — checkout = revenue)
- **VibeCheck fit:** A — textbook ("click on the wrong-state field → bug report with browser + autocomplete state")
- **Noxon expertise:** Yes
- **Angle:** "Safari autocomplete is overwriting WooCommerce shipping state — here's the 12-line fix"
- **Banner:** Safari iframe → checkout → state field flips → VibeCheck captures form state + UA

### [12] WooCommerce Checkout Block subscribe function not executing on page load (Chrome)
- **GitHub:** https://github.com/woocommerce/woocommerce/issues/43440 (9 reactions)
- **Search query:** "woocommerce checkout block subscribe not firing chrome"
- **VibeCheck fit:** A+B
- **Noxon expertise:** Yes
- **Angle:** "Checkout Block subscribe race condition — what AI gets wrong"

### [13] WordPress: PHP POST Content-Length exceeds limit (file upload broken)
- **SO:** https://stackoverflow.com/questions/11719495 (684,438 views, 319)
- **Search query:** "post content-length exceeds limit wordpress"
- **Volume:** very high
- **VibeCheck fit:** A (broken upload UI is clickable; VibeCheck grabs network 413/500)
- **Noxon expertise:** Yes
- **Angle:** "Upload silently fails on WP: which limit (PHP / nginx / Cloudflare) and how to read the trace"

### [14] WordPress nginx serves .php as downloads
- **SO:** https://stackoverflow.com/questions/25591040 (410,081 views, 221)
- **Search query:** "nginx php downloads instead of executing"
- **Volume:** high
- **VibeCheck fit:** A (visible: file downloads instead of page load — VibeCheck records URL + response headers)
- **Noxon expertise:** Yes (runs WP nginx daily)
- **Angle:** "PHP downloading instead of executing: minimal nginx fastcgi block"

### [15] WordPress utf8mb4_unicode_520_ci unknown collation (DB import)
- **SO:** https://stackoverflow.com/questions/42385099 (806,663 views, 368)
- **Search query:** "unknown collation utf8mb4_unicode_520_ci"
- **Volume:** very high
- **VibeCheck fit:** D (CLI/DB; VibeCheck is browser-only) → SKIP
- **Noxon expertise:** Yes but wrong tool match

### [16] Flexbox: center horizontally and vertically
- **SO:** https://stackoverflow.com/questions/19026884 (1,870,313 views, 1005)
- **Search query:** "flexbox center vertically"
- **Volume:** very high
- **VibeCheck fit:** A — visual bug, click misaligned div → file fix
- **Noxon expertise:** Generic frontend (any dev)
- **Angle:** "5 flexbox centering patterns AI gets backwards (with screenshots before/after)"

### [17] Flexbox children 100% height of their parent
- **SO:** https://stackoverflow.com/questions/15381172 (1,683,649 views, 940)
- **Search query:** "flex child 100% height"
- **Volume:** very high
- **VibeCheck fit:** A
- **Noxon expertise:** Generic
- **Angle:** "100% height in flex column: the parent-chain rule + min-height: 0 trick"

### [18] CSS Grid: prevent content from expanding grid items
- **SO:** https://stackoverflow.com/questions/43311943 (395,867 views, 392)
- **Search query:** "grid item expands beyond container"
- **Volume:** high
- **VibeCheck fit:** A — overflow is the canonical "click element to file" demo
- **Noxon expertise:** Generic
- **Angle:** "minmax(0, 1fr) — the one rule that fixes 80% of CSS Grid overflow"

### [19] How to set focus on input field after rendering (React)
- **SO:** https://stackoverflow.com/questions/28889826 (1,153,449 views, 995)
- **Search query:** "react autofocus input"
- **Volume:** very high
- **VibeCheck fit:** A (visible: autofocus missing; user clicks the input → reports it)
- **Noxon expertise:** Yes
- **Angle:** "Autofocus in React: useRef + useEffect + the modal portal gotcha"

### [20] Next.js scroll position resets when search params update
- **GitHub:** https://github.com/vercel/next.js/issues/49087 (98 reactions)
- **Search query:** "next js scroll position reset search params"
- **Volume:** medium (rising)
- **VibeCheck fit:** A — "page jumps to top, click here to file" → captures URL change + scroll
- **Noxon expertise:** Partial
- **Angle:** "Next.js App Router scroll reset on filter change: scroll={false} + manual restore pattern"

### [21] Next.js high memory usage in deployed app
- **GitHub:** https://github.com/vercel/next.js/issues/49929 (95 reactions)
- **Search query:** "nextjs high memory usage production"
- **Volume:** medium
- **VibeCheck fit:** D — server-side, no DOM signal → SKIP for now

### [22] How to connect ethers.js with MetaMask
- **SO:** https://stackoverflow.com/questions/60785630 (67,958 views, 30)
- **Search query:** "connect metamask ethers.js"
- **Volume:** medium
- **VibeCheck fit:** A — "Connect Wallet button does nothing" is iconic Web3 bug; VibeCheck grabs `window.ethereum` state + console
- **Noxon expertise:** Yes — MultiCurrencyWallet does this every day, multiple chains
- **Angle:** "Connect Wallet does nothing: 7 reasons (no provider, multiple injections, mobile deeplink, locked, wrong chain, popup blocked, Brave shield)"
- **Banner:** click Connect → no popup → VibeCheck reports providers detected + chainId

### [23] How to trigger change blockchain network request on MetaMask
- **SO:** https://stackoverflow.com/questions/68252365 (17,518 views, 22)
- **Search query:** "metamask switch network programmatically"
- **Volume:** medium
- **VibeCheck fit:** A
- **Noxon expertise:** Yes (MCW supports 10+ chains)
- **Angle:** "wallet_switchEthereumChain — the unknown-chain fallback most copy-paste snippets miss"

### [24] How to check if MetaMask is connected after page refresh
- **SO:** https://stackoverflow.com/questions/71184100 (24,346 views, 21)
- **Search query:** "metamask connected after refresh"
- **Volume:** medium
- **VibeCheck fit:** A
- **Noxon expertise:** Yes
- **Angle:** "Persisting wallet connection: eth_accounts vs eth_requestAccounts (and why localStorage flag is wrong)"

### [25] Ethers.js — chainId is called every time the provider is used
- **GitHub:** https://github.com/ethers-io/ethers.js/issues/901 (14 reactions)
- **Search query:** "ethers eth_chainId every call slow"
- **Volume:** low-medium
- **VibeCheck fit:** A (slow page → VibeCheck captures network waterfall flooded with eth_chainId)
- **Noxon expertise:** Yes
- **Angle:** "Why your dApp does 200 eth_chainId/min — provider caching pattern"

### [26] Ethers — uncatchable "missing v" when sending transaction
- **GitHub:** https://github.com/ethers-io/ethers.js/issues/4513 (13 reactions)
- **Search query:** "ethers missing v error transaction"
- **VibeCheck fit:** B
- **Noxon expertise:** Yes
- **Angle:** "ethers v6 'missing v' on hardware wallets: signature mismatch root cause"

### [27] Uniswap interface — high CPU load, unresponsive
- **GitHub:** https://github.com/Uniswap/interface/issues/3706 (5 reactions)
- **Search query:** "uniswap high cpu unresponsive"
- **Volume:** low (but Noxon's exact niche — unifactory)
- **VibeCheck fit:** A (visible: laggy UI; VibeCheck grabs perf trace)
- **Noxon expertise:** Yes (unifactory = Uniswap fork with admin panel)
- **Angle:** "Why your Uniswap fork hangs at 100% CPU: re-render storm in TokenList — diff from a real fork"

### [28] estimateGas failed on Uniswap removeLiquidity
- **GitHub:** https://github.com/Uniswap/interface/issues/1318 (4 reactions, 1582 also)
- **Search query:** "estimategas failed removeliquidity uniswap"
- **VibeCheck fit:** B (catches the UI message + tx params)
- **Noxon expertise:** Yes
- **Angle:** "estimateGas failed on removeLiquidityWithPermit: deadline math + slippage caveat"

### [29] ERC721 transfer caller is not owner nor approved
- **SO:** https://stackoverflow.com/questions/69302320 (15,252 views, 7)
- **Search query:** "erc721 transfer caller is not owner nor approved"
- **Volume:** low-medium
- **VibeCheck fit:** B (Mint button errors → VibeCheck logs revert reason)
- **Noxon expertise:** Yes (NFTsy)
- **Angle:** "ERC721 transferFrom revert: setApprovalForAll vs approve, with a real lazy-mint flow"

### [30] Verify user is owner of an NFT via MetaMask connection
- **SO:** https://stackoverflow.com/questions/69395126 (5,409 views, 12)
- **Search query:** "verify nft ownership metamask"
- **VibeCheck fit:** B
- **Noxon expertise:** Yes (NFTsy ships exactly this)
- **Angle:** "Token-gated content the right way: nonce + signature + balanceOf (NFTsy pattern)"

---

## Recommended Bug Clusters

### Cluster 1 — WordPress/WooCommerce visual + checkout bugs (Noxon's NFTsy turf)
**Why:** WooCommerce checkout is the highest-revenue surface in WP; bugs are visual and clickable; Noxon ships a Woo-adjacent NFT plugin (NFTsy) so first-hand. Existing landing already demos a WP banner.
- 1. Safari autocomplete overwrites shipping state in Checkout Block (#11)
- 2. WooCommerce 9 hooks cheat sheet — 10 fixes from NFTsy (#10)
- 3. Checkout Block subscribe race on page load (#12)
- 4. PHP upload limit chain (PHP / nginx / Cloudflare) (#13)
- 5. nginx serves .php as download — minimal vhost (#14)
- 6. ERC721 token-gated WP content done right (#30) — bridges to crypto cluster

### Cluster 2 — React state/effect bugs in AI-coded apps
**Why:** Highest pure search demand (4 of top 10 SO React-hooks questions). Every Cursor/Claude user hits these weekly. Noxon's MCW codebase has 100+ hook patterns to mine for real diffs.
- 1. useState not updating after fetch — 4 wrong AI patterns (#1)
- 2. useEffect missing-dependency warning — when to obey/silence (#2)
- 3. useEffect runs twice in StrictMode — idempotency rules (#3)
- 4. Invalid hook call — 3 root causes (#6)
- 5. Hydration mismatch — 5 culprits VibeCheck catches in 1 click (#4)
- 6. Detect click outside (modal/dropdown won't close) (#9) — best landing demo

### Cluster 3 — Web3 wallet & DEX UX bugs (Noxon's deepest moat)
**Why:** Almost no-one combines (a) crypto credibility (b) frontend writing (c) tooling that captures `window.ethereum`. Noxon owns MCW + unifactory + launchpad. Lower volume per article but near-zero competition + perfect E-E-A-T.
- 1. "Connect Wallet does nothing": 7 root causes (#22)
- 2. wallet_switchEthereumChain — unknown-chain fallback (#23)
- 3. Persist wallet connection across refresh (#24)
- 4. eth_chainId flood — provider caching (#25)
- 5. Uniswap fork at 100% CPU — TokenList re-render storm (#27)
- 6. estimateGas failed on removeLiquidity — deadline + slippage (#28)
- 7. ERC721 transferFrom revert: setApprovalForAll caveat (#29)

### Cluster 4 (optional, generic) — CSS Flexbox/Grid layout traps
**Why:** Massive volume but zero E-E-A-T moat; treat as funnel-top filler only after clusters 1–3 ship. Use only as "demo this with VibeCheck in 5s" content, not pillars.
- Flexbox center vertically (#16), 100% child height (#17), Grid overflow with minmax (#18), Right-align flex item, gap between items.

---

## Anti-recommendations — what NOT to write

- **Solana / Candy Machine NFT** (SO #70597753, #69701491). Noxon has zero Solana repos; would be scaled-content-trap material under March-2026 Google rules.
- **DB / collation / phpMyAdmin** (#15). VibeCheck is a browser tool — no DOM signal, no demo, doesn't fit the product.
- **Generic "what does X do" questions** ("difference between npx and npm", "what are the three dots in React"). High volume, but they're concept questions not bugs — wrong intent for VibeCheck CTAs.
- **Next.js memory / RSC server bugs** (#21, #46756). Server-side, invisible to a browser bug-reporter; outside Noxon's stack focus.
- **Solidity language basics** ("memory keyword", "address(0)", "msg.sender"). Concept questions, not bugs; better-served by existing Solidity docs.
- **Hardhat / Truffle CLI errors** (e.g. "Error connecting to localhost after npx hardhat run"). CLI surface, not browser; no VibeCheck angle.
- **WordPress FTP credentials prompt** — config issue, no UI bug to click on.

---

## Final report (≤150 words)

Top 3 clusters to own:

1. **WordPress + WooCommerce checkout/visual bugs** — Noxon's NFTsy plugin gives him real WP/Woo PRs to cite; Checkout-Block bugs are textbook "click broken element → file report" demos that show off VibeCheck better than any React demo.
2. **React state/effect bugs (useState/useEffect/hydration)** — by far the highest search volume (4 questions >900k SO views each); perfect handoff to the free AI-fix flow; Noxon's 540-star MultiCurrencyWallet supplies real diffs.
3. **Web3 wallet & DEX UX** ("Connect Wallet does nothing", chain switch, gas estimate, ERC721 approve) — lowest competition, highest E-E-A-T moat (unifactory + MCW + NFTsy).

**Suggested first article:** "useState not updating after fetch — the 4 patterns AI keeps generating wrong, with real PR diffs from a 540-star wallet" (Cluster 2 #1). It hits maximum volume, is easy to demo with VibeCheck (counter banner), and lets Noxon establish authority via MCW PRs in the very first piece.
