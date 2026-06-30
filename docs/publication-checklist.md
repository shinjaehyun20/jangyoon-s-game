# Publication Checklist

Use this checklist before adding a new game or publishing a substantial update.

## Game folder

- [ ] Game folder exists at the repository root.
- [ ] Entry point exists, preferably `<game-id>/index.html`.
- [ ] The game can run through a static web server.
- [ ] The game has no dependency on private local files or absolute machine paths.
- [ ] Any assets needed by the game are committed under the game folder or another documented public path.

## Catalog metadata

- [ ] `games.json` includes `id`, `title`, `title_ko`, `description`, `thumbnail`, and `path`.
- [ ] `path` points to the playable entry file or to a deliberate external URL.
- [ ] `thumbnail` exists when it points to a local file.
- [ ] `menu.json` is updated if the game should appear in the menu/sidebar.
- [ ] `docs/games-catalog.md` is regenerated or updated after `games.json` changes.

## Browser and mobile checks

- [ ] Root landing page loads and shows the total game count.
- [ ] The game opens from the landing page.
- [ ] Desktop browser play path is checked.
- [ ] Mobile/touch viewport play path is checked for the main interaction.
- [ ] Keyboard focus or visible controls are available when the game expects them.

## Publication hygiene

- [ ] No private local path appears in Markdown/HTML/JS/CSS.
- [ ] No generated junk, temporary logs, or unrelated screenshots are committed.
- [ ] README or docs link to the game when it is a representative/highlighted addition.
- [ ] `CHANGES.md` or progress notes mention the update when it is user-visible.
