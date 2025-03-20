import linkchecker
import time


def main():
    # test
    # Define the parameters
    # checked_date_time = "2025-02-19 15:29:40"
    # name = "Teams"
    # version = "xyyyyy"
    # hash_value = "xxxxxxx"
    # link = "https://staticsint.teams.cdn.office.net/production-windows-x64/1.8.00.2353/Teams_windows_x64.exe"

    # Create the app object
    # app = create_app(link, version, hash_value, checked_date_time)

    # Define the filename
    filename = "app_data.json"
    filename_done = "app_data_done.json"
    filename_updated = "app_data_updated.json"
    foldername = "Superdump"

    # Export the app object to a file
    # export_app_to_file(app, filename)

    # Import all the app objects from the file
    imported_apps = linkchecker.import_apps_from_file(filename)
    linkchecker.clear_done(filename_done)

    for app in imported_apps:
        linkchecker.clear_folder(foldername)
        old_version = app.version
        old_hash = app.hash_value
        file_path = linkchecker.run_with_timeout(
            linkchecker.download_installer_wrapper, (app, foldername), 50
        )
        if file_path == "Failed":
            print(f"Timeout for {app.name}")
            linkchecker.export_app_to_file(app, filename_done)
            continue
        linkchecker.update_app_version_and_date(file_path, app)
        linkchecker.export_app_to_file(app, filename_done)
        if old_version != app.version or old_hash != app.hash_value:
            print(f"Version has changed from {old_version} to {app.version}")
            print(f"Hash has changed from {old_hash} to {app.hash_value}")
            linkchecker.export_app_to_file(app, filename_updated)

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

    time.sleep(30)
    main()


if __name__ == "__main__":
    # testing timeouts
    # linkchecker.run_with_timeout(main(), 40)
    main()
