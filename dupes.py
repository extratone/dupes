import os
import hashlib
import argparse

def find_duplicates(directory):
    """
    Finds duplicate files in the given directory and its subdirectories.

    Args:
      directory: The path to the directory to search.

    Returns:
      A dictionary where keys are SHA-256 hashes and
      values are lists of file paths with that hash.
    """
    hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            if file_hash in hashes:
                hashes[file_hash].append(filepath)
            else:
                hashes[file_hash] = [filepath]
    return {h: files for h, files in hashes.items() if len(files) > 1}

def delete_duplicates(duplicates, show_all=False, created=False):
    """
    Prompts the user to delete duplicate files.

    Args:
        duplicates: A dictionary of duplicate files as returned by 
                    find_duplicates.
        show_all: If True, shows all duplicates in a single response.
        created: If True, offers to delete only the latest created files.
    """
    if show_all:
        all_duplicates = []
        for file_hash, files in duplicates.items():
            all_duplicates.extend(files)
        if all_duplicates:
            print("Found the following duplicate files:")
            for file in all_duplicates:
                print(f"  - {file}")
            response = input("Delete these duplicates? (y/n): ")
            if response.lower() == "y":
                for file in all_duplicates[1:]:  # Keep the first file
                    os.remove(file)
                    print(f"Deleted {file}")
    else:
        for file_hash, files in duplicates.items():
            if created:
                # Sort files by creation time, keeping only the oldest
                files.sort(key=lambda f: os.path.getctime(f))
                print(f"Found the following duplicate files with hash 
                      {file_hash}:")
                for file in files[1:]:  # Skip the oldest file
                    print(f"  - {file}")
                response = input("Delete these duplicates? (y/n): ")
                if response.lower() == "y":
                    for file in files[1:]:  # Keep the first file
                        os.remove(file)
                        print(f"Deleted {file}")
            else:
                print(f"Found the following duplicate files with hash 
                      {file_hash}:")
                for file in files:
                    print(f"  - {file}")
                response = input("Delete these duplicates? (y/n): ")
                if response.lower() == "y":
                    for file in files[1:]:  # Keep the first file
                        os.remove(file)
                        print(f"Deleted {file}")

def main():  # Added main function for entry point
    parser = argparse.ArgumentParser(
        description="Find and delete duplicate files.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all duplicates in a single response",
    )
    parser.add_argument(
        "--created",
        action="store_true",
        help="Offer to delete only the latest created files",
    )
    args = parser.parse_args()

    current_directory = os.getcwd()
    duplicates = find_duplicates(current_directory)
    delete_duplicates(duplicates, show_all=args.show_all, created=args.created)

if __name__ == "__main__":
    main()
