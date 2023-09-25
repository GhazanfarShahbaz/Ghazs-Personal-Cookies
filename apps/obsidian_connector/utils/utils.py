from os import getenv

from typing import Dict, List


from obsidian_wrapper.obsidian_vault import ObsidianVault, VaultTree
from obsidian_wrapper.obsidian_markdown_file import ObsidianMarkdownFile

VAULT: ObsidianVault = ObsidianVault(getenv("PATH_TO_OBSIDIAN_VAULT"))


def reload_vault():
    global VAULT
    VAULT.reload_vault()


def get_vault_files() -> List[str]:
    global VAULT
    markdown_files: Dict[str, ObsidianMarkdownFile] = VAULT.markdown_files

    return list(markdown_files.keys())


def get_vault_file_contents_by_name(file_name: str) -> str:
    global VAULT
    markdown_files: Dict[str, ObsidianMarkdownFile] = VAULT.markdown_files

    if not file_name in markdown_files:
        raise KeyError("File was not found in obsidian vault")

    markdown_file: ObsidianMarkdownFile = markdown_files[file_name]
    contents: str = ""

    with open(markdown_file.file_path, "r", encoding="UTF-8") as current_file:
        for line in current_file:
            contents += line

    return contents

def get_file_contents_by_name_detailed(file_name: str) -> str:
    global VAULT 
    
    markdown_files: Dict[str, ObsidianMarkdownFile] = VAULT.markdown_files
    
    if not file_name in markdown_files:
        raise KeyError("File was not found in obsidian vault")

    markdown_file: ObsidianMarkdownFile = markdown_files[file_name]

    return markdown_file.get_file_contents(as_dict=True)


def get_folder_contents(folder_name: str) -> Dict[str, str]:
    global VAULT 
    data:  Tuple[str, VaultTree, int] = VAULT.get_folder(folder_path=folder_name)
    
    # Contents are only only one level down
    current_folder: Dict[str, str] = {
        "folder_name":data [0],
        "contents": {},
        "size": data[2]
    }
    
    for object_name, value in data[1].items():
        content_type: str = ""
        
        if isinstance(value, dict):
            content_type = "folder"
        else:
            content_type = "file"    
            
        current_folder["contents"][object_name] = content_type            
    
    return current_folder

    
    