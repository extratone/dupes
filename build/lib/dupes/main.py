# dupes/main.py

import os
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict

def calculate_hash(file_path, block_size=65536):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(block_size):
            sha256.update(chunk)
    return sha256.hexdigest()

def find_duplicates(directory):
    file_hashes = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                file_hash = calculate_hash(file_path)
                file_hashes[file_hash].append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return {hash_value: paths for hash_value, paths in file_hashes.items() if len(paths) > 1}

def show_all_duplicates(duplicates):
    for hash_value, paths in duplicates.items():
        print(f"\nHash: {hash_value}")
        for path in paths:
            print(f"  {path}")

def prompt_deletion(files, keep_oldest=True):
    if keep_oldest:
        files = sorted(files, key=lambda x: x.stat().st_ctime)
        files_to_delete = files[1:]  # Keep the oldest file
    else:
        files_to_delete = files

    for file_path in files_to_delete:
        response = input(f"Delete {file_path}? (y/n): ").strip().lower()
        if response == "y":
            try:
                file_path.unlink()
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Could not delete {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Find and manage duplicate files in a directory.")
    parser.add_argument("--show-all", action="store_true", help="Show all found duplicates in a single list.")
    parser.add_argument("--created", action="store_true", help="Offer to delete only the latest duplicates, preserving the oldest.")
    args = parser.parse_args()

    directory = Path.cwd()
    duplicates = find_duplicates(directory)

    if args.show_all:
        show_all_duplicates(duplicates)

    for hash_value, files in duplicates.items():
        print(f"\nDuplicate set with hash {hash_value}:")
        for file in files:
            print(f"  {file}")

        if args.created:
            prompt_deletion(files, keep_oldest=True)
        else:
            prompt_deletion(files, keep_oldest=False)

if __name__ == "__main__":
    main()
