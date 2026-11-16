---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-06T18:19:23-06:00"
---
# Round compatibility and native QA

## Targets
- Emery:200×228, existing rectangular drawing path.
- Chalk:180×180, original Time Round.
- Gabbro:260×260, Round2.

Use `PBL_ROUND` for both round targets. Round helpers use180 logical units and rasterize bitmap glyphs at the actual target resolution. Existing UUID/settings keys stay stable. The round layout is automatic; it is not a user setting. Keep each repository self-contained.

## Native fixture workflow
Run SDK builds and native captures in separate phases. Only one process may drive the shared SDK emulator. An install success does not prove the correct face reached the foreground.

```sh
python3 execution/build_round_fixture.py
python3 execution/capture_round.py --platform chalk --reset-emulator
python3 execution/capture_round.py --platform gabbro --reset-emulator
```

`--reset-emulator` backs up SDK flash under `.tmp/round-qa/emulator-backups/` before wiping emulator state. Never run it while another native QA task owns the emulator. QEMU is closed gracefully; never use SIGKILL. The second install handles the SDK's stale foreground/boot race.

Fixtures and logs live in `.tmp/round-qa/`. Production `dist/` is untouched. `execution/round_cases.json` records settings, deterministic fixture values, and palette peak for each native case. `--case default` captures just one case.

Fixture-only key11022 enables a magenta foreground marker plus a green/red layout marker. A native screenshot is accepted only after the magenta marker proves the intended fixture is running and the green marker confirms checked text/bitmap geometry fits the screen. The marker is cleared before saving clean media. Text widths are measured using native fonts; bitmap ink and polygon vertices are checked against the circular safe area. This audit does not prove that arbitrary intra-face content cannot overlap; inspect the captured variants too.

Outputs: `media/round/chalk-*.png`, `media/round/gabbro-*.png`, and `.tmp/round-qa/native-*.json`.

## Production boundary
After fixtures, stop the emulator before SDK builds. Clean-build production and verify its platform binaries:

```sh
pebble kill
python3 execution/build.py
python3 execution/verify.py
```

The production builder removes fixture environment flags. Do not copy fixture bundles into `dist/`. Physical-watch battery life, real phone location permissions, and live Health readings need device validation; emulator fixtures do not establish those results. Store publication is a separate action.
