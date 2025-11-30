import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "my-app"
}

def dir_structure(owner, repo, path=""):
    """
    Recursively fetch the directory structure of a GitHub repository.
    Returns a nested list/dict representing files and folders.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    
    structure = []
    for item in data:
        if item["type"] == "dir":
            sub_structure = dir_structure(owner, repo, path=item["path"])
            structure.append({item["name"]: sub_structure})
        else:
            structure.append(item["name"])
    return structure

def parse_url(repo_url):
    """Extract owner and repo name from GitHub URL."""
    try:
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1].replace('.git', '')
        return owner, repo
    except IndexError:
        raise ValueError("Invalid GitHub repository URL.")
    
def tree_structure_str(structure, prefix=""):
    """
    Recursively build a tree-like string from a nested structure.
    """
    lines = []
    for i, item in enumerate(structure):
        connector = "└── " if i == len(structure) - 1 else "├── "
        
        if isinstance(item, dict):
            for folder, contents in item.items():
                lines.append(f"{prefix}{connector}{folder}/")
                extension = "    " if i == len(structure) - 1 else "│   "
                lines.append(tree_structure_str(contents, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{item}")
    
    return "\n".join(lines)

def get_repo_structure(repo_url):
    """Get the directory structure from a GitHub repository URL."""
    owner, repo = parse_url(repo_url)
    structure = dir_structure(owner, repo)
    structure = tree_structure_str(structure)
    return structure

def get_repo_dict_structure(repo_url):
    """Get the directory structure from a GitHub repository URL."""
    owner, repo = parse_url(repo_url)
    structure = dir_structure(owner, repo)
    paths = extract_paths(structure)
    # return [structure, paths]
    return paths

def get_file_content(repo_url, file_path):
    """Fetch the content of a specific file in a GitHub repository."""
    owner, repo = parse_url(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()

    if "content" in data:
        content = base64.b64decode(data["content"]).decode('utf-8')
        return content
    else:
        raise ValueError("File content not found.")

def extract_paths(tree, prefix=""):
    """
    Recursively convert nested list/dict structure into full file paths.
    """
    paths = []

    for item in tree:
        if isinstance(item, str):
            # It's a file
            paths.append(prefix + item)

        elif isinstance(item, dict):
            # It's a folder
            for folder, contents in item.items():
                folder_path = prefix + folder + "/"
                paths.extend(extract_paths(contents, folder_path))

    return paths



# print(get_repo_structure('https://github.com/Divy13ansh/discord-bot-for-github'))
# print(get_repo_dict_structure('https://github.com/CyrilBaah/Superheroes-API'))