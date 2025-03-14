import json
import os
import requests
import win32api
from datetime import datetime
import hashlib


class App:
    def __init__(self, url, name, version, hash_value, date_checked):
        self.url = url
        self.name = name
        self.version = version
        self.hash_value = hash_value
        self.date_checked = date_checked


def create_app(url, name, version, hash_value, date_checked):
    return App(url, name, version, hash_value, date_checked)


def export_app_to_file(app, filename):
    # Check if the file already exists
    if os.path.exists(filename):
        # Read the existing data
        with open(filename, "r") as file:
            app_list = json.load(file)
    else:
        app_list = []

    # Add the new app data
    app_data = {
        "url": app.url,
        "name": app.name,
        "version": app.version,
        "hash_value": app.hash_value,
        "date_checked": app.date_checked,
    }
    app_list.append(app_data)

    # Write the updated list back to the file
    with open(filename, "w") as file:
        json.dump(app_list, file, indent=4)


def import_apps_from_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            app_list = json.load(file)
        return [
            App(
                app["url"],
                app["name"],
                app["version"],
                app["hash_value"],
                app["date_checked"],
            )
            for app in app_list
        ]
    else:
        return print("File does not exist")


# FIX THIS. The file path is create by combining the file name and the folder name. The folder name is not passed as a parameter
# Easy fix. Make the folder name based on the file name and have it delete and recreate the folder each time.
# Once in folder search folder for any files and whatever is found is the file path that is passed down into update function
# fixed issue but keeping for documentation


def download_installer(app, folder_name="Superdump"):
    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Get the file name from the URL
    file_name = os.path.basename(app.url)

    # Full path for where the file will be saved
    file_path = os.path.join(folder_name, file_name)

    # Download the installer
    try:
        response = requests.get(app.url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded {file_name} to {file_path}")
        return os.path.abspath(file_path)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the installer: {e}")


def update_app_version_and_date(file_path, app):
    try:

        # Get file version info
        print(file_path)
        info = win32api.GetFileVersionInfo(file_path, "\\")

        # Extract version numbers
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"

        try:
            # Update the App object with the new version and date
            app.version = version
            app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.hash_value = get_file_hash(file_path)
        except:
            print(f"Error updating app version and date: {e}")

        print(f"Updated App Version: {app.version}")
        print(f"Updated Date Checked: {app.date_checked}")
        print(f"Updated Hash Checked: {app.hash_value}")
        # Delete the file after processing
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

    except Exception as e:
        print(f"Error updating app object: {e}")


def get_file_hash(file_path, hash_function="sha256"):
    # Create a hash object
    hash_obj = hashlib.new(hash_function)

    # Open the file in binary mode and read in chunks
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)

    # Return the hex digest of the hash
    return hash_obj.hexdigest()


def return_curr(app_data_path, app_data_done_path):
    # Read contents from app_data_done.json
    with open(app_data_done_path, "r") as done_file:
        done_data = json.load(done_file)

    # Write contents to app_data.json
    with open(app_data_path, "w") as app_file:
        json.dump(done_data, app_file, indent=4)

    # Clear the contents of app_data_done.json
    with open(app_data_done_path, "w") as file:
        file.write("[]")
