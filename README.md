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

## Explore Kerala 3D atlas

Open `/location/` for the Three.js landscape with 26 destination pins, a scenic route, orbit and zoom controls, top view, category/search filters and destination-specific WhatsApp enquiries.

- `src/explore.py` owns destination content and the accessible page markup. Run `python3 src/redesign.py` after edits; this refreshes `dist/assets/atlas/destinations.json` too.
- `dist/explore.js` owns the Three.js scene and progressive enhancement. Three.js r160 is vendored in `dist/assets/vendor/three.module.js`; no map API key or CDN runtime is needed.
- `dist/explore.css` is scoped to the atlas.
- `dist/assets/atlas/kerala-terrain.json` contains the simplified DataMeet / geohacker boundary and a geographic triangulated mesh. The renderer adds artistic, exaggerated elevation rather than measured terrain heights. Scenic flight paths are not road directions.
- Mobile keeps vertical page scrolling and uses horizontal swipes to orbit. Keyboard users can focus the map and use arrows, +/−, and Home, or use the destination buttons. Reduced motion starts with animations paused. Rendering stops offscreen and in background tabs. The destination directory remains present if JavaScript or WebGL is unavailable.

Map attribution: [Kerala boundaries by DataMeet / geohacker](https://github.com/geohacker/kerala), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), simplified and triangulated. Destination information: [Kerala Tourism](https://www.keralatourism.org/destination/).
