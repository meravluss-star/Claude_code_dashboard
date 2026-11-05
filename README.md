# Micro Medical Devices — HR Recruiting Dashboard

A dashboard for the HR / Talent Acquisition team at Micro Medical Devices. It shows every open job, the candidates for each job, their CVs and hiring status, and alerts recruiters when a new CV arrives.

**Status:** Working demo with fictional sample data, hosted on GitHub Pages. The full spec is in [spec.md](spec.md).

**Live dashboard:** https://meravluss-star.github.io/Claude_code_dashboard/

## Features

- **Candidates by job** — list of 6 open jobs with candidate counts and a red/yellow/green mini bar; a sortable candidates table; filters by job, status and source; search by name, email or skill; summary (KPI) cards that also filter by status; and a chart of candidates per job (click a bar to filter, or view it as a table).
- **CV files** — the CV column shows a PDF (red) or DOC (blue) file icon and the file size; open any CV in a side panel to see the candidate details, a CV preview, and a Download button (sample CVs download as real PDF / Word files). Upload new CVs with the "Upload CV" button or drag & drop (PDF, DOC, DOCX, max 10 MB); uploaded PDFs can be previewed.
- **Color-coded status** — 🔴 Rejected · 🟡 In progress · 🟢 Hired, shown with color + text + icon on the status badges and in the chart. Table rows and cards stay white — color is used only for status. "In progress" shows the stage (Screening, Phone interview, Technical interview, Offer). Change status and add notes in the CV panel; every change is saved to the candidate's history. Changing a hired candidate to rejected asks for confirmation.
- **New CV bell** — bell in the header with a red counter of unread new CVs; it shakes and shows a message when a CV arrives. Click it to see the latest CVs and open one, or "Mark all as read". New candidates get a "NEW" tag. In the demo, a new CV arrives automatically after 25 seconds and then every minute, or with "Simulate new CV".
- **Mobile friendly** — layouts for desktop, tablet and phone; on phones the table becomes cards and the CV panel opens full screen.
- **Big friendly icons & big touch targets** — rounded icons (24–48 px) and buttons of at least 56 × 56 px.
- **White background** — clean white page on all devices.
- **Glowing blue logo** — the company caduceus logo, large (68 px) in clear bright blue (`#1E90FF`) with a soft, light glow.
- **Accessibility** — designed for WCAG 2.2 AA and Israeli Standard IS 5568: keyboard-only use (shortcuts `/` = search, `N` = notifications), screen-reader labels and announcements, reduced motion, English / Hebrew (right-to-left) switch, and an [accessibility statement](accessibility.html).

## Demo limitations

- All candidates are fictional sample data built into the page; there is no server or database yet.
- Status changes and notes are saved only in your own browser (local storage). Uploaded CVs disappear when the page is reloaded.
- No login yet — the spec's sign-in, roles and secure CV storage need a real backend.

## Project files

| File | What it is |
|---|---|
| [index.html](index.html) | The dashboard (one page: HTML, CSS and JavaScript) |
| [accessibility.html](accessibility.html) | Accessibility statement |
| [spec.md](spec.md) | Full dashboard specification |
| [practice.md](practice.md) | Working rules (commit & push every approved feature, keep README updated) |
| README.md | This file — project description and features |
