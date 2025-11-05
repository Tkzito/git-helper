# Git Helper

`git-helper` is a Python script that provides a simple command-line interface to perform common Git operations. It simplifies tasks like cloning repositories, checking status, creating commits, creating tags, and pushing changes.

## Features

-   **Clone Repositories**: Clone a new repository from a URL.
-   **Work with Local Repositories**: Easily manage your local git repositories.
-   **Git Status**: Show the working tree status.
-   **Remote Access Check**: Verify connection to the remote repository.
-   **Create Commits**: Add and commit all changes in the working directory.
-   **Create Tags**: Create annotated tags.
-   **Push Changes**: Push commits and/or tags to the remote repository.

## Usage

1.  Run the script:
    ```bash
    python3 git-helper.py
    ```

2.  The script will present a menu with options to clone a repository or work with an existing local repository.

3.  If you choose to work with a local repository, the script will list all git repositories found in the base directory (`~/Documentos/Git` by default).

4.  After selecting a repository, you can choose from a list of actions to perform.

## Cross-Platform Compatibility

The script is written in Python and uses the `pathlib` module, which handles path operations in a cross-platform manner. This allows the script to run on both Windows and Linux systems without modification.
