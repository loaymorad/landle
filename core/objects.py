"""
Generate hash (SHA-256)

Save objects to .landle/objects/

Keep immutable history

    Blobs == FileContents: file contents
    Trees: map file/dir names to blob/tree hashes
    Commits == States: history nodes
"""

import hashlib
import os
import time
import json

class FileContent: # Stores immutable content in .landle/objects/
    def __init__(self, data: bytes):
        self.content = data
    
    def store(self, objects_dir: str) -> str:
        # Store the file content as a blob object and return its hash
        
        sha = hashlib.sha256(self.content).hexdigest()

        object_path = os.path.join(objects_dir, sha)

        if not os.path.exists(object_path):
            with open(object_path, 'wb') as f:
                f.write(self.content)

        return sha

# ####### ###########

class Tree:
    """Tree: maps file/dir names to blob/tree hashes"""
    
    def __init__(self):
        self.entries = {
            # name: (type, hash)
            # value: ("blob" or "tree", hash)
        }
    
    def store(self, objects_dir: str) -> str:
        # store the directory as a tree object and return its hash
        
        json_data = json.dumps(self.entries, sort_keys=True).encode()
        
        sha = hashlib.sha256(json_data).hexdigest()

        object_path = os.path.join(objects_dir, sha)
        if not os.path.exists(object_path):
            with open(object_path, 'wb') as f:
                f.write(json_data)

        return sha

# ####### ###########

class State:
    """State: points to a tree and parent commit(s)"""
    def __init__(self, tree_hash: str, parent_hash: str = None, message: str = ""):
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash
        self.message = message
        self.timestamp = int(time.time())
    
    def store(self, objects_dir: str) -> str:
        # store the state object and return its hash
        
        state_data = {
            "tree": self.tree_hash,
            "parent": self.parent_hash,
            "message": self.message,
            "timestamp": self.timestamp
        }
        
        json_data = json.dumps(state_data, sort_keys=True).encode()
        
        sha = hashlib.sha256(json_data).hexdigest()

        object_path = os.path.join(objects_dir, sha)
        if not os.path.exists(object_path):
            with open(object_path, 'wb') as f:
                f.write(json_data)
        
        return sha