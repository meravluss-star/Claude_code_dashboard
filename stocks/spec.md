# Market Movers — Daily Top 10 Most Active US Stocks

**Spec version:** 1.0 · **Date:** 2026-11-15
**Purpose:** A friendly, mobile-first page that shows the 10 most actively traded US stocks of the last trading day. For each stock it shows whether it went up or down, by how much, the news that may explain the move, and a short description of the company. Everything is in English. Data comes from Alpha Vantage and is refreshed automatically once per trading day after the US market closes, within the Alpha Vantage free plan.

**Live page:** https://meravluss-star.github.io/Claude_code_dashboard/stocks/

---

## 0. Out of Scope (demo)

This is a static demo page on GitHub Pages with a daily GitHub Actions job. It does **not** include:

| Not included | What the demo does instead |
|---|---|
| Real-time or intraday prices | End-of-day prices, refreshed once per trading day after the close (§2.3) |
| A server or database | Data is saved as JSON files in the repository (`stocks/data/`) by a GitHub Actions job |
| User accounts, watchlists, alerts | One public page, same for everyone |
| Price charts and history | Only the last trading day is shown |
| Written analysis of *why* each stock moved | Headlines and Alpha Vantage news sentiment for each stock (§4.3); no AI or human analysis |
| Paid Alpha Vantage data (premium endpoints, more than 25 requests a day) | Free plan only, at most 20 requests per run (§2.2) |
| Investment advice or trading | Information only; the footer says so |
| Exact update time | GitHub runs scheduled jobs on a best-effort basis; the run can start some minutes after 22:30 UTC |

Acceptance criteria in §7 apply to the demo only where they do not depend on the items above.

---

## 1. Users and goal

Anyone who wants a quick, phone-friendly look at "what was hot on Wall Street today": which stocks traded the most, whether they rose or fell, and why.

## 2. Data

### 2.1 Source and selection

| Item | Alpha Vantage function | Use |
|---|---|---|
| Most active stocks, price, change, % change, volume | `TOP_GAINERS_LOSERS` (`most_actively_traded`) | The list of 10 stocks and their numbers |
| Stock vs. ETF, company name | `LISTING_STATUS` | Removes ETFs; name when no profile exists yet |
| News and sentiment | `NEWS_SENTIMENT` (one request per stock, `tickers=<symbol>`) | "In the news: why it moved" |
| Company profile | `COMPANY_OVERVIEW` | About text, exchange, sector, industry, market cap |

**Selection rules** (applied to the 20 most actively traded tickers, in order of share volume):
1. Common stocks only: **ETFs are removed** (asset type from `LISTING_STATUS`).
2. Warrants, rights and units are removed (5-letter symbols ending in W, R or U whose 4-letter root is listed; symbols with `+` or `.`).
3. Shares priced **under $0.50** are removed.
4. The top **10** that remain, by volume, are shown. On a day when fewer than 10 qualify, fewer are shown.

### 2.2 Free-plan request budget

The Alpha Vantage free plan allows **25 requests per day**. The update job never makes more than **20 requests per run** (hard limit in the script), leaving 5 for manual checks. It waits **13 seconds** between requests (under 5 per minute).

| Step | Requests | When |
|---|---|---|
| Most active stocks | 1 | Every run |
| Stock/ETF list | 1 | Once every 7 days |
| News, one per stock | up to 10 | Every new trading day |
| Company profiles | whatever is left of the 20 | Only for stocks with no profile, or a profile older than 30 days |
| **Total** | **≤ 20** | Typical day: 12–15 |

If the trading day returned by Alpha Vantage is already saved (weekend, holiday, or a second run), the job stops after **1 request**. If a request is refused (limit message), that stock keeps an empty news list or its cached profile, and the run still saves the rest.

### 2.3 Schedule

- GitHub Actions workflow `.github/workflows/update-stocks.yml`, **Monday–Friday at 22:30 UTC** (5:30 PM New York time in winter, 6:30 PM in summer), after the 4:00 PM close.
- It can also be started by hand (Actions → *Update stock movers* → *Run workflow*), with "Test only" (no requests) or "Force" (refresh the same day again) options.
- The API key is stored as the repository secret `ALPHA_VANTAGE_KEY`. It is never in the code or the page.
- The job runs the tests first (§6), then fetches, then commits `stocks/data/` only if it changed. The commit updates GitHub Pages.

### 2.4 Files

| File | Content |
|---|---|
| `stocks/data/latest.json` | What the page shows: trading date, update time, number of requests used, 10 stocks |
| `stocks/data/cache.json` | Stock/ETF list and company profiles kept between runs (saves requests) |
| `stocks/scripts/update_stocks.py` | Update script (Python standard library only) |
| `stocks/tests/test_update.py` + `fixtures/` | Tests with saved sample responses |

**Starting data:** until the first automatic run, `latest.json` holds the Nov 13, 2026 prices from Alpha Vantage, with company summaries and headlines added by hand. It has `"seed": true`, and the page shows a yellow notice saying so. The first automatic run replaces it.

## 3. Look and feel

| Rule | Spec |
|---|---|
| Background | **White** (`#FFFFFF`) on every device; cards are white with a light gray border `#E3EAF2` and soft shadow |
| Language | **English** only, left-to-right |
| Stock name | **Ticker bold** (weight 800, 22 px on phone / 24 px from 600 px) and **company name bold** (weight 700, 16 px) |
| Price | 22 px (phone) / 24 px, weight 700 |
| Up (gain) | Standard market marking: **green ▲ and a + sign**, text `#137333` on `#E6F4EA` |
| Down (loss) | **Red ▼ and a − sign**, text `#C5221F` on `#FCE8E6` |
| Unchanged | Gray ■, text `#5F6368` on `#F1F3F4` |
| Color is never the only signal | Every change shows an arrow and a +/− sign as well as color; screen readers hear "up 2.34 percent" / "down …" |
| Touch targets | Every button, the sort menu and every headline link are at least **56 px** tall (buttons also ≥ 56 px wide) |
| Text | Body 16 px; secondary text at least 13 px; all text passes 4.5 : 1 contrast |

### 3.1 Layout

```
┌──────────────────────────────────────────────┐
│ [icon] Market Movers                         │
│        Top 10 most actively traded US stocks │
│ Trading day · Updated · Source               │
├──────────┬──────────┬───────────┬────────────┤
│ Gainers  │ Losers   │ Top gainer│ Top loser  │  ← summary tiles
├──────────┴──────────┴───────────┴────────────┤
│ [ All | ▲ Gainers | ▼ Losers ]   Sort by [▾] │
├──────────────────────────────────────────────┤
│ #1  NVDA                         $162.85     │
│     NVIDIA Corporation           ▼ −2.01%    │
│     NASDAQ · Technology          −$3.34      │
│     Volume 360.8M · Market cap · Rank #1     │
│     ABOUT  short company description         │
│     IN THE NEWS: WHY IT MOVED                │
│     • Headline (source · date · sentiment)   │
└──────────────────────────────────────────────┘
```

| Screen | Layout |
|---|---|
| Phone (< 600 px) | One column; summary tiles 2 × 2; filter counts hidden under 440 px; rank circle hidden under 380 px; no horizontal scroll at 375 px |
| Tablet (600–1023 px) | One column; summary tiles in one row of 4 |
| Desktop (≥ 1024 px) | Stock cards in **2 columns**; page max width 1200 px |

## 4. Content

### 4.1 Header
Title "Market Movers", subtitle, and a line with the trading day (e.g. "Friday, November 13, 2026"), the update time (in the viewer's time zone) and the source.

### 4.2 Summary tiles
Gainers count (▲, green), Losers count (▼, red), Top gainer (biggest % gain, ticker + name), Top loser (biggest % loss, ticker + name).

### 4.3 Stock card
Rank, **ticker**, **company name**, exchange · sector · industry, price, % change pill, $ change, volume, market cap (when known), "About" (first 1–2 sentences of the company description, max 300 characters), and "In the news: why it moved": up to **3** headlines from the trading day and the day before, with relevance to the stock ≥ 0.2, newest first. Each headline shows its source, date and Alpha Vantage sentiment (Bullish / Somewhat Bullish / Neutral / Somewhat Bearish / Bearish) and opens in a new tab. When there is no news: "No major headlines found for this stock on this trading day."

### 4.4 Filter and sort
Filter: All / ▲ Gainers / ▼ Losers (with counts). Sort: Volume (default), Biggest gain, Biggest loss, Price, Ticker A–Z.

### 4.5 Footer
Data source and update rule, the meaning of ▲/▼, the selection rule (no ETFs, warrants, or shares under $0.50), and **"For information only. This is not investment advice."**

### 4.6 Loading and errors
Gray placeholder cards while loading. If the data cannot be loaded: a message and a **Try again** button (≥ 56 × 56 px).

## 5. Accessibility
WCAG 2.2 AA: page language `en`, "Skip to the stock list" link, headings in order (h1 → h2 → h3 per ticker → h4 sections), filter buttons use `aria-pressed`, list updates announced (`aria-live`), visible focus ring, reduced motion respected, full keyboard use.

## 6. Tests
`python stocks/tests/test_update.py` (runs at the start of every workflow run) checks: ETFs and sub-$0.50 shares are removed and the 10 are ordered by volume; at most 20 requests; a same-day rerun uses 1 request; cached listing and profiles are not requested again; a limit message for one stock does not stop the run; `AV_MAX_CALLS` is never exceeded; a missing API key fails with a clear message and writes nothing.

## 7. Acceptance Criteria

1. The page shows the 10 most actively traded US common stocks of the last trading day, ordered by volume, with **no ETFs, warrants, or shares under $0.50** (§2.1).
2. Each card shows the **bold ticker** (weight 800, 22/24 px) and **bold company name** (weight 700, 16 px), price, % change, $ change, volume, an About text, and up to 3 headlines, or the "no headlines" message (§4.3).
3. Gains show **green ▲ with +**, losses **red ▼ with −**, in the colors in §3; never color alone.
4. The page background is **white** on phone, tablet and desktop.
5. All text on the page is in **English**.
6. At **375 px** width there is no horizontal scroll and cards are one column; at **≥ 1024 px** cards are in 2 columns.
7. Every button, the sort menu and every headline link are **≥ 56 px** tall; buttons are also ≥ 56 px wide (including **Try again**).
8. Filters (All / Gainers / Losers) and all 5 sort options work, and the counts match the summary tiles.
9. The update job runs Monday–Friday at 22:30 UTC, makes **at most 20** Alpha Vantage requests per run (free plan: 25/day), and makes only **1** request when the trading day is already saved (§2.2).
10. After a successful run, `stocks/data/latest.json` has the new trading date, `"seed": false`, and the live page shows it.
11. The API key is only in the repository secret `ALPHA_VANTAGE_KEY`, never in the code or the page.
12. The tests in §6 pass before every update.
13. The footer says the data is for information only and is not investment advice.
