🔍 Duplicate Finder

A Python-based command-line application that helps identify duplicate files in a folder and its subfolders using SHA-256 hashing.

Duplicate Finder scans files, compares their content, generates reports, and allows users to delete duplicate copies after confirmation.

✨ Features

- Recursive Folder Scanning: Scans files in the selected folder and its subfolders.
- Duplicate Detection: Identifies duplicate files using SHA-256 hashing.
- Efficient File Reading: Reads files in chunks instead of loading entire files into memory.
- Progress Tracking: Displays scanning progress.
- Extension Filtering: Scans all files or selected file types such as ".pdf", ".txt", and ".jpg".
- Error Handling: Handles missing files, permission errors, and other file-related exceptions.
- Storage Analysis: Calculates the storage occupied by duplicate files and the potentially recoverable space.
- Report Generation: Generates detailed text reports containing duplicate file information.
- Delete Duplicates: Allows users to delete duplicate copies after confirmation.
- Modular Programming: Organises the application into separate Python modules for better readability and maintainability.

🛠️ Technologies Used

- Python 3
- "os" – File and directory operations
- "hashlib" – SHA-256 hashing
- "datetime" – Report timestamps

No external Python libraries are required.

📁 Project Structure

Duplicate-Finder/
│
├── main.py
├── file_scanner.py
├── hash_calculator.py
├── duplicate_detector.py
├── report_generator.py
│
├── test-files/
│
├── reports/
│
├── README.md
└── .gitignore

Description of Python Files

File| Purpose
"main.py"| Main entry point and menu handling
"file_scanner.py"| Scans folders and collects file paths
"hash_calculator.py"| Calculates SHA-256 hashes
"duplicate_detector.py"| Groups duplicate files and handles deletion
"report_generator.py"| Generates, displays, and saves reports

Other folders:

- "test-files/" – Contains sample files for testing.
- "reports/" – Stores generated text reports.

⚙️ How to Run the Project

1. Clone the Repository

git clone https://github.com/nainabharti/Duplicate-Finder.git

2. Navigate to the Project Folder

cd Duplicate-Finder

3. Run the Application

python main.py

🔄 How It Works

1. The user enters the folder path to scan.
2. The application collects file paths recursively.
3. Each file is read in small chunks.
4. SHA-256 hashes are calculated for the files.
5. Files with matching hashes are grouped as duplicates.
6. A report displays duplicate groups and storage statistics.
7. The user can save the report or choose to delete duplicate copies.

📊 Sample Output

========================================
          DUPLICATE FINDER
========================================

1. Scan a folder
2. Exit

Enter your choice: 1

Enter folder path to scan: test-files

Total files found: 7

Duplicate Files Found!

Duplicate Group 1:
- test-files/file1.txt
- test-files/file2.txt

Duplicate Group 2:
- test-files/sub_test-files/new.pdf
- test-files/sub_test-files/new1.pdf

1. Save report
2. Delete duplicate copies
3. Return to main menu

Note: The sample output is illustrative. Actual results depend on the files being scanned.

🧠 Concepts Learned

This project helped me practise:

- File handling in Python
- Working with files and directories using "os"
- SHA-256 hashing using "hashlib"
- Dictionaries and lists
- Functions and modular programming
- Recursive folder traversal
- Exception handling
- Reading files in chunks
- User input and menu-driven programs
- Generating and saving text reports

⚠️ Important Note

The delete option permanently removes selected duplicate files using Python's "os.remove()" function.

- Review the duplicate file paths before deletion.
- The application keeps the first file in each duplicate group and considers the remaining files as duplicate copies.
- Always keep a backup of important files before using the delete option.

🚀 Future Improvements

- Add a graphical user interface (GUI).
- Support more advanced filtering options.
- Add an option to move duplicates to a backup folder instead of permanently deleting them.
- Improve duplicate detection performance for large directories.

👩‍💻 Author

Naina Bharti

GitHub: "@nainabharti" (https://github.com/nainabharti)

---

⭐ If you find this project useful, consider giving it a star!