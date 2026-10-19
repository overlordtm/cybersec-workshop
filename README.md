# Cybersecurity workshops

Two reveal.js slide decks, built with Vite and published together to GitHub Pages.

## Local development

Use Node.js 24 (`nvm use` if you use nvm).

```sh
npm ci
npm run dev
```

Open the URL printed by Vite. The landing page links to both decks:

- `/cybersec-101/` — cybersecurity fundamentals
- `/cybersec-201/` — applied cybersecurity
- `/cybersec-201/vaje/` — participant exercise instructions in Slovenian

## Editing slides

Edit `cybersec-101/slides.md` or `cybersec-201/slides.md`.

- A line containing `---` starts a new horizontal slide.
- A line containing `--` starts a vertical slide.
- `Note:` starts speaker notes for the current slide.
- Fenced code blocks have syntax highlighting.
- Press **S** to open speaker notes, **Esc** for the slide overview, and arrow keys to navigate.

Shared configuration lives in `shared/reveal.js`, and shared styling in `shared/slides.css`.
For images, put them in the deck directory and reference them from its `index.html`
or import them in `main.js` so Vite includes them in the build. Images referenced
only inside raw Markdown are not processed by Vite: put those in
`public/cybersec-101/` or `public/cybersec-201/` and use a relative path such as
`![Description](./diagram.png)` in that deck's Markdown.

## Exercise pages

`cybersec-101/vaje/VAJE.md` holds the participant instructions (no instructor
solutions — those stay in `cybersec-101/EXERCISES.md`, which is not published).
The `handout` Vite plugin (`shared/handout.js`) renders it into
`cybersec-101/vaje/index.html` at build time and adds a QR code for every
external link in each `##` section. When `SITE_URL` is set (the Pages workflow
sets it), the page also shows a QR code of its own published URL.

Cybersec-201 has fifteen exercises. Within an exercise, use `### Namig` followed
by `### Postopek` to keep the hint and solution separate from the task. The
renderer creates nested native disclosure buttons: the hint appears first,
then its button for the procedure. Links and QR codes stay inside their
respective disclosure. Exercises without these headings render as before.

## Production build

```sh
npm run build
npm run preview
```

The output in `dist/` contains the landing page and both slide decks. Relative
asset URLs support repository Pages URLs as well as custom domains.

## GitHub Pages

1. Push this project to a GitHub repository with a `main` branch.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Push to `main`, or run **Build and deploy slides** from the Actions tab on `main`.

The workflow installs locked dependencies with `npm ci`, builds both decks, and
deploys `dist/` using GitHub's Pages actions. Pull requests targeting `main` run
the build without deploying. No personal access token is required.

Published routes:

```text
https://<owner>.github.io/<repository>/
https://<owner>.github.io/<repository>/cybersec-101/
https://<owner>.github.io/<repository>/cybersec-101/vaje/
https://<owner>.github.io/<repository>/cybersec-201/
https://<owner>.github.io/<repository>/cybersec-201/vaje/
```

If your default branch differs, update the branch filters and deployment
conditions in `.github/workflows/pages.yml`.
