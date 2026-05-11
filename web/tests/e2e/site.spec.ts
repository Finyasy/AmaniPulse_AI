import { expect, test } from "@playwright/test";

const routes = [
  { path: "/", heading: "AmaniPulse AI" },
  { path: "/site-map", heading: "The AmaniPulse AI frontend is organized around action." },
  { path: "/resources", heading: "Practical guidance for safer civic participation." },
  { path: "/dashboard", heading: "National risk overview" },
  { path: "/dashboard/map", heading: "County risk map" },
  { path: "/dashboard/incidents", heading: "Incident stream" },
  { path: "/dashboard/review", heading: "Review queue" },
  { path: "/dashboard/alerts", heading: "Alerts and interventions" },
  { path: "/report", heading: "Share an election peace signal without creating an account." },
];

test.describe("AmaniPulse web routes", () => {
  for (const route of routes) {
    test(`${route.path} renders expected heading`, async ({ page }) => {
      const response = await page.goto(route.path);

      expect(response?.ok()).toBeTruthy();
      await expect(page.getByRole("heading", { level: 1, name: route.heading })).toBeVisible();
      await expect(page.locator("main")).toHaveCount(1);

      const overflow = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      }));
      expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 1);
    });
  }
});

test("mobile navigation opens and routes to dashboard", async ({ page, isMobile }) => {
  test.skip(!isMobile, "Mobile menu is only visible in the mobile layout.");

  await page.goto("/");
  await page.getByRole("button", { name: "Menu" }).click();
  await expect(page.getByRole("navigation", { name: "Mobile navigation" })).toBeVisible();
  await page
    .getByRole("navigation", { name: "Mobile navigation" })
    .getByRole("link", { name: "Dashboard" })
    .click();

  await expect(page).toHaveURL(/\/dashboard$/);
  await expect(page.getByRole("heading", { level: 1, name: "National risk overview" })).toBeVisible();
});

test("anonymous report form produces a prototype receipt", async ({ page }) => {
  await page.goto("/report");

  await page.getByPlaceholder("Example: Nairobi").fill("Nairobi");
  await page.getByPlaceholder("Example: Mathare").fill("Mathare");
  await page.locator('select[name="category"]').selectOption("violence_threat");
  await page.locator('select[name="language"]').selectOption("sw");
  await page
    .getByPlaceholder("Share only what feels safe. Avoid names if they could expose you.")
    .fill("Demo report: crowd tension rising near a campaign meeting.");
  await page.locator('input[type="checkbox"]').check();
  await page.getByRole("button", { name: "Submit anonymous report" }).click();

  await expect(page.getByRole("status")).toContainText("Reference WEB-");
  await expect(page.getByText("Report captured for demo review")).toBeVisible();
});

test("review page exposes backend-shaped queue and audit events", async ({ page }) => {
  await page.goto("/dashboard/review");

  await expect(page.getByRole("heading", { name: "Reports needing partner context" })).toBeVisible();
  await expect(page.locator(".review-card")).toHaveCount(3);
  await expect(page.locator(".event-row")).toHaveCount(3);
  await expect(page.getByText("AP-2714", { exact: true })).toBeVisible();
});
