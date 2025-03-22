Link Checker Project

This project is designed to check and verify links to various software applications by downloading their installers, calculating file hashes, and monitoring version changes. The project supports automatic iterations and will notify you when the version or hash of an application has changed.

Features:
Download installers from specified URLs.
Verify and update application versions and hash values.
Automatically retry download operations with a timeout.
Store application information in JSON files.
Log changes of versions or hashes.
Regularly refresh and repeat operations.

Prerequisites:
Python 3.x

Required Python packages:
requests
pywin32
multiprocessing
shutil
re
json
datetime
os
hashlib

Installation:
Clone the repository:

git clone <repository-url>
cd <repository-directory>
Install the required packages:

pip install -r requirements.txt

Usage:
Create a JSON file named app_data.json with the initial app details. Example structure:

[
    {
        "url": "http://example.com/app1.exe",
        "name": "App1",
        "version": "1.0.0",
        "hash_value": "abc123",
        "date_checked": "2023-01-01 00:00:00"
    }
]

Run the project:

python main.py
The script will automatically check for updates and report any changes in application versions or hash values.

Files:
linkchecker.py: Contains functions to download installers, calculate file hashes, update application details, and manage JSON files.
main.py: Initializes the process and manages iterations, calling linkchecker functions.

Functionality:
Create & Export App: Create App objects and export them to JSON files.
Download & Save Installer: Download application installers and save them locally.
Update App Info: Retrieve version and hash information for applications.
Timeout Management: Retry downloads with a maximum of three attempts.
JSON File Management: Import and export application information for future runs.

Licensing:
This project is not currently licensed. If you wish to choose a license, consider options like MIT, Apache 2.0, GPL, etc.

Contributing:
Contributions are not welcome at this time.

Contact:
For more information or questions, please contact [dorianblackbird@gmail.com].