# Micro Medical Devices — HR Recruiting Dashboard

**Spec version:** 1.3 · **Date:** 2026-11-15 (1.2: 2026-11-15, 1.1: 2026-11-12, 1.0: 2026-11-05)
**Owner:** HR / Talent Acquisition
**Purpose:** One screen where recruiters see every open job, the candidates for each job, their CV files and hiring status, with an alert when a new CV arrives. The dashboard works on desktop, tablet and mobile.

> **Scope of this version:** this spec describes the full target system. What was actually built is a **front-end demo** (one HTML page with fictional data). Sections 4–6 and parts of 3 describe the future real system — see **§0 Out of Scope** for exactly what the demo does *not* include.

---

## 0. Out of Scope (demo version 1.0)

The demo on GitHub Pages is a static page with no server. The following parts of this spec are **not** included in the demo and are planned for a later, real version:

| Not in the demo | Spec section | What the demo does instead |
|---|---|---|
| Login, company SSO, user roles (HR Admin, Recruiter, Hiring Manager) | §6 | No login — anyone with the link sees the demo |
| Backend server and REST API (`/api/...`) | §5 | Without Airtable: data is built into the page. With Airtable connected (§3.7): the page calls the Airtable REST API directly from the browser |
| Database and real candidate data | §4 | Fictional candidates only — either built-in sample data, or the fictional rows in the Airtable `CVs` table (§3.7) |
| Secure / encrypted CV storage, HTTPS-only file access, access log of CV views | §3.2, §6 | Sample CVs are generated in the browser. With Airtable connected, uploaded CVs (max 5 MB) are attached in Airtable; without it they live only in memory and disappear on reload |
| Data retention and deletion by privacy law (GDPR / Israeli Privacy Protection Law) | §6 | Not applicable — no real personal data is stored |
| Saving the full change history for all users | §3.3 | With Airtable connected, status, stage and notes are saved in Airtable for everyone; the step-by-step history stays in the user's own browser. Without Airtable, everything is saved only in the browser (`localStorage`) |
| Real new-CV notifications (WebSocket / push) | §3.4 | With Airtable connected: polling every 30 s. Without it: a simulated new CV after 25 s, then every minute, or via "Simulate new CV" |
| Login and a server that keeps the Airtable token secret | §3.7, §6 | Each user pastes their own Airtable personal access token; it is stored only in their browser, never in the site's code |
| Date-range filter and filter bottom sheet on mobile | §3.1, §3.5 | Filters by job, status, source and free-text search |
| Formal accessibility testing (axe / Lighthouse ≥ 95, NVDA, VoiceOver) and a real accessibility contact | §7.7 | Built to WCAG 2.2 AA guidelines; accessibility statement page included |
| Database **unique constraint** on ID number and phone (duplicates impossible at the data level) | §3.6, §4 | The upload form checks for duplicates before adding (against Airtable data when connected); an Airtable automation flags any duplicate that is added another way (§3.6) |

Acceptance criteria in §8 apply to the demo only where they do not depend on the items above.

---

## 1. Branding & Logo

### 1.1 Logo
The logo keeps the look of the current company mark — a **caduceus** (winged staff with two serpents) above the wordmark **"MICRO MEDICAL DEVICES"** in small caps — but in a clearer, brighter, **glowing blue**.

| Element | Spec |
|---|---|
| Symbol | Caduceus: vertical staff, two spread wings at the top, two serpents twisting around the staff, small round knob on top |
| Main color | Bright medical blue `#1E90FF` (replaces the faded lavender‑blue of the old logo) |
| Highlight color | Light cyan `#7FD4FF` for inner edges / highlights |
| Glow | Soft, light glow that keeps the edges sharp: `filter: drop-shadow(0 0 3px rgba(30,144,255,.45))` |
| Wordmark | "MICRO MEDICAL DEVICES", serif small caps, color `#0B5ED7`, letter-spacing `0.08em` |
| Format | Inline SVG (sharp on every screen, can be recolored by CSS) |
| Sizes | Header: 68 px tall (mobile 56 px) · Login/splash: 160 px tall |
| Background | Always shown on the white page background, where the blue glow stands out clearly |

Placement: top-left of the header, symbol + wordmark on desktop, **symbol only** on mobile (< 600 px).

### 1.2 Colors

**White background:** the whole dashboard uses a clean **white background** (`#FFFFFF`). No dark mode — the page stays white on every device and system setting. Cards are separated from the page by a light gray border and soft shadow, not by a colored background.

| Token | Value | Use |
|---|---|---|
| `--brand` | `#1E90FF` | Logo, links, active tab, primary buttons |
| `--bg` | `#FFFFFF` | Page background (white) |
| `--surface` | `#FFFFFF` | Cards, tables (white) |
| `--border` | `#E3EAF2` | Card and table borders |
| `--shadow` | `0 2px 8px rgba(21,32,43,.08)` | Soft card shadow |
| `--text` | `#15202B` | Body text |
| `--status-rejected` | `#E53935` (red) | Rejected candidates |
| `--status-progress` | `#FFE11A` (yellow) | Candidates in progress |
| `--status-hired` | `#43A047` (green) | Hired candidates |

Status is never shown by color alone — every colored badge also has a text label and an icon (✕ / ⏳ / ✓) so it is readable for color-blind users.

### 1.3 Big Friendly Icons

The dashboard uses **large, rounded, friendly icons** everywhere, so it is easy to understand at a glance and easy to tap.

| Rule | Spec |
|---|---|
| Style | Rounded, filled or thick-outline icons (soft corners, 2.5 px stroke), one consistent icon set (e.g. Material Symbols Rounded or Phosphor "bold") |
| Size — header (bell, search, profile) | **32 px** icon |
| Size — KPI cards | **48 px** icon inside a 72 px colored circle |
| Size — table / card actions (view CV, change status, note) | **28 px** icon |
| Size — status badges | **24 px** icon next to the text |
| Labels | Every icon button has a visible text label or tooltip — icons never stand alone |
| Color | Brand blue for actions; red / yellow / green for status icons |

Icons used:

| Meaning | Icon |
|---|---|
| New CV bell | 🔔 bell |
| CV file | 📄 document (red for PDF, blue for DOCX) |
| Jobs | 💼 briefcase |
| Candidates | 👥 people |
| Hired | ✅ check circle (green) |
| In progress | ⏳ hourglass (yellow) |
| Rejected | ❌ x circle (red) |
| Upload CV | ⬆️ cloud upload |
| Search / Filter | 🔍 magnifier / ⚙️ sliders |

### 1.4 Big Touch Targets

| Element | Minimum size |
|---|---|
| All buttons and icon buttons | **56 × 56 px** (above the 44 px standard) |
| Bell, search, profile in header | 56 × 56 px tap area |
| Table rows / candidate cards | Row height **64 px** minimum; whole card is tappable |
| Status dropdown, filter chips | 48 px tall, 16 px horizontal padding |
| Space between tappable items | At least **12 px** so fingers don't hit the wrong one |
| Body text | 16 px minimum (18 px on mobile); buttons text 18 px semibold |

---

## 2. Layout

```
┌───────────────────────────────────────────────────────────────┐
│ [Glowing logo] Micro Medical Devices      🔍 Search   🔔(3)  👤 │  ← Header
├───────────────────────────────────────────────────────────────┤
│  KPI cards:  Total candidates │ In progress │ Hired │ Rejected │
├──────────────┬────────────────────────────────────────────────┤
│ Jobs list    │  Candidates table for selected job             │
│ (filter)     │  Name │ Job │ Applied │ CV │ Status │ Actions   │
│              │                                                │
├──────────────┴────────────────────────────────────────────────┤
│  Chart: candidates per job, stacked by status                 │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. Features

### 3.1 Candidates by Job (requirement 1)

**Jobs panel** — list of open positions, each with candidate count and a mini status bar (red / yellow / green segments).

Example jobs for a medical-device company:

| Job ID | Job title | Department | Location | Open since |
|---|---|---|---|---|
| J-101 | R&D Biomedical Engineer | R&D | Tel Aviv | 2026-09-01 |
| J-102 | Quality Assurance Engineer (ISO 13485) | QA/RA | Haifa | 2026-09-15 |
| J-103 | Regulatory Affairs Specialist (FDA / MDR) | QA/RA | Remote | 2026-10-01 |
| J-104 | Clinical Application Specialist | Clinical | Jerusalem | 2026-10-05 |
| J-105 | Embedded Software Engineer | R&D | Tel Aviv | 2026-10-12 |
| J-106 | Production Technician (Clean Room) | Operations | Haifa | 2026-10-20 |

**Candidates table** — shows candidates of the selected job (or "All jobs").

| Column | Description |
|---|---|
| Name | Full name + avatar initials |
| Job | Job title (shown when "All jobs" is selected) |
| Applied | Date the CV was received |
| Source | LinkedIn / Company site / Referral / Agency |
| Experience | Years of experience |
| CV | File icon + file name (see 3.2) |
| Status | Colored badge (see 3.3) |
| Recruiter | Assigned recruiter |
| Actions | View · Change status · Add note |

- Sort by any column; default sort = newest first.
- Filters: job, status, source, date range, free-text search (name, email, skills).
- **Chart:** horizontal stacked bar — one bar per job, segments colored by status. Clicking a bar filters the table to that job.
- **KPI cards** at top: Total candidates, In progress, Hired, Rejected, New this week.

### 3.2 CV Files (requirement 2)

- Each candidate has one or more CV files (PDF, DOCX).
- CV column shows a file icon (PDF red, DOCX blue), file name and size.
- Click → **CV viewer side panel** (full screen on mobile) with:
  - In-browser preview of the PDF.
  - Download button.
  - Candidate details: email, phone, ID number (ת.ז), job, status, notes history.
- Upload: drag & drop or "Upload CV" button; allowed types `.pdf`, `.doc`, `.docx`, max 10 MB. The upload form asks for full name, email, **phone** and **ID number** (all required) and runs the duplicate check in §3.6 before adding the candidate.
- Files stored in secure storage; access only for logged-in HR users (candidate data is personal — see §6).

### 3.3 Candidate Status Colors (requirement 3)

| Status | Color | Badge | Meaning |
|---|---|---|---|
| **Rejected** | 🔴 Red `#E53935` | `✕ Rejected` | Candidate was not accepted |
| **In progress** | 🟡 Yellow `#FFE11A` | `⏳ In progress` | Screening, interview, tests or offer stage |
| **Hired** | 🟢 Green `#43A047` | `✓ Hired` | Candidate accepted the offer |

- "In progress" can show a sub-stage as small text: *Screening → Phone interview → Technical interview → Offer*.
- Table rows and mobile cards stay **white** — color is used only on the status badge (and in the chart / job mini-bars).
- Changing status: dropdown in the row or in the CV panel; change is saved with date and user in the history.

### 3.4 New CV Notification Bell (requirement 4)

- 🔔 bell icon in the header, right side.
- **Red counter badge** with the number of unread new CVs (shows `9+` above 9).
- When a new CV arrives:
  - Badge number goes up.
  - Bell does a short shake animation (disabled when the user prefers reduced motion).
  - Optional toast at bottom: *"New CV: Dana Levi — QA Engineer"*.
- Click the bell → dropdown list of latest new CVs: candidate name, job, time ("5 min ago"), unread dot.
  - Click an item → opens that candidate's CV panel and marks it read.
  - "Mark all as read" link at the bottom.
- New candidates also show a blue **"NEW"** tag in the table until opened.
- Update method: polling every 60 s (MVP) → WebSocket / push later.

### 3.5 Mobile Friendly (requirement 5)

| Breakpoint | Layout |
|---|---|
| ≥ 1024 px (desktop) | Header + KPI row + side jobs panel + table + chart |
| 600–1023 px (tablet) | Jobs panel becomes a dropdown above the table; KPI cards in 2×2 grid |
| < 600 px (mobile) | Logo symbol only; KPI cards scroll horizontally; **table becomes cards** (one card per candidate: name, job, status badge, CV button); CV panel opens full screen; filters in a bottom sheet |

- Touch targets at least **56 × 56 px** and big friendly icons (see §1.3–1.4).
- No horizontal page scrolling; 16 px side margins.
- Bell stays visible in the sticky header on all sizes.

### 3.6 Duplicate Prevention (requirement 6)

The same person must exist **only once**. Two submissions are the same person when they have the **same ID number (ת.ז) OR the same phone number**.

**Normalization before comparing**
- ID number: digits only, padded with leading zeros to 9 digits (`12345678-2` = `123456782`; `5678920` → `005678920`). Must pass the Israeli ID check digit.
- Phone: digits only; a leading `972` becomes `0` (`+972-50-555-1234` = `050-5551234` = `0505551234`). Valid form: `0` + 8–9 digits.

**Layer 1 — block on entry (upload form)**
- Validation messages: missing / wrong length ID → *"Please enter a 9-digit ID number."*; wrong check digit → *"This ID number is not valid — the check digit does not match."*; bad phone → *"Please enter a valid phone number, for example 050-1234567."*
- If the ID or phone already exists, **no new candidate is created**. The dialog shows a message box: *"This candidate is already in the system — {name} already exists with {the same ID number / the same phone number / both}. Applied for {job} on {date}."* The box is announced to screen readers (`role="alert"`) and focus moves to its first button.
- Two buttons (each at least 56 px tall, §1.4):
  - **Add this CV to the existing candidate** — the new file becomes the candidate's current CV, the history gets *"New CV received (duplicate blocked) — {job}"*, the candidate gets the NEW tag and the bell rings.
  - **Open existing candidate** — closes the dialog and opens that candidate's CV panel.
- Editing the ID or phone field hides the message (it may no longer apply).

**Layer 2 — safety net in the data store (Airtable base *HR Recruiting – Micro Medical Devices*, table `CVs`)**
- Formula fields `ID key` and `Phone key` hold the normalized values above.
- Automation *"Flag duplicate CVs (same ID or phone)"*: when a record has both ID and phone filled, it finds other records with the same `ID key` or `Phone key` and links them in `Same ID as` / `Same phone as`. The formula field `Duplicate check` then shows **⚠️ Duplicate** (otherwise ✓ Unique). The original record shows the newer submission in `Later CVs with same ID / phone`.
- The automation **never deletes** — a recruiter decides whether to merge (for example, when the ID was typed wrong).
- Real system: the database has a **unique constraint** on the normalized ID number and on the normalized phone, so a duplicate cannot be saved at all (§4).
- When the dashboard is connected to Airtable (§3.7), Layer 1 checks against the Airtable rows. "Add this CV to the existing candidate" then also updates the existing Airtable record: `Submissions` + 1, a line in `Duplicate notes`, `CV file` = the new file name, and the file is attached to `CV`. No second record is created.

### 3.7 Airtable Connection (requirement 7)

- An **Airtable** button in the header (database icon, 56 × 56 px) opens the *Connect to Airtable* dialog. A small dot on the button is green when connected, grey when not.
- The dialog asks for a **personal access token** and the **Base ID** (pre-filled with the HR Recruiting base, `app…`, 17 characters) and explains how to create the token: scopes `data.records:read` and `data.records:write`, access to the base *HR Recruiting – Micro Medical Devices* only.
- The token is saved **only in that browser** (`localStorage`) and is never written into the site's code. "Disconnect" removes it and goes back to the demo data.
- When connected, the dashboard shows the rows of the `CVs` table instead of the demo data, and the line under the title says *"Live data from Airtable · {n} candidates · updated {time}"*. It reloads the table every **30 s**; new rows ring the bell.
- Field mapping (Airtable → dashboard): `Full name`, `Email`, `Phone`, `ID number (ת.ז)`, `Job` (must match a job title), `Applied`, `Source`, `Experience (years)`, `Status`, `Stage` (Screening / Phone interview / Technical interview / Offer), `Recruiter`, `CV` (first attachment; preview for PDF), `Notes`. Rows with no name or an unknown job are skipped and counted in a message.
- Saved back to Airtable: status and stage, notes (each note starts with `[YYYY-MM-DD HH:MM]`), new candidates from the upload form (all fields above plus `Job type`, `CV file`, `Submissions` = 1, and the CV file up to 5 MB), and blocked duplicates (§3.6). If a save fails, the change is undone on screen and a message explains why.
- Error messages: wrong token, no access to the base, no `CVs` table, no internet — each in plain language (English and Hebrew).

---

## 4. Data Model

```json
{
  "job": {
    "id": "J-102",
    "title": "Quality Assurance Engineer (ISO 13485)",
    "department": "QA/RA",
    "location": "Haifa",
    "openSince": "2026-09-15",
    "status": "open"
  },
  "candidate": {
    "id": "C-0457",
    "fullName": "Dana Levi",
    "email": "dana.levi@example.com",
    "phone": "+972-50-000-0000",
    "idNumber": "123456782",
    "jobId": "J-102",
    "appliedAt": "2026-11-04T09:32:00Z",
    "source": "LinkedIn",
    "yearsExperience": 5,
    "status": "in_progress",
    "stage": "technical_interview",
    "recruiter": "Merav",
    "isNew": true,
    "cvFiles": [
      { "id": "F-881", "name": "Dana_Levi_CV.pdf", "type": "pdf", "sizeKb": 412, "uploadedAt": "2026-11-04T09:32:00Z" }
    ],
    "history": [
      { "at": "2026-11-04T09:32:00Z", "by": "system", "change": "CV received" }
    ]
  }
}
```

`status` values: `rejected` | `in_progress` | `hired`

`idNumber` (9 digits, valid check digit) and the normalized `phone` are each **unique** — one candidate per person (§3.6). A person who applies for another job gets a new application linked to the same candidate, not a second candidate.

---

## 5. Main API (suggested)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs` | List jobs with counts per status |
| GET | `/api/candidates?jobId=&status=&q=` | List / filter candidates |
| GET | `/api/candidates/{id}` | Candidate details + history |
| PATCH | `/api/candidates/{id}/status` | Change status / stage |
| POST | `/api/candidates/{id}/cv` | Upload CV file |
| GET | `/api/cv/{fileId}` | Download / preview CV |
| GET | `/api/notifications?unread=true` | New CV notifications for the bell |
| POST | `/api/notifications/read` | Mark notifications as read |

---

## 6. Security & Privacy

- Login required (company SSO); roles: HR Admin, Recruiter, Hiring Manager (view only for own jobs).
- CVs contain personal data → encrypted storage, HTTPS only, access log for every CV view/download.
- The ID number (ת.ז) is sensitive personal data: shown only to logged-in HR users, never put in URLs or notifications, and used for duplicate checks (§3.6).
- Data retention: rejected candidates' CVs deleted after a defined period (per company policy / GDPR / local privacy law).

---

## 7. Accessibility

Target: **WCAG 2.2 level AA**, and Israeli Standard **IS 5568** (based on WCAG), so the dashboard can be used by recruiters with vision, motor, hearing or cognitive disabilities.

### 7.1 Vision & Color

- Text contrast at least **4.5 : 1** on the white background (large text 3 : 1); icons and borders at least **3 : 1**.
- Status is always shown with **color + text + icon** — never color alone (color-blind safe).
- **Yellow badge rule:** yellow `#FFE11A` on white is too light for text. The "In progress" badge uses a yellow fill with **dark text `#332B00`** and a darker yellow border `#D4B800`. Red and green badges use white text on the solid color only if contrast passes; otherwise dark text on a light tint.
- Zoom to **200%** and text spacing changes without losing content or needing horizontal scroll.
- Respects the browser/OS font size — sizes set in `rem`, not fixed `px`.
- Visible **focus ring**: 3 px brand-blue outline with 2 px white offset on every focusable element.

### 7.2 Keyboard

- Everything works **without a mouse**: Tab / Shift+Tab to move, Enter / Space to activate, Esc to close panels and dropdowns, arrow keys inside lists, tables and menus.
- "**Skip to main content**" link as the first item on the page.
- Logical tab order: header → KPI cards → jobs list → candidates table → chart.
- When the CV panel or bell dropdown opens, focus moves into it; when it closes, focus returns to the button that opened it. Focus is trapped inside the full-screen CV panel on mobile.
- Keyboard shortcuts (optional, can be turned off): `/` search, `N` open notifications.

### 7.3 Screen Readers

- Semantic HTML: `<header>`, `<nav>`, `<main>`, real `<table>` with `<th scope>` headers, `<button>` for actions (not clickable `<div>`s).
- Every icon button has an accessible name, e.g. `aria-label="View CV of Dana Levi"`; decorative icons have `aria-hidden="true"`.
- Bell: `aria-label="Notifications, 3 new CVs"`; new-CV arrivals announced politely through an `aria-live="polite"` region ("New CV received: Dana Levi, QA Engineer").
- Status badges read as text ("Status: In progress, technical interview").
- Sortable columns use `aria-sort`; the chart has a text summary and a "View as table" option.
- CV preview: PDF opens with a download link as an alternative; candidate details are plain text, not inside the image of the PDF.
- Logo has `alt="Micro Medical Devices"`.

### 7.4 Motor & Touch

- Touch targets at least **56 × 56 px**, 12 px apart (see §1.4).
- No action needs drag-and-drop only — CV upload also has an "Upload CV" button; status change uses a dropdown.
- No time limits on actions; toasts stay until dismissed or at least 8 s, with a close button.
- Works in both portrait and landscape.

### 7.5 Motion, Sound & Cognitive

- Bell shake and other animations are turned off when the user has **"reduce motion"** set (`prefers-reduced-motion`).
- Nothing flashes more than 3 times per second.
- No sound alerts by default; if added later, they are optional and paired with a visual signal.
- Plain, short wording ("Rejected", "Hired", "View CV"); same icons and labels everywhere.
- Error messages say what went wrong and how to fix it ("File too large — max 10 MB").
- Confirm before destructive actions (e.g. changing a hired candidate to rejected).

### 7.6 Language & Direction

- Page `lang` set correctly (`en` / `he`).
- Supports **Hebrew right-to-left (RTL)** layout: `dir="rtl"` mirrors the layout, the bell and icons move sides, and the data table reads right to left.

### 7.7 Accessibility Statement & Testing

- An **Accessibility Statement** page linked in the footer, with a contact for accessibility issues (required in Israel).
- Testing before release: automated checks (axe / Lighthouse score ≥ 95), keyboard-only walkthrough, screen-reader test with **NVDA** (Windows) and **VoiceOver** (iPhone), 200% zoom test, color-blindness simulation.

---

## 8. Acceptance Criteria

1. Selecting a job shows only that job's candidates; counts match the KPI cards and chart.
2. Every candidate row has a working CV link that previews and downloads the file.
3. Rejected = red, In progress = yellow, Hired = green — in status badges, chart and job mini-bars only; table rows and mobile cards stay white (no row tint), as in §3.3.
4. A newly added CV increases the bell counter within 60 s and appears in the bell dropdown.
5. At 375 px width the dashboard has no horizontal scroll and candidates show as cards.
6. The header shows the caduceus logo in bright glowing blue on a white background.
7. The page background is white on all devices.
8. Every button and icon button — including the "View" and close (✕) buttons in toasts, dialogs and the CV panel — is at least 56 × 56 px; status dropdowns and filter chips are at least 48 px tall (§1.4); icons follow the sizes in §1.3.
9. The full flow (find a candidate, open the CV, change status, read new-CV alerts) works with keyboard only and with a screen reader (NVDA, VoiceOver).
10. Automated accessibility check (axe / Lighthouse) shows no critical issues and score ≥ 95; all text passes 4.5 : 1 contrast.
11. Uploading a CV with an ID number or phone that already exists (in any format, e.g. `+972 50…` vs `050-…`) creates **no** new candidate; the duplicate message names the existing candidate and offers "Add this CV to the existing candidate" and "Open existing candidate" (§3.6). An ID with a wrong check digit or a phone that is not `0` + 8–9 digits is rejected with the messages in §3.6.
12. In the Airtable `CVs` table, a new record whose normalized ID or phone matches an existing record shows **⚠️ Duplicate** in `Duplicate check` and links to the existing record; no record is deleted automatically.
13. After connecting with a valid token, the dashboard shows the `CVs` rows (same count as in Airtable), the green dot is on, and a status change, a note, a new candidate and a blocked duplicate are all saved in Airtable as in §3.6–3.7. The token never appears in the page's source code.
