#!/usr/bin/env python3
"""Require the bundled OpenBIOS at both the runtime and codegen paths."""
import argparse
from pathlib import Path
import zipfile


def check(archive):
    with zipfile.ZipFile(archive) as package:
        runtime = package.read("bios/openbios.bin")
        sdk = package.read("psxrecomp/bios/openbios.bin")
        if not runtime or runtime != sdk:
            raise ValueError("runtime OpenBIOS is empty or differs from the SDK image")
    print(f"PASS: {archive.name} includes matching runtime and SDK OpenBIOS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        check(args.archive)
    except (KeyError, OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Invalid setup BIOS layout: {error}\n")
