import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { name: 'My Delivery App' }),
  ).toBeVisible();
  await expect(page.getByText('Welcome to the Home Page!')).toBeVisible();
});
