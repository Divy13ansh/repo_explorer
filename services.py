from gh import get_repo_structure, get_file_content, get_repo_dict_structure
from llms import summarize_file_content

def repo_structure_with_summary(repo_url):
    """Get the repository structure along with summaries for each file."""
    structure = get_repo_dict_structure(repo_url)
    summarized_structure = {}
    for file_path in structure:
        content = get_file_content(repo_url, file_path)
        summary = summarize_file_content(content)
        summarized_structure[file_path] = summary
    return summarized_structure