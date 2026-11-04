import os
import hashlib
from datetime import datetime


# STEP 1: Scan folder and collect file paths
def get_file_paths(folder_path, extensions=None):

    files = []

    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path!")
        return files

    def handle_walk_error(error):
        print(f"Error accessing folder: {error}")

    for root, directories, all_files in os.walk(
        folder_path, onerror=handle_walk_error
    ):

        for file in all_files:

            file_extension = os.path.splitext(file)[1].lower()

            if extensions and file_extension not in extensions:
                continue

            complete_path = os.path.join(root, file)

            if os.path.isfile(complete_path):
                files.append(complete_path)

    return files


# STEP 2: Calculate SHA-256 hash
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

    except OSError as error:
        print(f"Error reading file {file_path}: {error}")

    return None


# STEP 3: Find duplicate files
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

        # STEP 4: Display progress
        if index % 10 == 0 or index == total_files:
            print(f"Progress: {index}/{total_files} files scanned")

    print("\nScanning completed!")

    return hash_groups, failed_files


# STEP 5: Convert bytes into readable units
def format_size(size_bytes):

    size = float(size_bytes)

    for unit in ["B", "KB", "MB", "GB", "TB"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# STEP 6: Generate duplicate report
def generate_report(hash_groups, total_files, folder_path,
                    failed_files=None):

    if failed_files is None:
        failed_files = []

    duplicate_count = 0
    duplicate_files = 0
    extra_copies = 0
    total_duplicate_size = 0
    extra_storage = 0

    report = []

    report.append("=" * 45)
    report.append("          DUPLICATE FINDER REPORT")
    report.append("=" * 45)

    report.append(f"\nScanned folder: {folder_path}")
    report.append(f"Total files found: {total_files}")

    for file_hash, file_list in hash_groups.items():

        if len(file_list) > 1:

            duplicate_count += 1
            duplicate_files += len(file_list)
            extra_copies += len(file_list) - 1

            report.append(f"\nDuplicate Group {duplicate_count}:")

            group_size = 0

            for file_path in file_list:

                report.append(file_path)

                try:
                    group_size += os.path.getsize(file_path)

                except OSError:
                    report.append(
                        f"Warning: Could not get size of {file_path}"
                    )

            total_duplicate_size += group_size

            try:
                original_size = os.path.getsize(file_list[0])

            except OSError:
                original_size = 0

            extra_storage += max(0, group_size - original_size)

    if duplicate_count == 0:
        report.append("\nNo duplicate files found!")

    report.append("\n" + "-" * 45)
    report.append("STATISTICS")
    report.append("-" * 45)

    report.append(f"Total files scanned: {total_files}")
    report.append(f"Duplicate groups: {duplicate_count}")
    report.append(f"Duplicate files: {duplicate_files}")
    report.append(f"Extra copies: {extra_copies}")

    report.append(
        f"Total size of duplicate-group files: "
        f"{format_size(total_duplicate_size)}"
    )

    report.append(
        f"Potentially recoverable extra storage: "
        f"{format_size(extra_storage)}"
    )

    report.append(f"Files that could not be read: {len(failed_files)}")

    if failed_files:
        report.append("\nUNREADABLE FILES:")

        for file_path in failed_files:
            report.append(file_path)

    report.append(
        "\nReport generated: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return "\n".join(report)


# STEP 7: Display report
def display_report(report):
    print(report)


# STEP 8: Save report
def save_report(report):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = os.path.join(
        "reports",
        f"duplicate_report_{timestamp}.txt"
    )

    try:
        with open(report_path, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"\nReport saved successfully: {report_path}")

    except OSError as error:
        print(f"Error saving report: {error}")


# STEP 9: Delete duplicate files with confirmation
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

        original_file = file_list[0]
        print(f"Preserved: {original_file}")

        for duplicate_file in file_list[1:]:

            print(f"\nExtra copy: {duplicate_file}")

            choice = input(
                "Delete this file? (yes/no): "
            ).strip().lower()

            if choice not in ("yes", "y"):
                print("File preserved!")
                continue

            # Verify that the file is still identical
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


# STEP 10: Scan folder and perform operations
def scan_folder():

    folder_path = input(
        "\nEnter folder path to scan: "
    ).strip().strip('"')

    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path!")
        return

    # STEP 11: File extension filtering
    print("\nChoose file filter:")
    print("1. Scan all files")
    print("2. Scan selected extensions")

    filter_choice = input("Enter your choice: ").strip()

    extensions = None

    if filter_choice == "2":

        extension_input = input(
            "Enter extensions separated by commas "
            "(e.g. .pdf,.txt): "
        ).strip()

        extensions = {
            extension.strip().lower()
            for extension in extension_input.split(",")
            if extension.strip()
        }

        if not extensions or any(
            not extension.startswith(".")
            or len(extension) < 2
            for extension in extensions
        ):
            print("Error: Enter valid extensions such as .pdf or .txt!")
            return

    elif filter_choice != "1":
        print("Invalid filter choice!")
        return

    # STEP 12: Get file paths
    files = get_file_paths(folder_path, extensions)

    if not files:
        print("No matching files found!")
        return

    print(f"\nTotal files found: {len(files)}")

    # STEP 13: Find duplicates
    hash_groups, failed_files = find_duplicates(files)

    # STEP 14: Generate and display report
    report = generate_report(
        hash_groups,
        len(files),
        folder_path,
        failed_files
    )

    display_report(report)

    # STEP 15: Display available actions
    print("\n1. Save report")
    print("2. Delete duplicate copies")
    print("3. Return to main menu")

    action = input("Enter your choice: ").strip()

    if action == "1":
        save_report(report)

    elif action == "2":
        delete_duplicates(hash_groups)

    elif action == "3":
        print("Returning to main menu...")

    else:
        print("Invalid choice!")


# STEP 16: Main menu with repeating loop
def main():

    while True:

        print("\n" + "=" * 40)
        print("          DUPLICATE FINDER")
        print("=" * 40)

        print("\n1. Scan a folder")
        print("2. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            scan_folder()

        elif choice == "2":
            print("\nThank you for using Duplicate Finder!")
            break

        else:
            print("\nInvalid choice! Please select 1 or 2.")


if __name__ == "__main__":
    main()