import os
import hashlib
# step 1: Collect all file paths
def get_file_paths(folder_path):
    files = []

    all_files = os.listdir(folder_path)

    for file in all_files:
        complete_path = os.path.join(folder_path, file)

        if os.path.isfile(complete_path):
            files.append(complete_path)

    return files

# step 2: Calculate SHA256 hash
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        content = file.read()
        sha256_hash.update(content)

    return sha256_hash.hexdigest()

# step 3: Group file using their hashes
def find_duplicates(files):
    hash_groups = {}

    for file_path in files:
        file_hash = calculate_hash(file_path)

        if file_hash in hash_groups:

            hash_groups[file_hash].append(file_path)
        else:
            hash_groups[file_hash] = [file_path]

    return hash_groups
        
# step 4: display only duplicate files
def display_duplicates(hash_groups):
    duplicate_count = 0

    for file_hash, file_list in hash_groups.items():

        if len(file_list) > 1:
            duplicate_count += 1

            print(f"\nDuplicate Group {duplicate_count}:")

            for file_path in file_list:
                print(file_path)

    if duplicate_count == 0:
        print("\nNo duplicate files found!")
    else:
        print(f"\nTotal duplicate groups: {duplicate_count}")

def main():
    folder_path = "test-files"

    files = get_file_paths(folder_path)

    print("Files found:")
    print(files)

    hash_groups = find_duplicates(files)

    display_duplicates(hash_groups)
if __name__ == "__main__":
    main()

