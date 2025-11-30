from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services import repo_structure_with_summary, file_brief
app = FastAPI()

class RepoRequest(BaseModel):
    repo_url: str

class FileBriefRequest(BaseModel):
    repo_url: str
    file_path: List[str]

@app.post("/summary-structure/")
async def repo_structure(request: RepoRequest):

    try:
        structure = repo_structure_with_summary(request.repo_url)
        return {"structure": structure}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/file-brief/")
async def brief_file(request: FileBriefRequest):
    try:
        brief = file_brief(request.repo_url, request.file_path)
        return {"brief": brief}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))