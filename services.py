from gh import get_repo_structure, get_file_content, get_repo_dict_structure
from llms import summarize_file_content, file_explanation

def repo_structure_with_summary(repo_url):
    """Get the repository structure along with summaries for each file."""
    structure = get_repo_dict_structure(repo_url)
    summarized_structure = {}
    for file_path in structure:
        content = get_file_content(repo_url, file_path)
        summary = summarize_file_content(content)
        summarized_structure[file_path] = summary
    return summarized_structure

def file_brief(repo_url, file_path):
    file_path = list(file_path)
    file_path.append("README.md")
    structure = get_repo_structure(repo_url)
    file_content = ""
    file_content += f"Repository Structure:\n{structure}\n"
    for i in file_path:
        cont = get_file_content(repo_url, i)
        file_content += f"\n\nFile Path: {i}\nContent:\n{cont}"
    
    brief = file_explanation(file_content)
    return brief

# print(file_brief("Divy13ansh/cfox.ai_fastapi", ["config.py", "main.py"]))