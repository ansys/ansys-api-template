#!/usr/bin/env python
"""Hook to copy the .proto files into the project, and create __init__.py and py.typed files."""
import os
import pathlib
import shutil
import sys

PROTOS_DIR = "{{ cookiecutter.protos_dir }}"

DEST_PATH = (
    pathlib.Path("src")
    / "ansys"
    / "api"
    / "{{ cookiecutter.product_name | slugify(separator='_') }}"
    / "{{ cookiecutter.library_name | slugify(separator='_') }}"
)
VERSION_DEST_PATH = DEST_PATH / "v{{ cookiecutter.api_version }}"

init_content = """\
\"\"\"Autogenerated Python gRPC interface package for {{ cookiecutter.project_slug }}.\"\"\"

import pathlib

__all__ = ["__version__"]

with open(pathlib.Path(__file__).parent / "VERSION", encoding="utf-8") as f:
    __version__ = f.read().strip()
"""

if PROTOS_DIR:
    source_path = pathlib.Path(PROTOS_DIR)

    if not source_path.is_dir():
        print(f"ERROR: Path '{source_path}' does not exist.")
        sys.exit(1)

    shutil.copytree(source_path, VERSION_DEST_PATH)
else:
    os.makedirs(VERSION_DEST_PATH)
    print(
        "\nNOTE: No protos directory specified. Make sure to manually "
        f"copy the .proto files to '{VERSION_DEST_PATH.absolute()}'."
    )

with open(DEST_PATH / "__init__.py", mode="w", encoding="utf-8") as out_f:
    out_f.write(init_content)
(DEST_PATH / "py.typed").touch()
with open(DEST_PATH / "VERSION", mode="w", encoding="utf-8") as out_f:
    out_f.write("{{ cookiecutter.api_package_version }}")
