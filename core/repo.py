"""
Initialize repo
Keep track of HEAD
Manage refs/branches
Provide paths for objects, index, HEAD, refs
"""

"""
Absolute path like: /home/user/project
Relative path like: ./project
"""


"""
Concepts Again:
.landle/              # Repository metadata
    objects/          # Stored objects (FileContent (Blobs), Directories (Tree), states (Commits))
    refs/heads/       # Branch references
    HEAD              # Current branch reference
    index             # Staging area

    
HEAD → refs/heads/main → abc123 (latest commit)
HEAD is a pointer, not the commit itself.

Usually, HEAD points to a branch (like refs/heads/main).

That branch file (refs/heads/main) points to the latest commit hash.
"""


import os

class Repo:
    def __init__(self, path="."):
        self.working_dir = os.path.abspath(path) # current project directory
        
        # .landle folder path
        self.landle_folder = os.path.join(self.working_dir, ".landle")
        
        ## .landle/
        self.objects_dir = os.path.join(self.landle_folder, "objects")
        self.refs_dir = os.path.join(self.landle_folder, "refs", "heads")

        self.index_file = os.path.join(self.landle_folder, "index")
        self.head_file = os.path.join(self.landle_folder, "HEAD")

    
    def init_repo(self):
        
        if os.path.exists(self.landle_folder):
            print("Repository already initialized.")
            return
        
        os.makedirs(self.objects_dir, exist_ok=True)
        os.makedirs(self.refs_dir, exist_ok=True)

        # Initialize HEAD to point to main branch
        with open(self.head_file, 'w') as f:
            f.write("ref: refs/heads/main\n")

        # Create main branch ref (empty initially)
        main_ref = os.path.join(self.refs_dir, "main")
        open(main_ref, 'w').close()

        # Initialize empty index
        open(self.index_file, 'w').close()

        print(f"Initialized empty Landle repository in {self.landle_folder}")


    def get_head(self):
        
        if not os.path.exists(self.head_file):
            raise Exception("HEAD file does not exist. Is this a Landle repository?")
        

        with open(self.head_file, 'r') as f:
            ref_line = f.read().strip()
        
        if ref_line.startswith("ref: "):
            ref_line = ref_line[5:]
        
        return ref_line

        """
        read() → reads entire file as a single string
        readline() → reads one line at a time (returns string with \n)
        readlines() → reads all lines into a list (each element is a line including \n)
        """


    def update_head_latest_state(self, state_hash):
        # “save a state in the main branch”
        
        head_ref = self.get_head()
        branch_file = os.path.join(self.landle_folder, head_ref)

        with open(branch_file, 'w') as file:
            file.write(state_hash + "\n")

