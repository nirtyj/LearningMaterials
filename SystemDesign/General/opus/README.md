# OPUS — A Staff Engineering Compendium

Static site for staff-level system design interview preparation. Build target: GitHub Pages.

## Structure

- `index.html` — landing page with hero, strategy, and chapter cards
- `01-event-aggregator.html` ... `16-backpressure-patterns.html` — chapter pages
- `assets/style.css`, `assets/app.js` — shared styles and interaction layer

## Hosting on GitHub Pages

1. Create a repository (any name, or `<username>.github.io` for the root domain).
2. Copy these files into the repo root.
3. Settings → Pages → Source: `main` branch, `/` (root).
4. Visit `https://<username>.github.io/<repo>/`.

That's it — no build step, no dependencies (Google Fonts loaded over the network).

## Keyboard shortcuts

- `G` or `T` — open contents drawer
- `J` — next chapter
- `K` — previous chapter
- `I` — return to index
- `Esc` — close drawer

## Notes

- ASCII diagrams use a monospace font with disabled ligatures (`JetBrains Mono`).
- Code blocks render dark on cream — like a printed book with type-set code.
- Right rail of each chapter has the **Tooling Universe** — every system, paper, and primitive named in that chapter, organised by role. Use these to find connections between adjacent topics.
- `Related Chapters` panel routes you to the closest deep-dives.

Type set in Fraunces and Newsreader (serif) and Instrument Sans (sans). Code in JetBrains Mono.
