# N.B. Arch Co.

Marketing site for N.B. Arch Co. (Custom Goods), a custom laser engraving shop. The domain it is written for is [nbarchcompany.com](https://nbarchcompany.com/). The site is a static Vite project: HTML, CSS, and a small amount of JavaScript. There is no database and no account system.

## Run it locally

```bash
npm install
npm run dev
```

The dev server is http://127.0.0.1:43123

To build the files a host will publish:

```bash
npm run build
npm run preview
```

The build output is the `dist` folder.

## Edit the copy

Almost all of the words on the site are in `index.html`. Section headings, service descriptions, the process steps, the FAQ, and the quote introduction live there.

Colors, type, and spacing are in `src/styles.css`, under `:root`. The page is a warm light theme: ivory background, blush and sage section bands, deepened rose-gold as the brand accent, and sage as the second accent. Headings use Fraunces. Body text and buttons use Nunito Sans. Change those imports at the top of the stylesheet if you want a different pairing. Keep text colors dark enough to read on the cream, blush, and sage backgrounds.

Do not add a phone number, email address, street address, price, review, or testimonial unless it is real. None of those are invented on the site today.

## Logos

| File | Use |
| --- | --- |
| `public/brand/logo-badge.svg` | Circular badge. Used large in the hero. |
| `public/brand/logo-wordmark.svg` | Horizontal wordmark. Used in the header and footer. |
| `public/brand/arch.svg` | Arch only, transparent. Small decorative mark. |
| `public/brand/logo-badge.png` | Badge on cream, for sharing. |
| `public/brand/logo-wordmark.png` | Wordmark on cream. |
| `public/brand/logo-set.png` | Badge and wordmark together on cream. |
| `public/favicon.svg` | Arch mark, used as the browser icon. |
| `public/og.png` | Image for link previews (Open Graph). |

The SVGs are outlined, so they stay sharp at any size. To regenerate them after a code change in `scripts/generate-logo.py`:

```bash
python3 scripts/generate-logo.py
```

That script needs [fontTools](https://github.com/fonttools/fonttools) (`pip install fonttools brotli`). It sets the lettering in Jost Light, which is under the SIL Open Font License, and converts the letters to paths. The mark is darkened rose-gold so it reads on the cream site. If you recolor it, export new PNGs for `public/og.png`, `public/favicon-32.png`, `public/apple-touch-icon.png`, and `public/icon-512.png` on the same cream background.

## Swap gallery photos

The gallery is line drawings on purpose, so the page does not pretend they are customer photographs. Each drawing says “Placeholder drawing.”

1. Add a photo to `public/gallery/`. JPEG or WebP, at least 1200 pixels on the long side, works well. The frame is portrait, 4:5, and the image is cropped to fill it (`object-fit: cover`).
2. In `index.html`, find that figure in the gallery section.
3. Change the `src` and write an `alt` that describes the real piece.
4. Remove the line `<span class="plate-note">Placeholder drawing</span>`, or replace it with a short factual caption (the material, not a customer’s name).

`scripts/generate-gallery.py` redraws the placeholder SVGs if you want to change those drawings.

## Wire up the quote form

Visitors can fill out the form today. **Nothing is sent, and nothing is stored,** until you set one value.

Open `public/config.js` and set `formEndpoint`:

```js
window.NBARCH_CONFIG = {
  formEndpoint: "",
};
```

Leave it as `""` and the submit button stays off. The page tells visitors that online quotes are coming soon.

### Formspree (recommended)

Formspree accepts the form, including the optional artwork file, and emails you.

1. Create a form at [formspree.io](https://formspree.io/).
2. Copy the endpoint. It looks like `https://formspree.io/f/xxxxxxxx`.
3. Set `formEndpoint` to that URL, in quotes.
4. In Formspree, choose the inbox that should receive requests. Confirm the plan you are on allows file uploads if you want artwork to come through.
5. Rebuild and redeploy.

The form posts `multipart/form-data` with these fields: `name`, `email`, `phone`, `product`, `quantity`, `description`, `artwork`, and `_subject`. Any service that accepts that kind of POST can be used in place of Formspree. Put its URL in the same `formEndpoint` value.

### An email address instead

Set `formEndpoint` to the inbox, for example `"you@example.com"`. Submitting opens the visitor’s email app with the request filled in. Browsers cannot attach the artwork file this way. The page says so, and asks them to attach it in the email before sending. The text of the request is not stored on the website.

If the value is not a `http`/`https` URL and not an email address, the form stays off.

## Deploy

The site is static. Connect the git repository, then use:

- Build command: `npm run build`
- Output directory: `dist`
- Node 20 or newer

No environment variables are required. `public/config.js` is copied into the build as-is, so a change to the form endpoint needs a new deploy.

### Vercel

1. Import the repository. Vercel detects Vite.
2. Confirm the build command is `npm run build` and the output is `dist`.
3. Deploy.
4. In Project → Settings → Domains, add `nbarchcompany.com` and `www.nbarchcompany.com`.
5. At the registrar, set the DNS records Vercel shows (usually an A record and a CNAME for `www`).

### Netlify

1. Add a new site from the repository.
2. Build command: `npm run build`. Publish directory: `dist`.
3. Deploy.
4. Domain management → add `nbarchcompany.com`.
5. At the registrar, use the Netlify DNS records or point the nameservers at Netlify.

`public/_headers` is copied to `dist` and Netlify will apply those headers.

### Cloudflare Pages

1. Create a Pages project and connect the repository.
2. Framework preset: Vite. Build command: `npm run build`. Build output directory: `dist`.
3. Deploy.
4. Custom domains → set up `nbarchcompany.com`.
5. If DNS is already on Cloudflare, Pages can add the record. If it is not, change the nameservers at the registrar to the ones Cloudflare gives you.

`public/_headers` works on Cloudflare Pages as well. `public/404.html` is used for unknown URLs on Netlify and Cloudflare Pages.

After the domain is connected, the canonical URL and Open Graph tags already point at `https://nbarchcompany.com/`.

## Secrets policy

This repository is public. Never commit a secret. That includes API keys, passwords, tokens, private codes, and any other credential.

The site does not need environment variables today. If one is required later, put it in the hosting provider’s environment variables (Vercel, Netlify, or Cloudflare Pages). Do not put it in git. Do not put it in `public/config.js` either: that file is copied into the published site, so anything in it is public. A form endpoint there is a destination for quote requests, not a password.

`.env` and `.env.*` are ignored. `.env.example` is the only env file that may be committed, and only with names or empty placeholders. Pushes and pull requests run a gitleaks scan (`.github/workflows/gitleaks.yml`).

## What the owner still needs to provide

The site is deliberately missing anything that was not confirmed:

- A destination for quote requests (`formEndpoint` in `public/config.js`)
- Photographs of real work, to replace the gallery drawings
- Any public contact details to display: phone, email, shop address, hours
- Prices, if they should appear on the site
- A specific turnaround time, if one should be promised
- Social profile links, if they should appear
- DNS access for `nbarchcompany.com`, pointed at the host
