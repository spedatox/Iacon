# Parent application integration

The integrated applications remain the source of deployment and runtime state.
See `source-manifest.json` for the exact revisions represented here.

## Igor

- Construct `LibraryIndexer`, `LibraryService` and `LibraryControls` in the app
  lifespan and put them on `app.state`.
- Register `ListLibrarySkill`, `SearchLibrarySkill` and `ReadLibrarySkill` through
  the existing capability registry.
- Include `app.routers.library`; API-key middleware protects every route, and
  owner controls also validate `X-N8N-Secret`.
- Keep `library_index` and `library_embed` in the existing durable job queue.
  Source-scoped drains do not claim other owners' or unrelated jobs.
- Run additive migrations for `library_passages.position` and
  `library_index_generations.progress` before using these services.
- Persist owner settings through Igor's managed environment. The optional
  `LIBRARY_EMBEDDING_API_KEY` is separate from the shared provider key.

## Hisar

- Render `HallOfRecords` in its existing desktop window and load `iacon.css`.
- Keep the shared `api.js` owner-cookie transport in the parent application.
  It supplies `getLibrarySettings`, `saveLibrarySettings`, `getLibraryProgress`
  and the catalog/upload APIs imported by the components in this snapshot.
- Bootstrap the authoritative library store inside the existing confined vault.
- Create `LibraryDelivery` on app state and forward controls with server-held
  credentials. Secrets do not enter the frontend bundle.
- The desktop and dock use the original Optimus emblem. The dock places it in
  Hisar's existing `Tile` component so its size, highlight and alignment match
  adjacent applications. The header uses the same emblem at a larger size.
- English is the initial language; an explicit Turkish choice is retained in
  local storage.

The owner UI calls Hisar's `/library/settings`, `/library/progress` and
`/library/documents/{id}/retry` routes. Hisar forwards control requests to Igor's
authenticated `/library` routes. Original downloads and agent-authority resolution
continue through Hisar. No component has been detached or separately deployed.
