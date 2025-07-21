import { test, expect } from '@playwright/test'

test('Feedback form sends message (mock)', async ({ page }) => {
  await page.route('**/api/v1/feedback', route => {
    route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({ id: 1, message: 'Great!', resolved: false })
    })
  })

  await page.goto('/feedback')
  await expect(page.getByText('Feedback')).toBeVisible()

  const textarea = page.locator('textarea')
  await textarea.fill('Great!')
  const sendBtn = page.getByRole('button', { name: /send/i })
  await sendBtn.click()

  await expect(page.getByText(/thank you/i)).toBeVisible()
})
