# Landle

![Logo](https://raw.githubusercontent.com/loay/landle/main/landle.png)

Landle is a lightweight, Python-based version control system designed to help you manage your project's history with ease. It provides essential version control features like initializing repositories, staging files, saving states (commits), and navigating through history.

## Features

-   **Initialize Repository**: Create a new Landle repository in your project.
-   **Stage Changes**: Add files and directories to the staging area (index).
-   **Save State**: Commit your staged changes with a message to save a snapshot of your project.
-   **View History**: Browse through the list of saved states.
-   **Checkout State**: Restore your project to any previous state.

## Installation

Landle is a Python script. Ensure you have Python 3 installed on your system.

You can add an alias to your shell configuration file (`~/.bashrc` or `~/.zshrc`) for easier access:

```bash
alias landle="python3 /path/to/landle/landle.py"
```

## Usage

Run `landle.py` (or your `landle` alias) followed by a command.

### Initialize a Repository

Start tracking a project by initializing a Landle repository in the root directory.

```bash
landle init
```

### Add Files

Stage files or directories to be included in the next save.

```bash
# Add a single file
landle add file path/to/file.txt
# Shortcut
landle + f path/to/file.txt

# Add a directory (recursive)
landle add dir path/to/directory
# Shortcut
landle + d path/to/directory
```

### Save State

Save the current state of staged files with a message.

```bash
landle save state "Initial commit"
# Shortcut
landle s "Initial commit"
```

### View History

Show the history of saved states.

```bash
landle show states
# Shortcut
landle > states
```

### Restore State

Revert your project to a specific state using its hash.

```bash
landle state <state_hash>
```

## How it Works

Landle operates by taking snapshots of your project's state. When you `add` a file, Landle reads its content and stores it securely. When you `save` a state, Landle creates a record of exactly how your project looks at that moment, including which files are present and their contents. This allows you to travel back in time to any saved state.

## Internal Concepts

Landle uses a structure similar to Git but with some simplified terminology:

-   **.landle/**: The directory where all repository metadata and objects are stored.
-   **Objects**:
    -   **FileContent**: Stores the raw contents of your files. (These are immutable blobs).
    -   **Trees**: Represent directories and map filenames to their corresponding FileContent or other Trees.
    -   **States (Commits)**: Snapshots of the project at a specific point in time. Each state points to a root Tree and a parent State, forming a history chain.
-   **Index**: The staging area that tracks which files are ready to be saved in the next state.
-   **HEAD**: A pointer that keeps track of your current position in the history (usually pointing to the latest state on the main branch).