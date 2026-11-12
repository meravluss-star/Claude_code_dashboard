# Working Practice — HR Recruiting Dashboard

Rules for everyone (people and Claude) working on this project.

## 1. Commit and push automatically

- After every change is done and tested, **commit and push it automatically** to GitHub — no need to wait for approval:
  `https://github.com/meravluss-star/Claude_code_dashboard`
- One commit per change, with a clear message that says what changed, for example:
  `Add new-CV notification bell`
- Every push to `main` updates the live dashboard on GitHub Pages:
  `https://meravluss-star.github.io/Claude_code_dashboard/`
  After pushing, check that the Pages build finished.
- Every `gh` CLI command used is shown to the user.

## 2. Keep the README up to date

- The project has a `README.md` that describes the dashboard and its features.
- Whenever a feature is added or changed, update the README's **description / features** section in the **same commit**.
- The README must always match what is in `spec.md` and in the dashboard itself.

## 3. Keep the spec consistent

- When any requirement in `spec.md` changes, **search the whole spec** for every place that mentions it — especially the **Acceptance Criteria (§8)** — and update them in the same change, so the spec never contradicts itself.
- Check the dashboard against the numbers in the spec (for example: every button at least 56 × 56 px, including small ones in pop-up messages and dialogs).
- Anything the demo does not do goes in **§0 Out of Scope**.

## Checklist for every change

1. Change the files (`index.html`, `spec.md`, etc.).
2. If the spec changed: re-check the Acceptance Criteria (§8) and Out of Scope (§0).
3. Test in the browser (desktop, tablet, phone).
4. Update `README.md` (description / features).
5. Commit with a clear message.
6. Push to GitHub (`main` branch) — automatically.
7. Check that the GitHub Pages build finished and the live site shows the change.
