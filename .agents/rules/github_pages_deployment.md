# Static Web Host & GitHub Pages Deployment Rule

- **Deployment Branch Synchronization**:
  When committing updates to repositories hosted via GitHub Pages, verify the deployment branch setup (`gh-pages` vs `master`) and push updates to both `master` and `origin/gh-pages`.
- **Cache-Busting Resource Links**:
  Always append or increment version query parameters (e.g., `styles.css?v=1.0.2`, `app.js?v=1.0.2`) on CSS and JS resource tags in `index.html` to prevent stale browser caching on static hosting CDNs.
