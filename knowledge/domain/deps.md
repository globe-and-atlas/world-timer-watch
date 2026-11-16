---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-11-06T11:30:00-06:00"
---
# Native dependencies
- @rebble/clay 1.1.0 pinned in watchface/package.json and lockfile. Tests execute the installed Clay bundle, including Save/Cancel/persistence serialization.
- Pebble SDK 4.33.1 / pebble-tool 5.0.40 provide Emery compilation. SDK/tool update notices were not acted on.
- Pillow provides only screenshot normalization and contact sheets; no runtime watch dependency.

## Round native QA — 2026-11-06
Pillow12.3.0 is pinned for deterministic screenshot decoding, palette normalization, and contact sheets. This is development tooling only; Pebble runtime dependencies are unchanged. It provides `Image.get_flattened_data()` used by the capture audit. No SDK upgrade was installed.

## 2026-11-06 — Round SDK targets
Installed SDK4.33.1/tool5.0.40 built Emery, Chalk, and Gabbro without an SDK upgrade. Clay1.1.0 recognizes both round platforms. Pillow12.3.0 is native QA tooling only.

## 2026-11-07

IANA timezone data2026f added as generated source data, with source URL/SHA/license. System zic and Python3 zoneinfo compile/verify the official TZif data. No pip/npm dependency installed; existing Clay1.1.0 and Pebble SDK4.33.1 retained. Builds use checked-in/generated C and do not require runtime network. Oracle tests require the pinned .tmp TZif cache prepared with execution/generate_zones.py --fetch.
