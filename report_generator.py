import os
from datetime import datetime


# Convert bytes into readable units
def format_size(size_bytes):

    size = float(size_bytes)

    for unit in ["B", "KB", "MB", "GB", "TB"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


# Generate duplicate report
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
            file_sizes = []

            for file_path in file_list:

                report.append(file_path)

                try:
                    file_size = os.path.getsize(file_path)
                    file_sizes.append(file_size)
                    group_size += file_size

                except OSError:
                    file_sizes.append(None)
                    report.append(
                        f"Warning: Could not get size of {file_path}"
                    )

            total_duplicate_size += group_size

            # Calculate storage recoverable from extra copies
            if file_sizes[0] is not None:
                extra_storage += sum(
                    size for size in file_sizes[1:]
                    if size is not None
                )

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


# Display report
def display_report(report):
    print(report)


# Save report as TXT file
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