import os
import hashlib


# Step 1: Collect all file paths, including subfolders
def get_file_paths(folder_path):
    files = []

    try:
        for root, directories, all_files in os.walk(folder_path):

            for file in all_files:
                complete_path = os.path.join(root, file)
                files.append(complete_path)

    except PermissionError:
        print("Error: Permission denied to access folder!")

    return files


# Step 2: Calculate SHA256 hash using chunks
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:

            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

    except PermissionError:
        print(f"Error: Permission denied - {file_path}")

    return None


# Step 3: Group files using their hashes
def find_duplicates(files):
    hash_groups = {}

    for file_path in files:
        file_hash = calculate_hash(file_path)

        if file_hash is None:
            continue

        if file_hash in hash_groups:
            hash_groups[file_hash].append(file_path)

        else:
            hash_groups[file_hash] = [file_path]

    return hash_groups


# Step 4: Display duplicate files and statistics
def display_duplicates(hash_groups, total_files):
    duplicate_count = 0
    duplicate_files = 0
    extra_copies = 0

    print("\nDuplicate Finder Report")

    for file_hash, file_list in hash_groups.items():

        if len(file_list) > 1:
            duplicate_count += 1
            duplicate_files += len(file_list)
            extra_copies += len(file_list) - 1

            print(f"\nDuplicate Group {duplicate_count}:")

            for file_path in file_list:
                print(file_path)

    if duplicate_count == 0:
        print("\nNo duplicate files found!")

    print("\n--- Statistics ---")
    print(f"Total files scanned: {total_files}")
    print(f"Total duplicate groups: {duplicate_count}")
    print(f"Total duplicate files: {duplicate_files}")
    print(f"Total extra copies: {extra_copies}")


# Main function
def main():
    print("\n================================")
    print("       DUPLICATE FINDER")
    print("================================")

    print("\n1. Scan a folder")
    print("2. Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":

        folder_path = input("Enter folder path to scan: ").strip()

        if not os.path.isdir(folder_path):
            print("Error: Invalid folder path!")
            return

        files = get_file_paths(folder_path)

        hash_groups = find_duplicates(files)

        display_duplicates(hash_groups, len(files))

    elif choice == "2":
        print("Thank you for using Duplicate Finder!")

    else:
        print("Invalid choice! Please select 1 or 2.")


if __name__ == "__main__":
    main()