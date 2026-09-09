# Arafath Tours — Kerala Backwaters

Responsive Kerala travel website with a looping video hero, animated cloud transition, GSAP/Lenis motion, village gallery, Kerala journal and WhatsApp enquiries.

## Preview locally

The website is ready to serve from `dist/` with no build step:

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000 in your browser.

## Edit the website

- `src/redesign.py`: shared page markup and page generator.
- `src/kerala-content.json`: tour, gallery, article and cab route content.
- `dist/design.css`: responsive layout and visual styling.
- `dist/design.js`: navigation, motion, video playback, gallery and enquiries.
- `dist/assets/`: local images, videos, fonts and animation libraries.
- `ASSET_SOURCES.json`: media source notes.

To regenerate the HTML after changing its source:

```sh
python3 -m pip install lxml
python3 src/redesign.py
```

Serve or deploy `dist/` as the website root. Existing routes use directory-based `index.html` files. The `.openai/hosting.json` file retains the existing Sites deployment identity.

`src/layouts/` and `src/upgrade.py` preserve earlier implementation snapshots; the current page generator is `src/redesign.py`.
