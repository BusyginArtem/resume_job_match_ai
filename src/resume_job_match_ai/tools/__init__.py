from crewai_tools import SerperDevTool

from .file_tools import extract_job_description
from .pdf_tools import extract_resume, save_resume_as_pdf

# Register all tools for CrewAI project system
# The keys must match exactly what you use in YAML files
tool_functions = {
    "extract_resume": extract_resume,
    "save_resume_as_pdf": save_resume_as_pdf,
    "extract_job_description": extract_job_description,
    "SerperDevTool": SerperDevTool,
}

# Export tools for direct import
__all__ = [
    "extract_resume",
    "save_resume_as_pdf",
    "extract_job_description",
    "SerperDevTool",
    "tool_functions",
]
