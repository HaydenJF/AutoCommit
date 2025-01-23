import os

ENV_FILE = ".env"

def set_repo_path():
    """
    Set the WIP repository path and save it to a shared .env file.
    """
    current_path = os.getenv('WIP_REPO_PATH', os.getcwd())
    print(f"Current WIP repository path: {current_path}")
    
    new_path = input("Enter new repository path (press Enter for current directory): ").strip() or os.getcwd()
    
    # Write the new path to the .env file
    with open(ENV_FILE, "w") as env_file:
        env_file.write(f'WIP_REPO_PATH={new_path}\n')

    print(f"WIP repository path set to: {new_path}")
    print(f"Saved to {ENV_FILE}. Other scripts should read this file for updates.")

if __name__ == "__main__":
    set_repo_path()
