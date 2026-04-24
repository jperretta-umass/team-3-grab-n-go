import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: {
    baseURL: 'http://127.0.0.1',
    trace: 'on-first-retry',
  },
  webServer: [
    {
      command:
        'docker compose -f ../docker-compose.yml -f ../docker-compose.test.yml up --build backend test_db',
      url: 'http://127.0.0.1:8000/health',
      reuseExistingServer: true,
      timeout: 120_000,
    },
    {
      command:
        'cd ../frontend && npm ci && VITE_API_BASE=http://127.0.0.1:8000 npm run dev -- --host 0.0.0.0 --port 5173',
      url: 'http://127.0.0.1:5173',
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});