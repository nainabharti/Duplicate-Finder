import os
import hashlib
#1.
def get_file_paths(folder_path):
    files = []

    all_files = os.listdir(folder_path)

    for file in all_files:
        complete_path = os.path.join(folder_path, file)

        if os.path.isfile(complete_path):
            files.append(complete_path)

    return files

#2.
def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        content = file.read()
        sha256_hash.update(content)

    return sha256_hash.hexdigest()

def main():
    folder_path = "test-files"

    files = get_file_paths(folder_path)

    print("Files found:")
    print(files)

    for file_path in files:
        result = calculate_hash(file_path)
        print(file_path, result)

if __name__ == "__main__":
    main()

