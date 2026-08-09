# Browser Storage Safety Rule

- **Always Safe-Wrap Web Storage Access**:
  Never access `localStorage` or `sessionStorage` directly in root initializers or `DOMContentLoaded` callbacks without try-catch error handling.
- **Fallback Pattern**:
  Use safe helper functions (`safeGetStorage` / `safeSetStorage`) that gracefully return fallback values or ignore storage write errors when access is restricted by origin security policies.
