---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T16:22:54-06:00"
---
# World Timer departure board0.3.0

Goal: Build the approved departure-board preview for Time2, TimeRound and Round2.
Status: Published0.3.0; public download, description and three-device galleries verified.
Agent: OpenAI Codex
Handoff-from: OpenAI Codex
Handoff-type: continuation

## Delivered

- `dist/World-Timer-0.3.0.pbw`; same UUID0bd9074a-d5df-4b6b-99e7-90b829ab2aa7. SHA2567d84c1ae5684563a86a7b57ab51d1379266b67850c40af6be98045e8d954e497.
- Three independent native pixel layouts. Equal city clocks, individual split-flap digits;600ms flip with90ms second-row stagger. Only changed numeral tiles animate; timer settles by690ms. Optional transition disable.
- Signed Other-minus-Main difference from current IANA offsets, with fractional minutes; day delta separate. Amber default, Olive and Custom preserved. Date choices,12/24h, AM/PM and optional seconds remain. Long city labels use city code when needed.
- Call-hours UI and settings removed. Map/travel controls retired; no accelerometer subscription. Original key numbers retained; newFlapOn appended, defaults On independently of oldTravelOn. Legacy city/theme/custom settings migrate.

## Evidence

- `release/departure-0.3.0.json`, `release/departure-independent-review.json`.
-12 Python tests,7060 timezone oracle instants, real Clay Save/Cancel/reload/migration, ASan/UBSan and production bundle guards PASS. Four fixture globals absent from each production ELF.
- `.tmp/departure-native/{emery,chalk,gabbro}` contains13visual cases, fixed-phase and live AppTimer evidence; unchanged pixels outside changed tiles remain exact, old/new endpoints exact,5sGIF decoded duration exact, disabled transitions snap.
- Chalk/Gabbro reinstall restores cities/theme/date/animation state. Native hour, midnight and fall-DST reassembly pass on those targets. Gabbro production PBW foregrounded with live clocks.
- Six native amber/olive content images match the approved reference pixels. Round hardware mask outer2.5px is excluded and recorded separately; this is a display-boundary difference, not a glyph/layout change.
- Native presentation: `.tmp/departure-native/three-display-five-seconds.gif`, `amber-comparison.png`, `olive-comparison.png`. These show actual renderer captures enlarged2x; timed phase capture is distinct from live timer diagnostic movies.
- Fresh read-only reviewer independently verified source, native output, artifact hash/identity/platform binaries and production fixture exclusion: PASS.

## Publication

Exact reviewed PBW and12native assets uploaded once. Public media bytes/frames/timing verified; leadGIF order checked under all three device selectors. Description saved separately. CachedTime2 gallery initially reverted toold assets after hydration; waited for cache expiry and checked fully loaded currentSrc before final screenshot/proof. Six version-specific publisher guard tests PASS. Native media staging checks PASS.

## Handoff

Workflow: `directives/build_departure.md`; capture/render/persistence/rollover scripts underexecution/. The old combined0.2.0 scripts and pinned publisher are historical; do not reuse them to publish0.3.0. Historical0.2.0 receipt remains intact. Latest public proof is `release/departure-update/0.3.0/public-proof.json`; independent asset review in the same directory. User authorized publication in the following turn. Existing listing updated once using `execution/publish_departure.py`; no rebuild or repeated release upload. No Git commit or Git push. Preexisting dirty state preserved; changed-file backups `.tmp/pre-departure`.

A fixed0.3s reinstall wait initially sampled the OS spinner. Persistence checker now polls the exact expected foreground frame within12s; it does not reinterpret a spinner as lost settings.

Remaining: physical-watch performance/readability, battery endurance, companion-phone setup and voluntary sharing are not field-verified. Future timezone rule changes require regenerated data.

S.D.G.: Helps people read two cities quickly through the approved departure-board design and explicit signed time difference.
Feynman gap: Native visuals, timing and timezone math are verified; wrist readability, battery and real phone setup still require hardware trials.
