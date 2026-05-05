import { test, expect } from '@playwright/test';

test('root redirects to login', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveURL('/Login');
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
});
