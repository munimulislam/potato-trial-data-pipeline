"""
@File - files.py
@Author - MdMunimul.Islam@teagasc.ie
@Created - 02/10/2026
@Description - Description of the file.
"""

from pathlib import Path


def discover_files(source_dir: str, file_extensions: list[str]) -> list[Path]:
    incoming_dir = Path(source_dir)
    extensions = {e.lower() for e in file_extensions}
    files = [
        f
        for f in incoming_dir.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    ]
    return files


def archive_file(archive_dir: Path, file: str | Path):
    file = Path(file)
    target_path = archive_dir / file.name
    file.move(target_path)
