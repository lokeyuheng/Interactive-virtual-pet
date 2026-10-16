"""Run the official TripoSR CLI in an isolated, recorded CPU experiment."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime


def main():
    root = Path(__file__).resolve().parent
    vendor = root / 'vendor' / 'TripoSR'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path)
    parser.add_argument('--resolution', type=int, choices=(64, 128, 256), default=128)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    required = ('torch', 'omegaconf', 'PIL', 'einops', 'torchmcubes',
                'transformers', 'trimesh', 'rembg', 'huggingface_hub',
                'imageio', 'xatlas', 'moderngl', 'onnxruntime')
    missing = [name for name in required if importlib.util.find_spec(name) is None]
    if not (vendor / 'run.py').is_file():
        print('Official source missing. Follow README.md to clone TripoSR.', file=sys.stderr)
        return 2
    if missing:
        print('Missing dependencies: ' + ', '.join(missing), file=sys.stderr)
        return 2
    if args.check:
        print('Source and dependency modules found. Native imports and inference are verified by a trial run.')
        return 0
    photo = args.image.resolve() if args.image else vendor / 'examples' / 'chair.png'
    if not photo.is_file():
        print(f'Image does not exist: {photo}', file=sys.stderr)
        return 2
    output = root / 'outputs' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    output.mkdir(parents=True)
    command = [sys.executable, '-u', str(vendor / 'run.py'), str(photo),
               '--device', 'cpu', '--mc-resolution', str(args.resolution),
               '--chunk-size', '4096', '--model-save-format', 'glb',
               '--output-dir', str(output)]
    try:
        revision = subprocess.check_output(['git', '-C', str(vendor), 'rev-parse', 'HEAD'], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    metadata = {'image': str(photo), 'device': 'cpu', 'resolution': args.resolution,
                'python': sys.version, 'source_commit': revision, 'command': command,
                'status': 'running'}
    manifest = output / 'trial.json'
    manifest.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(f'Running CPU reconstruction. Log and results: {output}', flush=True)
    start = time.perf_counter()
    with (output / 'run.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(command, cwd=vendor, stdout=log, stderr=subprocess.STDOUT)
    mesh = output / '0' / 'mesh.glb'
    metadata.update(elapsed_seconds=round(time.perf_counter() - start, 2),
                    exit_code=result.returncode,
                    status='success' if result.returncode == 0 and mesh.is_file() else 'failed')
    manifest.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(f"{metadata['status']}: {metadata['elapsed_seconds']} seconds")
    print(mesh if metadata['status'] == 'success' else output / 'run.log')
    return 0 if metadata['status'] == 'success' else (result.returncode or 1)


if __name__ == '__main__':
    raise SystemExit(main())
