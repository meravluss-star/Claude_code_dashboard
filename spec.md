# Micro Medical Devices — HR Recruiting Dashboard

**Spec version:** 1.0 · **Date:** 2026-11-05
**Owner:** HR / Talent Acquisition
**Purpose:** One screen where recruiters see every open job, the candidates for each job, their CV files and hiring status, with an alert when a new CV arrives. The dashboard works on desktop, tablet and mobile.

---

## 1. Branding & Logo

### 1.1 Logo
The logo keeps the look of the current company mark — a **caduceus** (winged staff with two serpents) above the wordmark **"MICRO MEDICAL DEVICES"** in small caps — but in a clearer, brighter, **glowing blue**.

| Element | Spec |
|---|---|
| Symbol | Caduceus: vertical staff, two spread wings at the top, two serpents twisting around the staff, small round knob on top |
| Main color | Bright medical blue `#1E90FF` (replaces the faded lavender‑blue of the old logo) |
| Highlight color | Light cyan `#7FD4FF` for inner edges / highlights |
| Glow | Outer soft glow: `filter: drop-shadow(0 0 6px #1E90FF) drop-shadow(0 0 14px rgba(30,144,255,.55))` |
| Wordmark | "MICRO MEDICAL DEVICES", serif small caps, color `#0B5ED7`, letter-spacing `0.08em` |
| Format | Inline SVG (sharp on every screen, can be recolored by CSS) |
| Sizes | Header: 40 px tall (mobile 32 px) · Login/splash: 160 px tall |
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
| `--status-progress` | `#FBC02D` (yellow) | Candidates in progress |
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
  - Candidate details: email, phone, job, status, notes history.
- Upload: drag & drop or "Upload CV" button; allowed types `.pdf`, `.doc`, `.docx`, max 10 MB.
- Files stored in secure storage; access only for logged-in HR users (candidate data is personal — see §6).

### 3.3 Candidate Status Colors (requirement 3)

| Status | Color | Badge | Meaning |
|---|---|---|---|
| **Rejected** | 🔴 Red `#E53935` | `✕ Rejected` | Candidate was not accepted |
| **In progress** | 🟡 Yellow `#FBC02D` | `⏳ In progress` | Screening, interview, tests or offer stage |
| **Hired** | 🟢 Green `#43A047` | `✓ Hired` | Candidate accepted the offer |

- "In progress" can show a sub-stage as small text: *Screening → Phone interview → Technical interview → Offer*.
- The whole table row gets a light tint of the status color (10% opacity) plus a 4 px colored left border.
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
- Data retention: rejected candidates' CVs deleted after a defined period (per company policy / GDPR / local privacy law).

---

## 7. Accessibility

Target: **WCAG 2.2 level AA**, and Israeli Standard **IS 5568** (based on WCAG), so the dashboard can be used by recruiters with vision, motor, hearing or cognitive disabilities.

### 7.1 Vision & Color

- Text contrast at least **4.5 : 1** on the white background (large text 3 : 1); icons and borders at least **3 : 1**.
- Status is always shown with **color + text + icon** — never color alone (color-blind safe).
- **Yellow badge rule:** yellow `#FBC02D` on white is too light for text. The "In progress" badge uses a yellow fill with **dark text `#3E2C00`** and a darker yellow border `#C79100`. Red and green badges use white text on the solid color only if contrast passes; otherwise dark text on a light tint.
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
3. Rejected = red, In progress = yellow, Hired = green — in badges, row tint, chart and job mini-bars.
4. A newly added CV increases the bell counter within 60 s and appears in the bell dropdown.
5. At 375 px width the dashboard has no horizontal scroll and candidates show as cards.
6. The header shows the caduceus logo in bright glowing blue on a white background.
7. The page background is white on all devices.
8. Every button and icon button is at least 56 × 56 px; icons follow the sizes in §1.3.
9. The full flow (find a candidate, open the CV, change status, read new-CV alerts) works with keyboard only and with a screen reader (NVDA, VoiceOver).
10. Automated accessibility check (axe / Lighthouse) shows no critical issues and score ≥ 95; all text passes 4.5 : 1 contrast.
