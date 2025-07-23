#!/usr/bin/env bash
# This script uses the OpenAPI spec to generate an SDK (for demonstration).
# Requires `openapi-python-client` or similar tool installed.
openapi-python-client generate --url http://localhost:8000/openapi.json --output frontend/src/api_sdk
