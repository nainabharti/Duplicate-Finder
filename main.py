import os

from file_scanner import get_file_paths
from duplicate_detector import find_duplicates, delete_duplicates

from report_generator import (
    generate_report,
    display_report,
    save_report
)


def scan_folder():

    folder_path = input(
        "\nEnter folder path to scan: "
    ).strip().strip('"')

    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path!")
        return

    # File extension filtering
    print("\nChoose file filter:")
    print("1. Scan all files")
    print("2. Scan selected extensions")

    filter_choice = input("Enter your choice: ").strip()

    extensions = None

    if filter_choice == "2":

        extension_input = input(
            "Enter extensions separated by commas (e.g. .pdf,.txt): "
        ).strip()

        extensions = {
            extension.strip().lower()
            for extension in extension_input.split(",")
            if extension.strip()
        }

        if not extensions or any(
            not extension.startswith(".") or len(extension) < 2
            for extension in extensions
        ):
            print("Error: Enter valid extensions such as .pdf or .txt!")
            return

    elif filter_choice != "1":
        print("Invalid filter choice!")
        return

    # Get file paths
    files = get_file_paths(folder_path, extensions)

    if not files:
        print("No matching files found!")
        return

    print(f"\nTotal files found: {len(files)}")

    # Find duplicates
    hash_groups, failed_files = find_duplicates(files)

    # Generate and display report
    report = generate_report(
        hash_groups,
        len(files),
        folder_path,
        failed_files
    )

    display_report(report)

    # Give user available actions
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


# Main menu
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