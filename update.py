from pathlib import Path
import os,shutil,requests

author = "MisterNoFace"  # Replace with your GitHub username
project = "movieWatcher"  # Replace with your GitHub project name
CURRENT_DIR = Path(__file__).resolve().parent

response = requests.get(f"https://api.github.com/repos/{author}/{project}/commits/main")
if response.status_code != 200:
    print("Failed to check latest commit. Check your internet connection or repository info.")
    quit()
latest_commit = response.json()["sha"]

# Store the last downloaded commit SHA in a file
commit_file = CURRENT_DIR / ".last_commit"
if commit_file.exists():
    with open(commit_file, "r") as f:
        last_commit = f.read().strip()
    if last_commit == latest_commit:
        print("Already up to date. No update needed.")
        import main
        main.main()

response = requests.get(f"https://github.com/{author}/{project}/archive/refs/heads/main.zip")
if response.status_code != 200:
    print("Failed to download the update. Check your internet connection")
    quit()
else:
    with open(CURRENT_DIR/"repo.zip", "wb") as f:
        f.write(response.content)

    shutil.unpack_archive(str(CURRENT_DIR/"repo.zip"), str(CURRENT_DIR))
    print(f"Repository extracted to {CURRENT_DIR}")

    # Find the extracted folder (it will be named like '{project}-main')
    extracted_folder = CURRENT_DIR / f"{project}-main"
    if extracted_folder.exists() and extracted_folder.is_dir():
        for item in extracted_folder.iterdir():
            dest = CURRENT_DIR / item.name
            if dest.exists():
                if dest.is_file():
                    os.remove(dest)
                elif dest.is_dir():
                    shutil.rmtree(dest)
            shutil.move(str(item), str(CURRENT_DIR))
        shutil.rmtree(extracted_folder)
        print(f"Moved files from {extracted_folder} to {CURRENT_DIR}")
    os.remove(CURRENT_DIR/"repo.zip")
import main
main.main()
