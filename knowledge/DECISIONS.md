---
generated_by: "OpenAI Codex (GPT-6)"
timestamp: "2026-11-06T11:30:00-06:00"
---
# Design decisions
- Preserve inspiration through layout and visual hierarchy while using original names, native system fonts, original segment geometry, and original map data.
- Keep the fixed black surround for LCD contrast; custom background means LCD-field background.
- Use a dedicated small seconds layer. Minute/date/secondary clock and battery updates redraw the static face when needed.
- Represent the six presets as indexes 0–5 and Custom as index 6.
- Validate settings on both JavaScript and C boundaries before persistence.
- Secondary offset is index0–104; minutes=(index−48)×15. Use gmtime(epoch+offset) and compare Gregorian civil-day ordinals for rollover including year crossings.

- Native World capture verifies secondary numerals using original small seven-segment geometry, samples both analog hand orientations, and verifies civil-day indicator visibility. Calendar fixture messages permit New Year ±2-day tests; production ignores them.

## 2026-11-06 — Native round layouts
Keep Emery's original draw path behind round-only branches. Add Chalk and Gabbro to the same UUID rather than creating separate products. Dedicated circular compositions were chosen over cropping the rectangular face, preserving readable hierarchy and existing settings. Shared helpers use180 logical units and rasterize at each screen's actual resolution. Round selection is automatic, with no added settings key. Local0.1.1 is not published by this task.

## 2026-11-07 — combined design

Amber/Olive themes replace the generic instrument layout for local0.2.0; old UUID/key numbers remain. Named city clocks use pinned IANA tables, not previous fixed-offset controls. Both reference and other city are explicit choices. Common NEXT24H UTC call bars were chosen over a00–24 local-day axis to avoid DST missing/repeated-hour ambiguity. Compact original5×7 labels and scalable seven-segment numerals fit180px round. Double-case-knock travel uses the verified LooseDigits-style raw impulse policy; touch events remain unsupported for watchfaces.

## 2026-11-07 — approved departure board supersedes LCD map layout

User rejected the uneven LCD renderer, approved split-flap city rows and then explicitly removed call hours. Version0.3.0 uses independent native pixel coordinates for each target. Shared180-unit stretching was rejected because it varies one-pixel stroke widths. Bitmap glyphs use integer scale3/4/5 with fixed one-pixel labels and tile borders; only changed numeral panels project vertically during a flip. Dates remain static.

Signed difference is Other-minus-Main IANA offset at current UTC, formatted with fractional minutes when present. Day delta remains separate. Long labels fall back to the selected city code if they cannot fit beside the signed difference.12h mode keeps four tile positions with blank leading hour and separate AM/PM. Seconds are optional static labels.

The removed map makes the old map-travel gesture/control obsolete; no accelerometer is subscribed. Retired hour/travel AppMessage and persistence numbers stay reserved. A new appended FlapOn key defaults On independently of old travel settings. Published city/theme/custom-color settings migrate through Clay; retired settings are dropped. Existing0.2.0 artifact and store receipts remain intact.
