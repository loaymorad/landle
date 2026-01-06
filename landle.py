#!/usr/bin/env python3
# This tells the OS: “Use Python to run this file.”
"""
add in ~/.bashrc or ~/.zshrc
"""

import sys, os

from core.repo import Repo
from core.index import Index
from core.state_manager import StateManager

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: landle.py <command> [<args>]")
        print("Commands: init, add, save, history")
        return
    
    command = args[0]
    manager = StateManager()

    # -------- INIT --------
    if command in ["init"]:
        manager.repo.init_repo()
        return
    
    # -------- ADD --------
    if command in ["add", "+"]:
        if len(args) < 2:
            print("Usage: landle add file|dir <path>")
            return
        
        type_ = args[1]
        paths = args[2:]

        if type_ in ["file", "f"]:
            for path in paths:
                manager.index.add_file(path)
        elif type_ in ["dir", "d"]:
            for path in paths:
                manager.index.add_dir(path)
        else:
            print("Unknown add type. Use 'file' or 'dir'.")
        return
    
    # -------- SAVE STATE --------
    if command in ["save", "s"]:
        if len(args) < 2:
            print("Usage: landle save state \"message\"")
            return
        
        message = " ".join(args[2:])
        manager.save_state(message)
        return
    
    # -------- SHOW HISTORY --------
    if command in ["show", ">"]:
        if len(args) < 2 or args[1] != "states":
            print("Usage: landle show states")
            return
        
        manager.show_history()
        return
    
    # -------- CHANGE STATE --------
    if command in ["state", "s"]:
        if len(args) < 2:
            print("Usage: landle state <state_hash>")
            return
        
        state_hash = args[1]
        manager.change_state(state_hash)
        return
    
    print("Manual:")
    print("[+] landle.py init")
    print("[+] landle.py add file|dir <path>")
    print("[+] landle.py save state \"message\"")
    print("[+] landle.py show states")

    print("Shortcuts:")
    print("[+] landle.py + file|dir <path>")
    print("[+] landle.py s \"message\"")
    print("[+] landle.py > states")


if __name__ == "__main__":
    main()