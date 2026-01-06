"""
Track what files/directories are staged

Store file_path → blob_hash

Clear index after save_state
"""
from typing import Dict
import os
import json
from core.objects import FileContent 

class Index:
    def __init__(self, index_file: str, objects_dir: str):
        self.index_file = index_file
        self.objects_dir = objects_dir
        self.entries: Dict[str, str] = {}  # file_path -> blob_hash
        self.load()
       

    def load(self):
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    self.entries = json.load(f)
            except json.JSONDecodeError:
                self.entries = {}
        else:
            self.entries = {}

    
    def save(self):
        # save current staged files to index file
        with open(self.index_file, 'w') as f:
            json.dump(self.entries, f, indent=4)


    def add_file(self, file_path):
        # add a single file to the index (stage it)

        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} does not exist.")
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        file_content = FileContent(data)
        file_content_hash = file_content.store(self.objects_dir)

        self.entries[file_path] = file_content_hash
        self.save()

        print(f"added file: {file_path} -> {file_content_hash}")


    def add_dir(self, dir_path):
        # add all files in a directory (recursively) to the index (stage them)

        if not os.path.isdir(dir_path):
            raise Exception(f"Directory {dir_path} does not exist or is not a directory.")
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.add_file(file_path)

    def list_saved_files(self):
        # list all staged files
        for file_path, file_content_hash in self.entries.items():
            print(f"{file_path} -> {file_content_hash}")
