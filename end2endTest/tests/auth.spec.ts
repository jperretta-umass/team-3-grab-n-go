import { expect, test } from '@playwright/test';

function uniqueUser() {
  const suffix = Date.now();

  return {
    username: `playwright-user-${suffix}`,
    email: `playwright-${suffix}@example.com`,
    phone_num: '555-123-4567',
    password: 'password123',
  };
}

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => window.localStorage.clear());
});

test('User Registration', async ({ page }) => {
  const user = uniqueUser();

  await page.goto('/Register');

  await page.getByLabel('Username:').fill(user.username);
  await page.getByLabel('Email:').fill(user.email);
  await page.getByLabel('Phone Number:').fill(user.phone_num);
  await page.locator('#password').fill(user.password);
  await page.locator('#confirmPassword').fill(user.password);

  await page.getByRole('button', { name: 'Register Account' }).click();

  await expect(page).toHaveURL('/');
  await expect(page.getByText('Welcome to the Home Page!')).toBeVisible();

  const auth = await page.evaluate(() => {
    const raw = window.localStorage.getItem('auth');
    return raw ? JSON.parse(raw) : null;
  });

  expect(auth).toMatchObject({
    username: user.username,
    email: user.email,
    phone_num: user.phone_num,
    is_deliverer: false,
  });
  expect(auth?.id).toBeTruthy();
});

test('User Login', async ({ page, request }) => {
  const user = uniqueUser();

  const registerResponse = await request.post('http://127.0.0.1:8000/auth/register', {
    data: {
      username: user.username,
      email: user.email,
      phone_num: user.phone_num,
      is_deliverer: false,
      password: user.password,
    },
  });

  expect(registerResponse.ok()).toBeTruthy();

  await page.goto('/Login');

  await page.getByLabel('Email:').fill(user.email);
  await page.locator('#password').fill(user.password);

  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page).toHaveURL('/');
  await expect(page.getByText('Welcome to the Home Page!')).toBeVisible();

  const auth = await page.evaluate(() => {
    const raw = window.localStorage.getItem('auth');
    return raw ? JSON.parse(raw) : null;
  });

  expect(auth).toMatchObject({
    username: user.username,
    email: user.email,
    phone_num: user.phone_num,
    is_deliverer: false,
  });
  expect(auth?.id).toBeTruthy();
});
