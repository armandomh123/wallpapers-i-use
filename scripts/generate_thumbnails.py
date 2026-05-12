#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
THUMBNAIL_SIZE = "300x300"


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def needs_update(source: Path, thumbnail: Path) -> bool:
    if not thumbnail.exists():
        return True
    return source.stat().st_mtime > thumbnail.stat().st_mtime


def generate_thumbnail(source: Path, thumbnail: Path) -> None:
    thumbnail.parent.mkdir(parents=True, exist_ok=True)
    for command in ("magick", "convert"):
        try:
            subprocess.run(
                [
                    command,
                    str(source),
                    "-resize",
                    THUMBNAIL_SIZE,
                    "-background",
                    "white",
                    "-gravity",
                    "center",
                    "-extent",
                    THUMBNAIL_SIZE,
                    str(thumbnail),
                ],
                check=True,
            )
            return
        except FileNotFoundError:
            continue
    raise FileNotFoundError("ImageMagick not found. Install 'magick' or 'convert'.")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    sources = sorted(p for p in repo_root.iterdir() if is_image(p))
    if not sources:
        print("No images found. Nothing to do.")
        return 0

    updated = 0
    skipped = 0
    failures = 0

    for source in sources:
        thumbnail = repo_root / "thumbnails" / f"thumb_{source.name}"
        if not needs_update(source, thumbnail):
            skipped += 1
            continue
        try:
            generate_thumbnail(source, thumbnail)
            updated += 1
        except subprocess.CalledProcessError as exc:
            failures += 1
            print(f"Failed: {source.name} ({exc})")

    print(
        "Done. Updated: {updated}, Skipped: {skipped}, Failed: {failures}".format(
            updated=updated, skipped=skipped, failures=failures
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
