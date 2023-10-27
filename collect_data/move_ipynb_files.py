import os
import shutil
from pathlib import Path

def move_ipynb_files(source_folder_path, destination_folder_path):
    """
    Move all .ipynb files from the source folder to the destination folder.
    
    :param source_folder_path: The path of the source folder.
    :param destination_folder_path: The path of the destination folder.
    """
    try:
        # Ensure the destination folder exists
        Path(destination_folder_path).mkdir(parents=True, exist_ok=True)

        # Traverse the source folder and its sub-folders
        for root_dir, _, files in os.walk(source_folder_path):
            for file_name in files:
                if file_name.endswith('.ipynb'):
                    source_file_path = os.path.join(root_dir, file_name)
                    destination_file_path = os.path.join(destination_folder_path, file_name)
                    
                    # Move the .ipynb file to the destination folder
                    shutil.move(source_file_path, destination_file_path)
        
        print("Files moved successfully.")
        
    except (FileNotFoundError, PermissionError) as specific_error:
        print(f"Specific error occurred: {specific_error}")
        
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

def main():
    # Get the source and destination folder paths from the user
    source_folder_path = input("Enter the source folder path containing the subfolders and files: ").strip()
    destination_folder_path = input("Enter the destination folder path to move the .ipynb files: ").strip()

    # Call the function to move .ipynb files
    move_ipynb_files(source_folder_path, destination_folder_path)

if __name__ == "__main__":
    main()
