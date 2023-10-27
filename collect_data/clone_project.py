import os
import git
from git import Repo
import pandas as pd

def clone_repositories(repository_urls, max_repositories_to_clone, output_directory):
    """
    Clone repositories from a list of URLs to a specified output directory.
    
    :param repository_urls: List of repository URLs to clone.
    :param max_repositories_to_clone: Maximum number of repositories to clone.
    :param output_directory: The directory where cloned repositories will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Counter for cloned repositories
    cloned_count = 0

    for repo_url in repository_urls:
        if cloned_count >= max_repositories_to_clone:
            break

        # Extract the repository name from the URL
        repo_name = repo_url.split('/')[-1].split('.git')[0]
        repo_output_path = os.path.join(output_directory, repo_name)

        # Skip if the repository is already cloned
        if os.path.exists(repo_output_path):
            continue

        try:
            # Clone the repository
            Repo.clone_from(repo_url, repo_output_path)
            cloned_count += 1
        except git.exc.GitCommandError:
            print(f"Failed to clone repository: {repo_url}")
            continue

def main():
    # Load repository URLs from CSV file
    csv_filepath = 'nbcontents.csv'
    dataframe = pd.read_csv(csv_filepath)

    # Extract unique repository URLs
    repository_urls = list(set(dataframe['repo'].tolist()))

    # Define the maximum number of repositories to clone
    max_repositories_to_clone = 200

    # Get the output directory path from the user
    output_directory = input("Enter the output directory path to save the cloned repositories: ").strip()

    # Start cloning repositories
    clone_repositories(repository_urls, max_repositories_to_clone, output_directory)
    print(f"Cloned up to {max_repositories_to_clone} repositories successfully into '{output_directory}'.")

if __name__ == "__main__":
    main()
