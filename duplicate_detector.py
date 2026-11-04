import os
from hash_calculator import calculate_hash


def find_duplicates(files):

    hash_groups = {}
    failed_files = []

    total_files = len(files)

    print("\nScanning files...")

    for index, file_path in enumerate(files, start=1):

        file_hash = calculate_hash(file_path)

        if file_hash is None:
            failed_files.append(file_path)

        else:

            if file_hash in hash_groups:
                hash_groups[file_hash].append(file_path)

            else:
                hash_groups[file_hash] = [file_path]

        # Display progress after every 10 files
        if index % 10 == 0 or index == total_files:
            print(f"Progress: {index}/{total_files} files scanned")

    print("\nScanning completed!")

    return hash_groups, failed_files


def delete_duplicates(hash_groups):

    duplicate_groups = [
        (file_hash, file_list)
        for file_hash, file_list in hash_groups.items()
        if len(file_list) > 1
    ]

    if not duplicate_groups:
        print("\nNo duplicate files available for deletion!")
        return

    print("\nThe first file in each group will be preserved.")

    confirmation = input(
        "\nDo you want to review and delete extra copies? (yes/no): "
    ).strip().lower()

    if confirmation not in ("yes", "y"):
        print("Deletion cancelled!")
        return

    deleted_count = 0

    for group_number, (original_hash, file_list) in enumerate(
        duplicate_groups, start=1
    ):

        print(f"\nDuplicate Group {group_number}:")

        print(f"Preserved: {file_list[0]}")

        for duplicate_file in file_list[1:]:

            print(f"\nExtra copy: {duplicate_file}")

            choice = input(
                "Delete this file? (yes/no): "
            ).strip().lower()

            if choice not in ("yes", "y"):
                print("File preserved!")
                continue

            # Recheck the file before deleting it
            current_hash = calculate_hash(duplicate_file)

            if current_hash != original_hash:
                print("File changed or could not be read. Skipping deletion!")
                continue

            try:
                os.remove(duplicate_file)
                print("File deleted successfully!")
                deleted_count += 1

            except OSError as error:
                print(f"Could not delete file: {error}")

    print(f"\nTotal files deleted: {deleted_count}")