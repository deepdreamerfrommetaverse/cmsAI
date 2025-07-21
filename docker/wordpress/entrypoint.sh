#!/usr/bin/env bash
set -e

# Wait for MySQL
until mysqladmin ping -h"${WP_DB_HOST}" --silent; do
    echo "Waiting for MySQL..."
    sleep 3
done

cd /var/www/html

if [ ! -f wp-config.php ]; then
  echo "Installing WordPress..."
  wp core download --allow-root --skip-content
  wp core config --dbname="${WP_DB_NAME}" --dbuser="${WP_DB_USER}" --dbpass="${WP_DB_PASSWORD}" --dbhost="${WP_DB_HOST}" --allow-root
  wp core install --url="${WP_URL}" --title="${WP_TITLE}" --admin_user="${WP_JWT_USER}" --admin_password="${WP_JWT_PASSWORD}" --admin_email="${WP_ADMIN_EMAIL}" --skip-email --allow-root
fi

echo "Installing/activating plugins..."
# JWT Auth plugin
if ! wp plugin is-installed jwt-authentication-for-wp-rest-api --allow-root; then
  wp plugin install https://github.com/usefulteam/jwt-auth/archive/master.zip --activate --allow-root
fi

# Bricks Builder
if [ -n "${BRICKS_ZIP_URL}" ]; then
  echo "Installing Bricks from ${BRICKS_ZIP_URL}"
  curl -L "${BRICKS_ZIP_URL}" -o /tmp/bricks.zip
  wp plugin install /tmp/bricks.zip --activate --allow-root
  if [ -n "${BRICKS_LICENSE_KEY}" ]; then
    wp option update bricks_license_key "${BRICKS_LICENSE_KEY}" --allow-root
  fi
else
  echo "ERROR: BRICKS_ZIP_URL not set. Exiting."
  exit 1
fi

# Permalinks
wp rewrite structure "/%postname%/" --hard --allow-root

# Start Apache
apache2-foreground
