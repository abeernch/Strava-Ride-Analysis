"""Separate TCX activities into a destination folder by sport type."""

from __future__ import annotations

import argparse
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TCX_NAMESPACE = {"ns": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy TCX files for a chosen sport into a destination folder."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.cwd(),
        help="Folder that contains TCX files. Default: current directory.",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("Moved"),
        help="Folder that will receive matching files. Default: Moved.",
    )
    parser.add_argument(
        "--sport",
        default="Ride",
        help="TCX sport name to match. Default: Ride.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search the source folder recursively for TCX files.",
    )
    parser.add_argument(
        "--clear-destination",
        action="store_true",
        help="Remove the destination folder before copying files.",
    )
    return parser.parse_args()


def read_activity_sport(file_path: Path) -> str | None:
    try:
        raw_text = file_path.read_text(encoding="utf-8")
        root = ET.fromstring(raw_text.lstrip())
    except (UnicodeDecodeError, ET.ParseError, OSError) as exc:
        print(f"[skip] {file_path.name}: could not parse TCX ({exc})")
        return None

    activity = root.find(".//ns:Activity", namespaces=TCX_NAMESPACE)
    if activity is None:
        return None
    return activity.get("Sport")


def iter_tcx_files(source: Path, recursive: bool, destination: Path) -> list[Path]:
    if recursive:
        files = []
        for path in source.rglob("*.tcx"):
            if destination in path.parents:
                continue
            files.append(path)
        return files
    return [path for path in source.glob("*.tcx") if destination not in path.parents]


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    destination = args.destination.resolve()

    if not source.exists() or not source.is_dir():
        print(f"[error] Source folder not found: {source}")
        return 1

    if args.clear_destination and destination.exists():
        shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)

    matched = 0
    scanned = 0
    for file_path in sorted(iter_tcx_files(source, args.recursive, destination)):
        scanned += 1
        sport = read_activity_sport(file_path)
        if sport == args.sport:
            target = destination / file_path.name
            shutil.copy2(file_path, target)
            matched += 1
            print(f"[copy] {file_path.name} -> {target}")
        else:
            print(f"[skip] {file_path.name}: sport={sport or 'Unknown'}")

    print(
        f"Completed. Scanned {scanned} TCX file(s); copied {matched} {args.sport} file(s) to {destination}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
