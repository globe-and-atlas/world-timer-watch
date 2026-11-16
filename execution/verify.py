"""Verify identity, target, and generated numeral bounds in the production bundle."""
from pathlib import Path
import json
import zipfile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True,timeout=90)
    subprocess.run(['node','watchface/settings.test.js'],cwd=ROOT,check=True,timeout=30)
    host=ROOT/'.tmp/combined-policy-test'
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-Iwatchface/src/c','tests/combined_policy.c','watchface/src/c/city_policy.c','watchface/src/c/city_data.c','-o',str(host)],cwd=ROOT,check=True,timeout=60)
    subprocess.run([str(host)],check=True,timeout=60)
    package = json.loads((ROOT / 'watchface/package.json').read_text())
    assert package['pebble']['displayName'] == 'World Timer'
    assert package['pebble']['targetPlatforms'] == ['emery','chalk','gabbro']
    with zipfile.ZipFile(ROOT / f"dist/World-Timer-{package['version']}.pbw") as bundle:
        info = json.loads(bundle.read('appinfo.json'))
        assert info['uuid'] == package['pebble']['uuid']
        assert info['versionLabel'] == package['version']
        assert info['targetPlatforms'] == package['pebble']['targetPlatforms']
        assert 'emery/pebble-app.bin' in bundle.namelist()
        assert 'pebble-js-app.js' in bundle.namelist()
        for platform in ['emery','chalk','gabbro']:
            assert b'CALL NEXT24H' not in bundle.read(platform+'/pebble-app.bin'), 'Call-hours renderer in production'
            assert bundle.read(platform+'/pebble-app.bin') == (ROOT / 'watchface/build' / platform / 'pebble-app.bin').read_bytes()
    assert not json.loads((ROOT/'.tmp/last-build.json').read_text())['fixture']
    nm=Path.home()/'Library/Application Support/Pebble SDK/SDKs/current/toolchain/arm-none-eabi/bin/arm-none-eabi-nm'
    for platform in ['emery','chalk','gabbro']:
        symbols=subprocess.run([str(nm),str(ROOT/f'watchface/build/{platform}/pebble-app.elf')],check=True,capture_output=True,text=True,timeout=30).stdout
        for field in ['f_epoch','f_phase','f_format','f_previous']:assert field not in symbols, 'Fixture state in production: '+field
    print('PASS: World Timer production bundle for Emery, Chalk and Gabbro')


if __name__ == '__main__':
    main()
