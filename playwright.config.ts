import { PlaywrightTestConfig } from '@playwright/test'
const config: PlaywrightTestConfig = {
  webServer: {
    command: 'npm run dev',
    port: 5173,
    timeout: 120 * 1000,
    reuseExistingServer: true
  },
  testDir: 'tests/e2e'
}
export default config
