import json
import multiprocessing
import os
import requests
import win32api
from datetime import datetime
import hashlib
import shutil
import re


# Define the App class
class App:
    def __init__(self, url, name, version, hash_value, date_checked):
        self.url = url
        self.name = name
        self.version = version
        self.hash_value = hash_value
        self.date_checked = date_checked


# Creates an App object
def create_app(url, name, version, hash_value, date_checked):
    return App(url, name, version, hash_value, date_checked)


# Exports the app object to a file
def export_app_to_file(app, filename):
    # Check if the file already exists
    if os.path.exists(filename):
        # Read the existing data
        with open(filename, "r") as file:
            app_list = json.load(file)

    # If the file doesn't exist, create an empty list
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
    # Append the new app data to the list
    app_list.append(app_data)

    # Write the updated list back to the file
    with open(filename, "w") as file:
        json.dump(app_list, file, indent=4)


# Imports the app objects from a file
def import_apps_from_file(filename):
    # Check if the file exists
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
        return print(f"File does not exist: {filename}")


# Downloads the installer from the app's URL
def download_installer(app, folder_name):
    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Download the installer
    try:
        return os.path.abspath(download_and_find_file(app, folder_name))

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the installer: {e}")


def save_downloaded_file(response, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return file_path


def download_and_find_file(app, folder_path):
    # Download the file
    response = requests.get(app.url, stream=True)
    response.raise_for_status()

    # Define a file name based on the URL or a fixed name
    file_name = app.url.split("/")[-1]

    # Save the downloaded file to the specified folder
    saved_file_path = save_downloaded_file(response, folder_path, file_name)

    # Confirm the file was saved
    if os.path.exists(saved_file_path):
        print(f"Downloaded and saved file: {saved_file_path}")
    else:
        print("Failed to save the file.")

    return saved_file_path


def update_app_version_and_date(file_path, app):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    if "NameVersion" in app.name:
        try:
            digits = re.findall(r"\d+", file_path)

            # Combine all found digits into a string
            version = "".join(digits)

            # Set the app.version to the extracted numerical string
            app.version = version
            app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.hash_value = get_file_hash(file_path)

        except Exception as e:
            print(f"Error updating app version and date: {e}")
    elif file_path.endswith(".exe"):
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
                print(f"Error updating exe app version and date: {e}")

        except Exception as e:
            print(f"Error updating exe app object: {e}")
    elif file_path.endswith(".msi") or file_path.endswith(".msix"):
        try:
            # Get file version info
            print(file_path)
            version = "MSI"
            try:
                # Update the App object with the new version and date
                app.version = version
                app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app.hash_value = get_file_hash(file_path)
            except:
                print(f"Error updating msi or msix app version and date: {e}")

        except Exception as e:
            print(f"Error updating msi or msix app object: {e}")
    elif file_path.endswith(".zip"):
        try:
            # Extract the zip file
            extract_folder = os.path.splitext(file_path)[0]  # Remove .zip extension
            os.makedirs(extract_folder, exist_ok=True)
            shutil.unpack_archive(file_path, extract_folder)
            print(f"Extracted {file_path} to {extract_folder}")

            # Check if app.version is not "ZIP"
            if app.version != "ZIP":
                target_file_path = os.path.join(extract_folder, app.version)
                if os.path.exists(target_file_path):
                    # Compute the hash of the target file
                    app.hash_value = get_file_hash(target_file_path)
                    app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    print(f"Target file not found: {target_file_path}")
            else:
                # Default behavior for ZIP
                app.version = "ZIP"
                app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app.hash_value = get_file_hash(file_path)

        except Exception as e:
            print(f"Error processing zip file: {e}")
    elif file_path.endswith(".dmg"):
        try:
            # Get file version info
            print(file_path)
            version = "DMG"
            try:
                # Update the App object with the new version and date
                app.version = version
                app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app.hash_value = get_file_hash(file_path)
            except:
                print(f"Error updating dmg app version and date: {e}")

        except Exception as e:
            print(f"Error updating dmg app object: {e}")
    elif file_path.endswith(".pkg"):
        try:
            # Get file version info
            print(file_path)
            version = "PKG"
            try:
                # Update the App object with the new version and date
                app.version = version
                app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                app.hash_value = get_file_hash(file_path)
            except:
                print(f"Error updating pkg app version and date: {e}")

        except Exception as e:
            print(f"Error updating pkg app object: {e}")
    else:
        try:
            # Get file version info
            print(file_path)
            info = win32api.GetFileVersionInfo(file_path, "\\")

            # Extract version numbers
            ms = info["FileVersionMS"]
            ls = info["FileVersionLS"]
            version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        except:
            print("File type may not supported")
            version = "Not Supported"
            app.version = version
            print(f"Error updating app version and date: {e}")
        try:
            # Update the App object
            app.date_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.hash_value = get_file_hash(file_path)
        except:
            print("File hash error")
            print(f"Error updating app version and date: {e}")

    # Print the updated app details
    print(f"Current App Version: {app.version}")
    print(f"Current Date Checked: {app.date_checked}")
    print(f"Current Hash Checked: {app.hash_value}")
    # Delete the file after processing
    os.remove(file_path)
    print(f"Deleted file: {file_path}")


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
    clear_done(app_data_done_path)


def clear_done(app_data_done_path):
    # Clear the contents of app_data_done.json
    with open(app_data_done_path, "w") as file:
        file.write("[]")


def clear_folder(folder_path):
    # List all files and directories in the specified folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if it's a file or directory and delete accordingly
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # Remove files or symlinks
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directories


# Time out wrapper for download_installer
def download_installer_wrapper(app, folder_name, queue):
    try:
        result = download_installer(app, folder_name)
        queue.put(result)
    except Exception as e:
        queue.put(e)


# Time out function
def run_with_timeout(func, args, timeout):
    trys = 0
    while trys < 3:
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=func, args=(*args, queue))
        process.start()
        process.join(timeout)

        if process.is_alive():
            process.terminate()
            process.join()
            print(f"{func.__name__} timed out and was restarted.")
            trys += 1
            if trys == 3:
                print(f"{func.__name__} failed after 3 attempts.")
                return "Failed"
        else:
            result = queue.get()
            if isinstance(result, Exception):
                print(f"An error occurred: {result}")
            else:
                print(f"{func.__name__} completed successfully.")
                return result
