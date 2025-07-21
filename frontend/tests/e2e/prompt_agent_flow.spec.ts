import { test, expect } from '@playwright/test'

test('Prompt Agent end‑to‑end UI flow (stubbed backend)', async ({ page }) => {
  const fakeArticle = {
    id: 99,
    title: 'Stubbed Bricks Article',
    slug: 'stubbed-bricks-article',
    body: '<p>Lorem ipsum</p>',
    hero_url: 'https://picsum.photos/seed/ai/800/400',
    meta_title: 'Stubbed Bricks Article',
    meta_description: 'Lorem ipsum dolor sit amet, consectetur.',
    wp_post_id: 256,
    author_id: 1
  }

  await page.route('**/api/v1/prompt-agent/', route => {
    route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify(fakeArticle)
    })
  })

  await page.goto('/generator')
  await page.getByRole('textbox').fill('Write about AI in finance')
  await page.getByRole('button', { name: /generate/i }).click()

  await expect(page.getByText(fakeArticle.title)).toBeVisible()
  await expect(page.getByText(/WordPress ID/)).toContainText('256')
  await expect(page.locator('img')).toHaveAttribute('src', fakeArticle.hero_url)
})
