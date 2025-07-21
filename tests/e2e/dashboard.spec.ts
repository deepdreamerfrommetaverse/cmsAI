import { test, expect } from '@playwright/test'

test('dashboard loads', async ({ page }) => {
  await page.goto('http://localhost:5173')
  await expect(page.getByText('Dashboard')).toBeVisible()
})
