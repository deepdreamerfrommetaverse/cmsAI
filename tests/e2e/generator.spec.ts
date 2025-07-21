import { test, expect } from '@playwright/test'

test('AI Generator flow (mocked API)', async ({ page }) => {
  // intercept POST /api/v1/articles/ and return fake article
  await page.route('**/api/v1/articles', route => {
    route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        id: 123,
        title: 'Mock Article',
        slug: 'mock-article',
        body: 'Generated content',
        author_id: 1
      })
    })
  })

  await page.goto('/generator')
  await expect(page.getByText('AI Article Generator')).toBeVisible()

  const textarea = page.locator('textarea')
  await textarea.fill('My test prompt')
  await page.getByRole('button', { name: /generate/i }).click()

  await expect(page.getByText('Mock Article')).toBeVisible()
  await expect(page.getByText('Generated content')).toBeVisible()
})
