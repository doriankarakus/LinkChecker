import linkchecker
import time


def main():

    # Define the filenames and foldername
    filename = "app_data.json"
    filename_done = "app_data_done.json"
    filename_updated = "app_data_updated.json"
    foldername = "Superdump"

    # Import all the app objects from the file
    imported_apps = linkchecker.import_apps_from_file(filename)
    linkchecker.clear_done(filename_done)

    for app in imported_apps:
        linkchecker.clear_folder(foldername)
        old_version = app.version
        old_hash = app.hash_value
        # Download the installer with a timeout of 50 seconds per app
        file_path = linkchecker.run_with_timeout(
            linkchecker.download_installer_wrapper, (app, foldername), 50
        )
        # If the download fails, skip the app
        if file_path == "Failed":
            print(f"Timeout for {app.name}")
            linkchecker.export_app_to_file(app, filename_done)
            continue
        # Update the app's version and date checked
        linkchecker.update_app_version_and_date(file_path, app)
        linkchecker.export_app_to_file(app, filename_done)
        # Check if the version or hash has changed and export the app to the updated file
        if old_version != app.version or old_hash != app.hash_value:
            print(f"Version has changed from {old_version} to {app.version}")
            print(f"Hash has changed from {old_hash} to {app.hash_value}")
            linkchecker.export_app_to_file(app, filename_updated)

    # Return the current apps to the imports file
    linkchecker.return_curr(filename, filename_done)

    # Print the imported apps' attributes to verify
    print("Imported App Details:")
    for idx, imported_app in enumerate(imported_apps, start=1):
        print(f"App {idx}:")
        print(f"  URL: {imported_app.url}")
        print(f"  Name: {imported_app.name}")
        print(f"  Version: {imported_app.version}")
        print(f"  Hash: {imported_app.hash_value}")
        print(f"  Checked Date: {imported_app.date_checked}")

    # Sleep for 30 seconds then run the main function again
    time.sleep(30)
    main()


if __name__ == "__main__":
    main()
