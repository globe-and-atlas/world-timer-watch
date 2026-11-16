---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-06T21:20:26-06:00"
---
# Publish a round-compatible watchface update

The user authorized15publications on2026-11-06 and explicitly excludedT9. Nine were existing listings; Dot Matrix, Railway, Classic LCD, World Timer, Triangle, and Lume were first publications.

Workspace execution scripts:
- `execution/prepare_round_store_assets.py` validates reviewed PBWs and stages native screenshots; new listings receive losslessly decoded six-palette GIFs.
- `execution/publish_watchface_updates.py` runs in the installed Pebble SDK's Python3 environment, uses SDK account authentication, and sends the SDK's multipart app/release fields. It uploads the exact reviewed PBW without rebuilding it.
- `execution/test_publish_watchface_updates.py` checks exclusion, duplicate-write guards, bounded retries, and redirect allowlists.

The run plan and checkpoints live under workspace `.tmp/round-watchfaces/store/`. Each project also retains its staged plan under `media/store/round-update/` and its public proof under `release/round-update/<version>/`. Never blindly repeat an upload after timeout; an inflight guard requires reconciliation first. Completed receipts skip duplicate POSTs. The historical round-only update used replaceScreenshots=false. A user-authorized redesign may replace obsolete galleries with replaceScreenshots=true after staging native replacement evidence. New listings are created only when the SDK account has no UUID mapping.

Public HTML contains the active watch gallery plus one cover image for each other platform. To check every round image, select each round watch in the public site's device selector and record its two screenshot URLs. The verifier combines this observed UI index with public platform covers, then downloads public images and PBW to compare exact pixels/bytes. Existing gallery URLs and bytes must remain intact. T9's separate baseline proves it was untouched.

Observed store constraint: Railway PNG upload processing merged rare colors and shifted one RGB channel. Re-encoding the same native pixels as single-frame GIFs preserves them exactly. Replace only the affected round stills in the listing editor, retaining the animated Emery GIF and release. Public GIF decode must match the original native PNG pixel-for-pixel. Native image content must not be changed to make a lossy upload pass.

A published response is not final proof: fetch the public listing/download, check exact version/PBW, inspect both selected-watch galleries, and preserve a public proof receipt. Cache convergence may lag the upload; do not upload a duplicate release to force refresh.

## 2026-11-07 combined redesign release

Use `execution/publish_store.py` with the Pebble SDK Python environment. Version-specific plan/receipt/proof live in `release/combined-update/0.2.0/`; prior round receipts remain historical. `prepare` fixes app identity and reviewed hash; `validate` checks media; `publish` sends one guarded existing-app release POST with replacement galleries. It never rebuilds. Six publishing guard tests exercise ambiguous writes, duplicate prevention and identity changes.

`execution/prepare_combined_store.py` converts verified native `.tmp/combined-native/{emery,chalk,gabbro}` captures into lossless travel-plus-color GIFs and three still GIFs per target. Preview color examples are separate settings, not automatic runtime cycling.

Release upload does not update the existing listing description. Save description separately using the dashboard Edit Listing form, reopen to confirm persistence, then check public propagation. Public selected-watch galleries can include a live-watch placeholder duplicating the lead image: deduplicate observed image URLs while preserving order. `verify` compares every frame, timing and PBW hash against the staged plan.

## 2026-11-07 departure0.3.0 publication

`execution/publish_departure.py` is separately pinned to the independently reviewed0.3.0 artifact/hash. Its receipts live in `release/departure-update/0.3.0/`, separate from0.2.0. Existing identity, UUID mapping, fixture-free marker and media hashes are validated before the guarded no-retry releasePOST. `execution/prepare_departure_store.py --check` validates12lossless native media assets and all three5second GIFs. Six dedicated write-guard tests pass.

Save description separately after release upload so old map/call-hours copy does not remain live. The store's cached platform gallery may lag even when fresh server-rendered public HTML and downloadable assets are current. Inspect the device selector for each target; do not create another release to refresh a stale gallery.
