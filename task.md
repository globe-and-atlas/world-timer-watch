---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-11-06T11:00:00-06:00"
---
# Native watchface implementation
## Contract
Source: watchface/. Execution: execution/build.py, execution/verify.py, execution/capture_native.py. Output: dist/*.pbw. Never read .env. No publishing. Native emulator belongs to parent agent.
## Validation
- [x] Emery production PBW builds.
- [x] Six preset palettes are selectable.
- [x] Custom background is selectable.
- [x] Custom foreground is selectable.
- [x] Custom accent is selectable.
- [x] Watch default time format is selectable.
- [x] Forced 12-hour time displays AM/PM.
- [x] Forced 24-hour time is selectable.
- [x] Date Off is selectable.
- [x] Word date is selectable.
- [x] ISO date is selectable.
- [x] US date is selectable.
- [x] EU date is selectable.
- [x] Battery uses the native battery service.
- [x] Seconds Off subscribes to minute ticks.
- [x] Real Clay Save sends settings.
- [x] Real Clay Cancel preserves settings.
- [x] Real Clay reload restores settings.
- [x] Host time policy tests pass.
- [x] Capture helper prepares at least twenty native cases.
- [x] Parent performs native visual review.
- [x] Fresh verifier reviews final source.
- [x] Secondary time uses UTC plus fixed manual offset.
- [x] Offset has 15-minute increments.
- [x] Offset supports UTC-12:00.
- [x] Offset supports UTC+14:00.
- [x] Offset help explains manual daylight-saving adjustment.

## Round compatibility — 2026-11-06
- [x] Emery remains a build target.
- [x] Chalk is a build target.
- [x] Gabbro is a build target.
- [x] The UUID is preserved.
- [x] Existing settings key mappings are preserved.
- [x] Native Chalk layout passes visual review.
- [x] Native Gabbro layout passes visual review.
- [x] Clean production PBW contains three native binaries.
- [x] Existing host/settings checks pass.
- [x] Fresh independent review passes.
No store publication is authorized by this compatibility request.

## Store round update — 2026-11-06
- [x] Publish the verified three-platform production update.
- [x] Preserve the current animated preview.
- [x] Add native screenshots for Chalk.
- [x] Add native screenshots for Gabbro.
- [x] Verify the public download matches the production artifact.
- [x] Verify public round screenshot pixels.
- [x] Fresh independent public-proof review passes.

## Combined World Timer — 2026-11-07

Scope: native0.2.0 local build only. Keep UUID and old key numbers. No store replacement or Git push. Preserve prior dirty work in .tmp/pre-combined before editing.

- [x] Amber-on-black is the fresh-install default.
- [x] Olive LCD can be selected.
- [x] Main city uses its IANA timezone rules.
- [x] Other city uses its IANA timezone rules.
- [x] Chicago spring DST boundary is correct.
- [x] Chicago autumn DST boundary is correct.
- [x] London/US mismatch weeks are correct.
- [x] Lord Howe half-hour DST is correct.
- [x] Kathmandu quarter-hour offset is correct.
- [x] Cuba reflects2026f rules.
- [x] Dates roll over according to each city.
- [x] Expired timezone data does not show confident city times.
- [x] Each call window uses its own city wall time.
- [x] Overnight call windows work.
- [x] Call bars use a common next24-hour UTC timeline.
- [x] Call bars account for a DST change inside that timeline.
- [x] Two case knocks trigger the travel animation.
- [x] A single impact cannot trigger double-knock mode.
- [x] Animation cannot restart while active.
- [x] Animation returns automatically to the resting map.
- [x] Local time stays readable during travel.
- [x] Time2 native layout passes visual review.
- [x] TimeRound native layout passes visual review.
- [x] Round2 native layout passes visual review.
- [x] Theme persists across reinstall.
- [x] Main city persists across reinstall.
- [x] Other city persists across reinstall.
- [x] Main call start persists across reinstall.
- [x] Main call end persists across reinstall.
- [x] Other call start persists across reinstall.
- [x] Other call end persists across reinstall.
- [x] Date Off remains available.
- [x] ISO date remains available.
- [x] US date remains available.
- [x] EU date remains available.
- [x] Production excludes fixture overrides.
- [x] A fresh independent review passes.

Combined0.2.0 complete:7060timezone cases, native three-target layouts, sensor/persistence, actual Clay lifecycle, sanitized policy and independent review PASS. Local build only.

## Authorized store update 0.2.0
- [x] Public PBW matches reviewed SHA256.
- [x] Emery gallery contains native travel preview.
- [x] Chalk gallery contains native travel preview.
- [x] Gabbro gallery contains native travel preview.
- [x] Public description explains city settings.
- [x] Fresh release reviewer passes.

Store0.2.0 published to the existing World Timer listing. Exact PBW, native three-device galleries, public description and independent release review pass.

## Departure board 0.3.0 contract
Surface: native C renderer, Clay settings, capture/verification scripts. Artifact: dist/World-Timer-0.3.0.pbw. Preserve UUID and AppMessage key numbers. No store upload or Git push.
- [x] Emery uses the approved departure-board composition.
- [x] Chalk uses the approved departure-board composition.
- [x] Gabbro uses the approved departure-board composition.
- [x] Only changed digits animate on a minute change.
- [x] Animation settles automatically.
- [x] Signed city difference follows current IANA offsets.
- [x] Signed city difference preserves quarter-hour precision.
- [x] Calendar-day difference remains separate.
- [x] Fresh-install theme is amber.
- [x] Olive remains selectable.
- [x] Custom colors remain selectable.
- [x] Call-hours UI is absent.
- [x] Call-hours settings are absent.
- [x] Date Off remains selectable.
- [x] Numeric date formats remain selectable.
- [x] 12-hour mode identifies AM/PM.
- [x] Production excludes fixture controls.
- [x] Native screenshots cover three target resolutions.
- [x] Native animation evidence covers three targets.
- [x] Relevant automated verification passes.
- [x] Fresh independent verification passes.

Departure0.3.0 complete locally: three native layouts, live timer checks,12 host tests,7060 timezone oracle instants, Clay migration, sanitized policy, exact production artifact and independent verifier PASS. Store not changed.

## Authorized0.3.0 publication
- [x] Public PBW matches reviewed0.3.0 hash.
- [x] Public Emery gallery contains split-flap preview.
- [x] Public Chalk gallery contains split-flap preview.
- [x] Public Gabbro gallery contains split-flap preview.
- [x] Public description describes departure-board behavior.
- [x] Independent release review passes.

Publication complete: exact0.3.0 public PBW,12 native gallery assets, description and independent public-asset verification PASS.
