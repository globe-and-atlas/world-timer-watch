---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T14:24:18-06:00"
---

# Build combined World Timer

Goal: the approved two-place travel instrument, native on Emery, Chalk, Gabbro. Amber default, Olive option, correct named-city time/DST/date, configured call windows on a common next24h timeline, double-knock schematic travel without hiding the clock.

Source layers: official pinned IANA data → execution/generate_zones.py → city_data.c/h and cities.json; pure C city/calendar/window/knock policy; native rendering and service wiring; Clay configuration. No runtime remote API is required. Do not infer named cities from old fixed offsets. Do not publish or push as part of this build request.

Prepare oracle cache with `python3 execution/generate_zones.py --fetch`. Build fixtures with `python3 execution/build.py --fixture`. Ensure the correct active watchface: install success is not proof of activation. Use Watchfaces menu to select World Timer if a prior face remains visible. Run capture_combined.py and check_combined.py sequentially per target. The shared emulator has one owner; never hard-kill QEMU.

Native capture verifies dimensions and theme identity; travel frame sequence must keep the clock region identical and return exactly to rest. Theme-aware palette normalization uses known maximum170 for Olive and255 for Amber/white custom, avoiding false yellow amplification. Compare selected source colors, not only maximum pixel brightness.

Finish with `python3 execution/build.py` and `python3 execution/verify.py`. Verification includes timezone oracle tests, explicit difficult DST cases, sanitizer calendar/knock sweep, actual Clay lifecycle, PBW identity/three binaries/current-build equality, nonfixture build marker, absence of fixture-only ELF symbols. Require fresh independent source/native review.

Acceptance remains the atomic checklist in task.md. Physical wrist readability, case-knock sensitivity, battery endurance, real companion configuration and voluntary sharing remain field tests; native emulator evidence must not be relabeled as those.
