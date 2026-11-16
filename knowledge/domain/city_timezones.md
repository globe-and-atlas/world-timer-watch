---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T14:20:54-06:00"
---

# City timezone and call-window policy

- Pinned official IANA2026f, validity2020–2037. Native data:40stable city IDs,740transitions, exact UTC seconds plus minute offsets. Generator/source hash in release/timezone-source.json. Host Python tzdata2025c was intentionally not used.
- All40choices have meaningful map coordinates; an early unpublished UTC-at0,0 draft was replaced by Madrid before completing this build. IDs are stable for subsequent releases.
- Pure C binary search resolves each city offset independently. Own portable Gregorian civil conversion avoids Pebble SDK time.h stubs and shared gmtime storage. No approximate DST formulas or manual offset inference.
- Call windows are daily own-city wall-time intervals. Endpoint excluded. Overnight ranges wrap. Equal endpoints closed;0–24 full day. Next24h samples actual UTC instants, so spring gaps and autumn repeated hours follow each zone transition correctly.
- Main city is a selected reference, not detected GPS/local watch location. Both city dates and signed civil-day difference are calculated from selected-city clocks.
- At data expiry suppress confident times; if future call horizon exceeds data coverage suppress bars with UPDATE ZONES. Rule changes before expiry still require a data update, just as upstream tzdb changes do.
- Map geometry is schematic; connecting arc is not flight/navigation data. A moving dot has a finite2.5s timer and never hides the clock.
