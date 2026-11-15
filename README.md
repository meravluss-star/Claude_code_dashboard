# Micro Medical Devices — HR Recruiting Dashboard

A dashboard for the HR / Talent Acquisition team at Micro Medical Devices. It shows every open job, the candidates for each job, their CVs and hiring status, and alerts recruiters when a new CV arrives.

**Status:** Working demo with fictional data, hosted on GitHub Pages. It can show built-in sample data or connect to an Airtable base. The full spec is in [spec.md](spec.md).

**Live dashboard:** https://meravluss-star.github.io/Claude_code_dashboard/

> This repository also hosts a second, separate demo: **[Market Movers](#market-movers--daily-top-10-most-active-us-stocks)**, a stock dashboard at [`/stocks/`](https://meravluss-star.github.io/Claude_code_dashboard/stocks/).

## Features

- **Candidates by job** — list of 6 open jobs with candidate counts and a red/yellow/green mini bar; a sortable candidates table; filters by job, status and source; search by name, email or skill; summary (KPI) cards that also filter by status; and a chart of candidates per job (click a bar to filter, or view it as a table).
- **Compact table** — the candidates table fits the screen without being cut off: Name, Job, Applied, Experience, CV, Status and a View button. Source and Recruiter are shown in the CV panel. On smaller screens (under 1366 px) the job title moves under the candidate's name and the Job and Experience columns are hidden.
- **CV files** — the CV column shows a PDF (red) or DOC (blue) file icon (hover to see the file name and size); open any CV in a side panel to see the candidate details, a CV preview, and a Download button (sample CVs download as real PDF / Word files). Upload new CVs with the "Upload CV" button or drag & drop (PDF, DOC, DOCX, max 10 MB); uploaded PDFs can be previewed.
- **No duplicate candidates** — the upload form asks for phone and ID number (ת.ז, checked with the Israeli check digit). If a candidate with the same ID **or** the same phone already exists (in any format, e.g. `+972 50…` or `050-…`), no new candidate is created: a message names the existing candidate and offers "Add this CV to the existing candidate" or "Open existing candidate". The ID number is shown in the CV panel.
- **Airtable data store with duplicate flagging** — the Airtable base *HR Recruiting – Micro Medical Devices* has a `CVs` table (fictional data, 38 submissions merged into 33 candidates) grouped and sorted by job type in the view *By job type*. An automation, *Flag duplicate CVs (same ID or phone)*, links any new record to existing records with the same normalized ID or phone, and the `Duplicate check` field then shows ⚠️ Duplicate. Nothing is deleted automatically.
- **Airtable connection** — the **Airtable** button in the header connects the dashboard to the `CVs` table. When connected, the dashboard shows the Airtable rows instead of the demo data, refreshes every 30 seconds and rings the bell for new rows. A green dot on the button shows the connection is live. Status, stage, notes, new candidates (with the CV file, up to 5 MB) and blocked duplicates are saved back to Airtable. A failed save is undone and explained on screen. "Disconnect" goes back to the demo data.
  - **Security:** each user creates their own Airtable personal access token (scopes `data.records:read` and `data.records:write`, access to this base only) and pastes it in the dialog. The token is saved only in that browser's local storage and is **never** put in the code, so the public site has no secrets in it.
- **Color-coded status** — 🔴 Rejected · 🟡 In progress · 🟢 Hired, shown with color + text + icon on the status badges and in the chart. Table rows and cards stay white — color is used only for status. "In progress" shows the stage (Screening, Phone interview, Technical interview, Offer). Change status and add notes in the CV panel; every change is saved to the candidate's history. Changing a hired candidate to rejected asks for confirmation.
- **New CV bell** — bell in the header with a red counter of unread new CVs; it shakes and shows a message when a CV arrives. Click it to see the latest CVs and open one, or "Mark all as read". New candidates get a "NEW" tag. In the demo, a new CV arrives automatically after 25 seconds and then every minute, or with "Simulate new CV".
- **Mobile friendly** — layouts for desktop, tablet and phone; on phones the table becomes cards and the CV panel opens full screen.
- **Big friendly icons & big touch targets** — rounded icons (24–48 px) and buttons of at least 56 × 56 px (including the View and close buttons in pop-up messages).
- **White background** — clean white page on all devices.
- **Glowing blue logo** — the company caduceus logo, large (68 px) in clear bright blue (`#1E90FF`) with a soft, light glow.
- **Accessibility** — designed for WCAG 2.2 AA and Israeli Standard IS 5568: keyboard-only use (shortcuts `/` = search, `N` = notifications), screen-reader labels and announcements, reduced motion, English / Hebrew (right-to-left) switch, and an [accessibility statement](accessibility.html).

## Demo limitations

- All candidates are fictional — either the sample data built into the page, or the fictional rows in the Airtable `CVs` table.
- Without the Airtable connection, status changes and notes are saved only in your own browser (local storage), and uploaded CVs disappear when the page is reloaded.
- No login yet — the spec's sign-in, roles and secure CV storage need a real backend. With Airtable, every user needs their own token.
- The duplicate check runs in the browser (against Airtable data when connected). In the real system the database itself must enforce a unique ID number and phone.
- The full list of what the demo does not include is in the spec's **§0 Out of Scope** section.

## Project files

| File | What it is |
|---|---|
| [index.html](index.html) | The dashboard (one page: HTML, CSS and JavaScript) |
| [accessibility.html](accessibility.html) | Accessibility statement |
| [spec.md](spec.md) | Full dashboard specification |
| [practice.md](practice.md) | Working rules (commit & push every change, keep README updated, keep the spec and its acceptance criteria consistent) |
| README.md | This file — project description and features |
| [stocks/](stocks/) | Market Movers stock dashboard (see below) |
| [.github/workflows/update-stocks.yml](.github/workflows/update-stocks.yml) | Daily job that updates the Market Movers data |

---

## Market Movers — Daily Top 10 Most Active US Stocks

A friendly, mobile-first page in English that shows the 10 most actively traded US stocks of the last trading day. For each one it shows whether it went up or down, the news that may explain the move, and a short description of the company. Data comes from **Alpha Vantage** and updates automatically after every trading day. The full spec is in [stocks/spec.md](stocks/spec.md).

**Live page:** https://meravluss-star.github.io/Claude_code_dashboard/stocks/

### Features

- **Top 10 most active stocks**: ranked by share volume. ETFs, warrants and shares under $0.50 are left out.
- **Clear up/down marking**: green ▲ with + for gains, red ▼ with − for losses (never color alone), with % change, $ change and price.
- **Bold names**: ticker and company name in bold on every card.
- **Why it moved**: up to 3 news headlines per stock from Alpha Vantage, with source, date and news sentiment (Bullish … Bearish); each opens the article.
- **About the company**: a 1–2 sentence description, exchange, sector, industry and market cap.
- **Summary tiles**: number of gainers and losers, top gainer and top loser.
- **Filter and sort**: All / Gainers / Losers; sort by volume, biggest gain, biggest loss, price or ticker.
- **Mobile friendly**: one column on phones and tablets, two columns on desktop, white background, touch targets of at least 56 px.
- **Automatic daily update**: a GitHub Actions job runs Monday–Friday at 22:30 UTC (after the US close), fetches the data and commits it, which updates the live page.
- **Stays on the free plan**: at most 20 Alpha Vantage requests per run (free limit: 25 per day). It skips the run with 1 request if the trading day is already saved, and caches company profiles (30 days) and the ETF list (7 days).

### Setup: Alpha Vantage key

The daily job needs a free Alpha Vantage API key, stored as a GitHub repository secret (never in the code):

1. Get a free key at https://www.alphavantage.co/support/#api-key
2. In the repository, open **Settings → Secrets and variables → Actions → New repository secret**. Set the name to `ALPHA_VANTAGE_KEY` and the value to your key. You can also run `gh secret set ALPHA_VANTAGE_KEY` and paste the key when asked.
3. Optional: run it once now in **Actions → Update stock movers → Run workflow**.

### Limitations

- End-of-day data only, no live prices or charts. The page shows the starting data (Nov 13, 2026, marked with a yellow notice) until the first automatic run.
- The free key allows 25 requests a day **in total**. If the same key is also used elsewhere on the same day, some news or profiles may be skipped that day.
- "Why it moved" lists headlines, not a written analysis. For information only, not investment advice.
- The full list is in the spec's **§0 Out of Scope**.
