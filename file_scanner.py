import os


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