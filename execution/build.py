"""Clean-build production World Timer; fixture flags are deliberately removed."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--fixture',action='store_true');args=parser.parse_args()
    env = {key: value for key, value in os.environ.items() if not key.startswith('WORLD_')}
    if args.fixture:env['WORLD_FIXTURE']='1'
    for command in [['pebble', 'clean'], ['pebble', 'build']]:
        subprocess.run(command, cwd=ROOT / 'watchface', env=env, check=True)
    version=json.loads((ROOT/'watchface/package.json').read_text())['version']
    target=ROOT/('.tmp/World-Timer-fixture.pbw' if args.fixture else f'dist/World-Timer-{version}.pbw')
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'watchface/build/watchface.pbw', target)
    (ROOT/'.tmp/last-build.json').write_text(json.dumps({'fixture':args.fixture,'path':str(target)},indent=2))
    print(f'Bundle: {target}')


if __name__ == '__main__':
    main()
