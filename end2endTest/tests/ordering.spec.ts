import { expect, type APIRequestContext, type Page, test } from '@playwright/test';

type TestUser = {
  username: string;
  email: string;
  phone_num: string;
  password: string;
};

type AuthSession = {
  access_token: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
};

type MenuItem = {
  id: number;
  name: string;
  price: number;
  category: string;
  dining_hall: string;
};

function uniqueUser(): TestUser {
  const suffix = `${Date.now()}-${Math.random().toString(16).slice(2)}`;

  return {
    username: `ordering-user-${suffix}`,
    email: `ordering-${suffix}@example.com`,
    phone_num: '555-987-1234',
    password: 'password123',
  };
}

async function registerUser(request: APIRequestContext): Promise<AuthSession> {
  const user = uniqueUser();
  const response = await request.post('http://127.0.0.1:8000/auth/register', {
    data: {
      username: user.username,
      email: user.email,
      phone_num: user.phone_num,
      is_deliverer: false,
      password: user.password,
    },
  });

  expect(response.ok()).toBeTruthy();
  return response.json() as Promise<AuthSession>;
}

async function signInWithToken(page: Page, token: string) {
  await page.goto('/');
  await page.evaluate((value) => window.localStorage.setItem('token', value), token);
}

async function getMenuItems(request: APIRequestContext): Promise<MenuItem[]> {
  const response = await request.get('http://127.0.0.1:8000/api/menu-items');
  expect(response.ok()).toBeTruthy();

  const data = await response.json();
  return data.menu_items as MenuItem[];
}

test('customer can choose items to put in cart and send it to checkout', async ({ page, request }) => {
  const session = await registerUser(request);
  const menuItems = await getMenuItems(request);
  const entree = menuItems.find(
    (item) => item.dining_hall === 'Hampshire' && item.category === 'entree',
  );
  const snack = menuItems.find(
    (item) => item.dining_hall === 'Hampshire' && item.category !== 'entree',
  );

  expect(entree).toBeTruthy();
  expect(snack).toBeTruthy();

  let checkoutPayload: unknown;
  await page.route('http://localhost:8000/api/payments/create-checkout-session', async (route) => {
    checkoutPayload = route.request().postDataJSON();
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ url: 'http://127.0.0.1/success' }),
    });
  });

  await page.goto('/');
  await page.evaluate(() => window.localStorage.clear());
  await signInWithToken(page, session.access_token);
  await page.goto('/CustomerLanding');

  await expect(page.getByRole('heading', { name: 'Customer Landing Page' })).toBeVisible();
  await page.locator('.hall-select').selectOption('Hampshire');
  await page.getByRole('button', { name: 'Start Order' }).click();

  await expect(page).toHaveURL('/ItemPage');
  await expect(page.getByRole('heading', { name: 'Grab & Go Menu' })).toBeVisible();

  await page
    .getByRole('listitem')
    .filter({ hasText: entree!.name })
    .getByRole('button', { name: 'Add' })
    .click();
  await page
    .getByRole('listitem')
    .filter({ hasText: snack!.name })
    .getByRole('button', { name: 'Add' })
    .click();

  const expectedTotal = (entree!.price + snack!.price).toFixed(2);
  await expect(page.getByRole('heading', { name: `Cart: $${expectedTotal}` })).toBeVisible();
  await expect(page.locator('.cart-panel')).toContainText(entree!.name);
  await expect(page.locator('.cart-panel')).toContainText(snack!.name);

  await page.getByRole('button', { name: 'Checkout' }).click();

  await expect(page).toHaveURL('/success');
  await expect(page.getByRole('heading', { name: 'Payment Successful!' })).toBeVisible();
  expect(checkoutPayload).toEqual({
    user_id: session.user.id,
    items: [
      { menu_item_id: entree!.id, quantity: 1 },
      { menu_item_id: snack!.id, quantity: 1 },
    ],
  });
});

test('placed orders appear in the customer order history API', async ({ request }) => {
  const session = await registerUser(request);
  const menuItems = await getMenuItems(request);
  const item = menuItems.find(
    (menuItem) => menuItem.dining_hall === 'Hampshire' && menuItem.name === 'Breakfast Burrito',
  ) ?? menuItems.find((menuItem) => menuItem.dining_hall === 'Hampshire');

  expect(item).toBeTruthy();

  const createResponse = await request.post(
    `http://127.0.0.1:8000/api/customers/${session.user.id}/orders`,
    {
      data: {
        dining_hall_id: 1,
        items: [
          {
            menu_item_id: item!.id,
            quantity: 2,
            special_instructions: 'Extra salsa',
            delivery_instructions: 'Meet by the pickup shelf',
          },
        ],
      },
    },
  );

  expect(createResponse.status()).toBe(201);
  const createdOrder = await createResponse.json();
  expect(createdOrder).toMatchObject({
    dining_hall: 'Hampshire',
    status: 'unclaimed',
    total_price: item!.price * 2,
    items: [
      {
        menu_item_id: item!.id,
        name: item!.name,
        price: item!.price,
        quantity: 2,
        special_instructions: 'Extra salsa',
        delivery_instructions: 'Meet by the pickup shelf',
      },
    ],
  });

  const ordersResponse = await request.get(
    `http://127.0.0.1:8000/api/customers/${session.user.id}/orders`,
  );
  expect(ordersResponse.ok()).toBeTruthy();

  const orders = await ordersResponse.json();
  expect(orders).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        id: createdOrder.id,
        dining_hall: 'Hampshire',
        status: 'unclaimed',
      }),
    ]),
  );
});
