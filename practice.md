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

## Checklist for every change

1. Change the files (`index.html`, `spec.md`, etc.).
2. Test in the browser (desktop, tablet, phone).
3. Update `README.md` (description / features).
4. Commit with a clear message.
5. Push to GitHub (`main` branch) — automatically.
6. Check that the GitHub Pages build finished and the live site shows the change.
