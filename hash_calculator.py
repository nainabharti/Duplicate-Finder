import hashlib


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