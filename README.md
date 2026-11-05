# Micro Medical Devices — HR Recruiting Dashboard

A dashboard for the HR / Talent Acquisition team at Micro Medical Devices. It shows every open job, the candidates for each job, their CVs and hiring status, and alerts recruiters when a new CV arrives.

**Status:** Specification stage — the full spec is in [spec.md](spec.md). The dashboard is not built yet.

## Features

- **Candidates by job** — list of open jobs with candidate counts, a sortable and filterable candidates table, summary (KPI) cards, and a chart of candidates per job.
- **CV files** — preview and download PDF / Word CVs in a side panel; upload CVs by drag & drop or button (max 10 MB); access only for logged-in HR users.
- **Color-coded status** — 🔴 Rejected · 🟡 In progress · 🟢 Hired, always shown with color + text + icon.
- **New CV bell** — bell in the header with a counter of unread new CVs, a list of the latest arrivals, and a "NEW" tag in the table.
- **Mobile friendly** — layouts for desktop, tablet and phone; on phones the table becomes cards.
- **Big friendly icons & big touch targets** — rounded icons (24–48 px) and buttons of at least 56 × 56 px.
- **White background** — clean white page on all devices.
- **Glowing blue logo** — the company caduceus logo in bright glowing blue (`#1E90FF`).
- **Accessibility** — WCAG 2.2 AA and Israeli Standard IS 5568: keyboard-only use, screen readers (NVDA, VoiceOver), 200% zoom, reduced motion, Hebrew right-to-left support, and an accessibility statement.

## Project files

| File | What it is |
|---|---|
| [spec.md](spec.md) | Full dashboard specification |
| [practice.md](practice.md) | Working rules (commit & push every approved feature, keep README updated) |
| README.md | This file — project description and features |
