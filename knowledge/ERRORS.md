---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-11-06T11:30:00-06:00"
---
# Errors and remedies
## 2026-11-06 — Pebble GCC misleading indentation
The native SDK treats misleading indentation as an error. Guard service resubscription with braces before the unconditional redraw/time refresh. The corrected production builds pass.
## 2026-11-06 — Calendar-year rollover
A sign-only year difference can undercount a 26-hour local/secondary gap spanning two civil dates. Compare Gregorian day ordinals instead. Compiled host regressions cover +2 and −2 across year boundaries.

## 2026-11-07 — native city policy and capture

- Pebble SDK time.h in a standalone C file did not expose the expected structtm/gmtime types. Resolved by a portable pure C Gregorian converter, verified against pinned TZif data and sanitizer sweeps. Graduated to domain/city_timezones.md.
- Unconditionally scaling framebuffer maximum to255 changed OliveAAAA55 into yellow. The native capture now uses the theme-specific known maximum170 for Olive,255 for Amber/white custom. Graduated to directives/build_combined.md.
- Emery install retained LooseDigits; identity guard rejected captures. Explicit Watchfaces-menu selection of WorldTimer fixed activation. No wrong-app image was accepted as evidence.

- Final long-ISO capture inherited the prior expired test epoch. Fixed by explicitly resetting UTC in that case and recapturing, without changing app code. Graduated to procedural/verify_combined.md.

## 2026-11-07 — reinstall visual check sampled launch spinner
A fixed0.3s pause after native reinstall captured the Pebble loading spinner and falsely reported lost settings. The saved city/theme/date restored correctly after foreground initialization. Fix: bounded12s visual polling for the exact expected frame; fail only after settling timeout. Graduated to `execution/check_departure_persistence.py` and `directives/build_departure.md`.
