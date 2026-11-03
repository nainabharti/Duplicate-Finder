import os
import hashlib
# step 1: Collect all file paths
def get_file_paths(folder_path):
    files = []
    try:
        all_files = os.listdir(folder_path)

        for file in all_files:
            complete_path = os.path.join(folder_path, file)

            if os.path.isfile(complete_path):
                files.append(complete_path)

    except FileNotFoundError:
        print("Error: Folder not found!")

    except PermissionError:
        print("Error: Permission denied to access folder!")

    return files

# step 2: Calculate SHA256 hash
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            content = file.read()
            sha256_hash.update(content)

        return sha256_hash.hexdigest()

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

    except PermissionError:
        print(f"Error: Permission denied - {file_path}")

    return None

# step 3: Group file using their hashes
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
        
# step 4: display only duplicate files and statistics
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

    print("\n---Statistics---")
    print(f"Total files scanned: {total_files}")
    print(f"Total duplicate groups: {duplicate_count}")
    print(f"Total duplicate files: {duplicate_files}")
    print(f"Total extra copies: {extra_copies}")
   
def main():
    folder_path = "test-files"

    files = get_file_paths(folder_path)

    print("Files found:")
    print(files)

    hash_groups = find_duplicates(files)

    display_duplicates(hash_groups, len(files))

if __name__ == "__main__":
    main()

