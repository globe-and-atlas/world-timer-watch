---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T16:19:18-06:00"
---
# Build the departure-board World Timer

Keep app UUID and existing AppMessage key numbers. Targets are Emery200×228, Chalk180×180 and Gabbro260×260. Build the approved two equal city rows using independent integer-pixel layouts. Amber default; Olive and Custom alternatives. Remove call-hour and map-travel controls. Keep explicit cities, IANA DST, date formats,12/24-hour modes and optional seconds.

A changed minute flips only changed numeral tiles. The two rows are staggered90ms; each flip lasts600ms. Timer ends by690ms and returns to static minute updates. Turning transitions Off snaps to the new digits. No accelerometer subscription. The signed hour difference is Other offset minus Main offset at the same UTC instant; keep fractional minutes. Calendar-day delta is separate.

Use `python3 execution/build.py --fixture` for `.tmp/World-Timer-fixture.pbw`. Own exactly one emulator; install the fixture, then run `python3 execution/capture_departure.py --platform <target>`. Cases cover amber/olive/custom, signed/fractional/zero differences, long names/ISO,12h/seconds, date choices and expired data. Fixed animation phases assert old/new endpoints and stable pixels outside the changed tiles; a separate live AppTimer trial proves intermediates and settle.

Run `check_departure_persistence.py` for reinstall proof; its bounded visual wait must outlast the launch spinner. Run `check_departure_rollovers.py` for hour/midnight/DST cases. Only one command may drive the emulator at a time.

`render_departure_evidence.py` makes native comparison sheets and a five-second composite from phase captures. It uses integer2x presentation and explicitly labels phase evidence.

Finish with `python3 execution/build.py` and the Pebble SDK Python environment running `execution/verify.py`. A fresh independent verifier reviews source, captures and final production PBW. No publication from this directive: the prior0.2.0 receipt is historical, and its publisher is pinned to those old bytes.
