#!/bin/bash

# Create full AI CMS directory structure with placeholder files

set -e

create_file() {
  mkdir -p "$(dirname "$1")"
  touch "$1"
}

# Frontend
create_file frontend/package.json
create_file frontend/tailwind.config.js
create_file frontend/vite.config.ts
create_file frontend/public/index.html
create_file frontend/src/index.css
create_file frontend/src/main.tsx
create_file frontend/src/App.tsx
create_file frontend/src/context/AuthContext.tsx
create_file frontend/src/context/ThemeConfigContext.tsx
create_file frontend/src/hooks/useAgent.tsx
create_file frontend/src/hooks/useBricks.tsx
create_file frontend/src/hooks/useFeedback.tsx
create_file frontend/src/hooks/useGallery.tsx
create_file frontend/src/hooks/useGenerator.tsx
create_file frontend/src/hooks/useHistory.tsx
create_file frontend/src/hooks/useSocial.tsx
create_file frontend/src/hooks/useStripe.tsx
create_file frontend/src/components/BrickBlock.tsx
create_file frontend/src/components/BricksPages.tsx
create_file frontend/src/components/ConflictModal.tsx
create_file frontend/src/components/DailySocialLimits.tsx
create_file frontend/src/components/PdfExportButton.tsx
create_file frontend/src/components/Sidebar.tsx
create_file frontend/src/components/StatsCtrBar.tsx
create_file frontend/src/components/StatsPromLink.tsx
create_file frontend/src/components/StatsSourcesPie.tsx
create_file frontend/src/components/ui/button.tsx
create_file frontend/src/components/ui/dialog.tsx
create_file frontend/src/pages/Feedback.tsx
create_file frontend/src/pages/Gallery.tsx
create_file frontend/src/pages/Generator.tsx
create_file frontend/src/pages/History.tsx
create_file frontend/src/pages/PromptAgent.tsx
create_file frontend/src/pages/Settings.tsx
create_file frontend/src/pages/Stats.tsx
create_file frontend/src/locales/en.json
create_file frontend/src/locales/pl.json
create_file frontend/src/i18n.ts
create_file frontend/Dockerfile
create_file frontend/nginx.conf

# Backend
create_file backend/Dockerfile
create_file backend/alembic/env.py
create_file backend/alembic/versions/763e3f8d7028_initial.py
create_file backend/alembic.ini
create_file backend/core/__init__.py
create_file backend/core/auth.py
create_file backend/core/openai_client.py
create_file backend/core/settings.py
create_file backend/database.py
create_file backend/main.py
create_file backend/models/__init__.py
create_file backend/models/analytics.py
create_file backend/models/article.py
create_file backend/models/feedback.py
create_file backend/models/user.py
create_file backend/models/version.py
create_file backend/routers/__init__.py
create_file backend/routers/analytics.py
create_file backend/routers/articles.py
create_file backend/routers/auth.py
create_file backend/routers/feedback.py
create_file backend/routers/stripe.py
create_file backend/routers/users.py
create_file backend/schemas/__init__.py
create_file backend/schemas/analytics.py
create_file backend/schemas/article.py
create_file backend/schemas/auth.py
create_file backend/schemas/feedback.py
create_file backend/schemas/user.py
create_file backend/services/__init__.py
create_file backend/services/analytics_service.py
create_file backend/services/article_service.py
create_file backend/services/auth_service.py
create_file backend/services/feedback_service.py
create_file backend/services/social_service.py
create_file backend/services/stripe_service.py
create_file backend/services/wordpress_service.py
create_file backend/scheduler.py
create_file backend/social/__init__.py

# Electron
create_file electron/main.js
create_file electron/preload.js
create_file electron/updater.js

# Scripts
create_file scripts/generate-sdk.sh

# Tests
create_file tests/e2e/generator.spec.ts
create_file tests/e2e/login.spec.ts
create_file tests/a11y/drag_drop.test.ts
create_file tests/backend/security/test_rate_limit.py

# GitHub workflows
create_file .github/dependabot.yml
create_file .github/workflows/ci.yml
create_file .github/workflows/security-scan.yml
create_file .github/workflows/electron-release.yml
create_file .github/workflows/docker-publish.yml
create_file .github/workflows/k6-load.yml

# Docs
create_file docs/README_notarize.md
create_file docs/a11y_report.md
create_file docs/deploy_guide.md
create_file docs/docs_observability.md

# Project root files
create_file docker-compose.yml
create_file docker-compose.logging.yml
create_file docker-compose.observ.yml
create_file docker-compose.traefik.yml
create_file lighthouse-axe.sh
create_file playwright.config.ts
create_file k6/load_test.js
create_file .env.example
create_file README.md

echo "✅ Project structure created successfully."
