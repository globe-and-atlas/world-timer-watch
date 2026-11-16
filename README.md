---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T16:19:18-06:00"
---
# World Timer — Departure Board

Published0.3.0 implements the approved split-flap departure board for Time2(Emery200×228), TimeRound(Chalk180×180) and Round2(Gabbro260×260). Live at [World Timer](https://apps.repebble.com/world-timer_dc42aa6ca1cf447785720f80). Public0.3.0 PBW and12native media assets verified against reviewed bytes/frames/timing. Receipt: `release/departure-update/0.3.0/public-proof.json`.

Two equal city rows display the selected cities independently of watch local timezone. Default Main Chicago and Other Tokyo. Amber on black is the fresh-install default; choose Olive LCD or custom background/ink/flap borders.

On a minute change, only changing numeral tiles flip. The second row follows90ms later; animation settles within690ms. Transitions can be disabled. The signed difference beside Other is relative to Main: +15H means15hours ahead, -5:45H means5hours45minutes behind. This follows current city DST rules. +1D or -1D below the second row means a separate calendar-day difference.

The approved board has no call-hours section or settings. It has no map or map-travel gesture. It does not subscribe to accelerometer data. Existing settings keep their key numbers; retired call/map controls are ignored. Cities, themes and custom colors migrate.

Date options: Off, weekday/day/month, ISO, US, European. Watch-default/12h/24h time format;12h uses AM/PM. Optional seconds default Off. Long city names use their city code when needed to leave room for the difference.

Forty cities use offline official IANA2026f transitions for2020–2037. Government changes require a future table update. Expired data says ZONE DATA EXPIRED instead of guessing. Prior generator/provenance and7060-instant oracle remain in place.

Build: `python3 execution/build.py`. Artifact: `dist/World-Timer-0.3.0.pbw`. Verify using `/Users/danielbally/.local/share/uv/tools/pebble-tool/bin/python3 execution/verify.py` (installed SDK dependencies). Native fixture/capture workflow: `directives/build_departure.md`.

Native evidence: `.tmp/departure-native/`; production manifest: `release/departure-0.3.0.json`. Phase-capture previews and live timer checks are emulator evidence. Physical watch readability, battery endurance and companion install remain separate field checks.
