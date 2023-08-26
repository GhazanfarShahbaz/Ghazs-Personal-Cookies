""" 
File Name: build_knowledge_graph.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/01/2023
Description: Provides functionality to extract information from obsidian directory and
then create a knowledge graph json file.
"""

from typing import Dict, Set, Tuple, List
from os import listdir, getenv
from os.path import isdir
from json import dump
from re import findall

path_to_vault: str = getenv("PATH_TO_OBSIDIAN_VAULT")
folders_to_ignore: Set[str] = {".obsidian", ".git"}
files_to_ignore: Set[str] = {".DS_Store", "Budgeting Sheet.md", "Todo.md"}


def get_all_files(
    md_files: Dict[str, str], other_files: Set[Tuple[str, str]], path: str
) -> None:
    """
    Recursively scans a directory for Markdown files and other files.

    Args:
        md_files: A dictionary to store the found Markdown files, where the key is the
        file path and the value is the file name without the extension.
        other_files: A set to store other files found, where each entry is a tuple containing
        the file path and the file name.
        path: The path to the directory to be scanned.

    Returns:
        None
    """

    for file_name in listdir(path):
        if file_name in files_to_ignore or file_name in folders_to_ignore:
            continue

        current_path: str = f"{path}/{file_name}"

        if isdir(current_path):
            get_all_files(md_files, other_files, current_path)
        elif current_path.endswith(".md"):
            md_files[current_path] = file_name[: len(file_name) - 3]
        else:
            # NOTE: remove .png, change this later to remove any extension
            other_files.add((current_path, file_name))


def extract_link_from_file(path_to_file: str, markdown_files) -> Set[str]:
    """
    Extracts links from a Markdown file. The markdown file is assumed to follow the
    obsidian markdown structure.

    Args:
        path_to_file: The path to the Markdown file.

    Returns:
        A set of extracted links.
    """
    links: Set[str] = set()

    with open(path_to_file, "r", encoding="UTF-8") as md_file:
        for line in md_file:
            matches: List[str] = findall(r"\[\[(.*?)\]\]", line)

            for match in matches:
                actual_link: str = ""
                previous_character: str = ""

                for character in match:
                    # "Ghaz's Notes#Table Of Contents | Contents" -> "Ghaz's Notes"
                    if (
                        previous_character != "\\"
                        and character == "#"
                        or character == "|"
                    ):
                        break

                    actual_link += character
                    previous_character = character

                actual_link = actual_link.strip()
                # TODO: LOOK FOR A BETTER SOLUTION
                markdown_exists: bool = False

                for path, file_name in markdown_files.items():
                    if file_name == actual_link:
                        markdown_exists = True
                        break

                if markdown_exists:
                    links.add(actual_link)

    return links


def create_and_save_graph(save_path: str) -> None:
    """
    Creates and saves a force-directed graph based on the markdown files in the given directory.

    Args:
        save_path: The path to where the graph file will be saved.

    Returns:
        None
    """

    force_graph_data: dict[str, list] = {"nodes": [], "links": []}

    def add_to_force_graph(file_data, index=0):
        if isinstance(file_data, dict):
            file_data = file_data.items()

        for full_path, file_name in file_data:  # pylint: disable=unused-variable
            current_object = {"id": file_name, "name": file_name, "val": index}

            force_graph_data["nodes"].append(current_object)
            index += 1

        return index

    md_files: Dict[str, str] = {}
    other_files: Set[Tuple[str, str]] = set()

    # populate md_file and other_files
    get_all_files(md_files, other_files, path_to_vault)
    graph: List[Dict[str, str]] = []

    for path, file_name in md_files.items():
        links: Set[str] = extract_link_from_file(path, md_files)

        for connection_to in links:
            graph.append({"source": file_name, "target": connection_to})

    index: int = add_to_force_graph(md_files)
    add_to_force_graph(other_files, index)

    for data in graph:
        force_graph_data["links"].append(data)

    with open(save_path, "w", encoding="utf-8") as output_file:
        dump(force_graph_data, output_file)
