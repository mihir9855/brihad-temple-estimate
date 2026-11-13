---
name: app-testing
description: Testing and QA for the app — type checks, build checks, unit/component tests (Vitest + React Testing Library), end-to-end and visual tests (Playwright), accessibility checks (axe), responsive/dark-mode screenshots, and Android/Capacitor release checks. Use when the user asks to test, verify, QA, check for bugs, add tests, or before shipping a feature, APK or EXE build.
---

# App testing skill

Goal: prove a change works and didn't break anything, and report results honestly
(show failing output; never skip or delete a test to get green).

Project: Brihad Temple Estimate (see `docs/PLAN.md`). Adjust paths below to the app's folder once it exists.
Most important tests: **calculation rules** — every rule from Shilp Ratnakar and from the owner's
CAD must be checked against known values (book feet tables, the 25-gaj example, the owner's CAD
measurements), including inch round-up (any fraction → next whole inch) and CFT = L×W×H×Nang÷1728.

## 1. Always run (no installs needed)

```bash
npm ci          # only if node_modules is missing
npx tsc -b      # type errors
npm run build   # production build must pass
```

## 2. Test layers — add only when needed

Adding a test framework changes `package.json`, so **ask the user before installing** the first time.

| Layer | Tool | When |
|---|---|---|
| Logic (calculation rules, unit conversion, CFT) | **Vitest** | Every rule — this is the core of the app |
| Components | **Vitest + @testing-library/react + jsdom** | Forms, sheets, conditional rendering |
| Full user flows, screenshots | **Playwright** | Critical paths (new project, select part, export PDF/Excel) |
| Accessibility | **@axe-core/playwright** | Every main screen |

Setup when approved:
```bash
npm i -D vitest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom
npm i -D @playwright/test @axe-core/playwright
```
Add scripts: `"test": "vitest run"`, `"test:e2e": "playwright test --trace off"`.
In `vite.config.ts` add `test: { environment: "jsdom", setupFiles: "./src/test/setup.ts" }`
(setup file: `import "@testing-library/jest-dom/vitest";`).

In this cloud environment Chromium + Playwright are preinstalled: if the project pins
its own `@playwright/test`, launch with `executablePath: '/opt/pw-browsers/chromium'`.
Never run `playwright install`.

## 3. Writing good tests

**Unit (Vitest)** — test behaviour and edge cases: zero, negative, empty, very large, decimals, dates across month/year boundaries, invalid input.
```ts
import { describe, it, expect } from "vitest";
describe("pith (paddhati 1)", () => {
  it("15 ft prasad gives 39 inch", () => { expect(pithHeight(180)).toBe(39); });
});
```

**Component** — query like a user (`getByRole`, `getByLabelText`), not by class names.
```tsx
render(<GarbhagruhInput onChange={onChange} />);
await userEvent.type(screen.getByLabelText(/garbhagruh/i), "108");
expect(onChange).toHaveBeenCalledWith(108);
```

**E2E (Playwright)** — run against `vite preview` (build first) or `vite dev`.
```ts
test("new project shows mandovar", async ({ page }) => {
  await page.goto("/");
  // create project, enter garbhagruh, select Mandovar, assert thar table and CFT are shown
});
```
Mock time/storage for determinism; clear `localStorage` between tests.

**Accessibility**
```ts
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

## 4. Visual / responsive check (quick, no test framework needed)

Use the preinstalled Playwright from a scratch script to screenshot each main screen at
360×800, 768×1024 and 1280×800, with `colorScheme: 'light'` and `'dark'`, and with
`reducedMotion: 'reduce'`. Look for: horizontal scroll, overlapping/cut text,
low contrast, tiny tap targets, layout jump while loading, console errors
(`page.on('console')` / `page.on('pageerror')`). Use deviceScaleFactor 2 for screenshots shown to the user.

## 5. Manual QA checklist

- [ ] Every flow: happy path, cancel midway, invalid input, empty data, lots of data
- [ ] Data survives reload / app restart; old saved data still loads after the change (migration)
- [ ] Keyboard only, and with screen-reader labels on icon buttons
- [ ] Offline behaviour (mobile)
- [ ] Android: back button, safe areas, soft keyboard not hiding inputs, PDF/Excel save
- [ ] No console errors or warnings

## 6. Before a release

1. Steps in section 1 pass; all tests pass.
2. Bump `version` in `package.json` if the release should show a new version.
3. Push; check the GitHub Actions run (if any) and read its logs on failure.

## 7. Report

State exactly what ran and the result: commands, pass/fail counts, screenshots, and anything not tested and why.
