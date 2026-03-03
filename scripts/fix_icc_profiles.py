#!/usr/bin/env python3
"""Backup PNG files and re-save them without embedded ICC profiles (iCCP).

Usage:
  python scripts/fix_icc_profiles.py --root . --backup backups/icc_backup_YYYYMMDD

By default it will create a backup of each PNG before modifying it.
"""
from __future__ import annotations
import os
import shutil
import argparse
from datetime import datetime

def fix_png(path: str) -> bool:
    try:
        from PIL import Image
    except Exception as e:
        print("Pillow is required. Install with: pip install pillow")
        raise

    try:
        img = Image.open(path)
        info = img.info
        if 'icc_profile' not in info:
            return False
        img2 = img.copy()
        # Save without supplying icc_profile, which strips it
        img2.save(path, optimize=True)
        return True
    except Exception as e:
        print(f"ERROR processing {path}: {e}")
        return False

def main(root: str, backup_root: str, dry_run: bool) -> None:
    root = os.path.abspath(root)
    backup_root = os.path.abspath(backup_root)
    os.makedirs(backup_root, exist_ok=True)
    processed = 0
    backed_up = 0
    total = 0

    for dirpath, dirs, files in os.walk(root):
        # skip backup folder if inside root
        try:
            if os.path.commonpath([backup_root, dirpath]) == backup_root:
                continue
        except Exception:
            pass
        for fname in files:
            if not fname.lower().endswith('.png'):
                continue
            total += 1
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root)
            bak_path = os.path.join(backup_root, rel)
            os.makedirs(os.path.dirname(bak_path), exist_ok=True)
            try:
                shutil.copy2(full, bak_path)
                backed_up += 1
            except Exception as e:
                print(f"Failed to backup {full}: {e}")
                continue

            if dry_run:
                continue

            try:
                changed = fix_png(full)
                if changed:
                    processed += 1
            except Exception:
                # fix_png prints the error
                continue

    print(f"Total PNGs found: {total}")
    print(f"Backed up: {backed_up} -> {backup_root}")
    print(f"Re-saved without ICC profile: {processed}")

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Backup and strip iCCP profiles from PNGs')
    p.add_argument('--root', default='.', help='Root folder to scan for PNGs')
    default_backup = os.path.join('backups', 'icc_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    p.add_argument('--backup', default=default_backup, help='Backup root folder')
    p.add_argument('--dry-run', action='store_true', help='Only backup, do not modify files')
    args = p.parse_args()
    main(args.root, args.backup, args.dry_run)
