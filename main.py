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

    # Export the app object to a file
    # export_app_to_file(app, filename)

    # Import all the app objects from the file
    imported_apps = linkchecker.import_apps_from_file(filename)

    for app in imported_apps:
        file_path = linkchecker.download_installer(app)
        old_version = app.version
        linkchecker.update_app_version_and_date(file_path, app)
        linkchecker.export_app_to_file(app, "app_data_done.json")
        if old_version != app.version:
            print(f"Version has changed from {old_version} to {app.version}")
            linkchecker.export_app_to_file(app, "app_data_updated.json")

    linkchecker.return_curr("app_data.json", "app_data_done.json")

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
    main()
