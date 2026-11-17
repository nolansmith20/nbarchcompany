# Agent notes

This repository is public. Never commit secrets.

## Secrets policy

Do not add API keys, passwords, tokens, private codes, credentials, or `.env` files that contain real values. That includes `public/config.js`, HTML, CSS, JavaScript, workflows, docs, and commit messages. `public/config.js` is published with the site, so it is not a place for a secret.

Secrets belong in the hosting provider's environment variables (Vercel, Netlify, or Cloudflare Pages). `.env.example` may list variable names or empty placeholders only. `.env` and `.env.*` are gitignored.

A gitleaks scan runs on pushes and pull requests (`.github/workflows/gitleaks.yml`). If a secret has already been committed, remove it and treat it as compromised. Do not open a pull request that adds one.
