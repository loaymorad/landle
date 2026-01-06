"""
Combine index + objects + repo

Manage commits & history

Restore files from state
"""

from core.objects import FileContent, Tree, State
from core.repo import Repo
from core.index import Index
import os
import json

class StateManager:
    def __init__(self, repo_path="."):
        self.repo = Repo(repo_path)

        self.index = Index(self.repo.index_file, self.repo.objects_dir)
    
    def save_state(self, message: str):
        if not self.index.entries:
            print("No changes staged. Nothing to commit.")
            return
        
        # 1. Create tree from index (staged files)
        tree = Tree()
        for file_path, file_content_hash in self.index.entries.items():
            tree.entries[file_path] = ("fileContent", file_content_hash)
        
        tree_hash = tree.store(self.repo.objects_dir)

        # 2. Get parent state hash from HEAD
        head_ref = self.repo.get_head()
        branch_file = os.path.join(self.repo.landle_folder, head_ref)
        parent_hash = None
        if os.path.exists(branch_file):
            with open(branch_file, 'r') as f:
                parent_hash = f.read().strip() or None

        # 3. Create new state
        state = State(tree_hash, parent_hash, message)
        state_hash = state.store(self.repo.objects_dir)

        # 4. Update branch ref to point to new state
        self.repo.update_head_latest_state(state_hash)

        # 5. Clear index
        self.index.entries = {}
        self.index.save()

        print(f"Saved state: {state_hash} with message: '{message}'")


    def show_history(self):
        # Traverse commits from HEAD backwards using parent_hash
        
        head_ref = self.repo.get_head()
        branch_file = os.path.join(self.repo.landle_folder, head_ref)
        if not os.path.exists(branch_file):
            print("No states found.")
            return
        
        state_hash = open(branch_file).read().strip()
        if not state_hash:
            print("No states found.")
            return
        
        print("State History:")
        while state_hash:
            state_path = os.path.join(self.repo.objects_dir, state_hash)
            if not os.path.exists(state_path):
                break
            
            with open(state_path, 'rb') as f:
                state_data = json.loads(f.read().decode())
            
            print(f"State: {state_hash}")
            print(f"  Message: {state_data['message']}")
            print(f"  Timestamp: {state_data['timestamp']}")
            print()
            
            state_hash = state_data.get("parent")

    def change_state(self, state_hash: str):
        # change the state at the given commit hash
        state_path = os.path.join(self.repo.objects_dir, state_hash)
        if not os.path.exists(state_path):
            raise Exception(f"State {state_hash} does not exist.")

        with open(state_path, 'rb') as f:
            state_data = json.loads(f.read().decode())
        
        tree_hash = state_data['tree']
        tree_path = os.path.join(self.repo.objects_dir, tree_hash)
        with open(tree_path, 'rb') as f:
            tree_data = json.loads(f.read().decode())

        for file_path, (obj_type, obj_hash) in tree_data.items():
            if obj_type != "fileContent":
                continue
            
            file_content_path = os.path.join(self.repo.objects_dir, obj_hash)
            with open(file_content_path, 'rb') as bf:
                file_content = bf.read()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as out_f:
                out_f.write(file_content)

        print(f"Changed to state: {state_hash}")
