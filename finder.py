from os import getcwd, listdir, path

def create_requirements_file(requirements: dict) -> None:
    requirements_file = open("requirements.txt", "w")
    for library, version in requirements.items():
        requirements_file.write(f"{library}=={version}\n")

    requirements_file.close()

def get_requirements_from_file(requirements: dict, file_path: str) -> None:
    try:
        requirements_file = open(file_path, 'r')

        for line in requirements_file:
            line = line.strip()
            library_name, version = line.split("==")

            if library_name in requirements:
                requirements[library_name] = max(requirements[library_name], version)
            else:
                requirements[library_name] = version

        requirements_file.close()
    except:
        None 

def get_requirements() -> dict:
    path: str = getcwd()
    requirements: dict = {}
    

    for content in listdir(path):
        current_path = f"{path}/{content}"
        
        if path.isdir(current_path):
            try:
                for nested_content in listdir(current_path):
                    nested_path = f"{current_path}/{nested_content}"

                    if nested_content == "requirements.txt":
                        get_requirements_from_file(requirements, nested_path)
                        break 
            except:
                continue

    create_requirements_file(requirements)


if __name__ == '__main__':
    get_requirements()