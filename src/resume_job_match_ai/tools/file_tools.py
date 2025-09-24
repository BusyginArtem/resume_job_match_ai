from crewai.tools import tool


@tool("JD Extractor")
def extract_job_description(jd_path: str) -> str:
    """Always use this tool to extract uploaded job description and return string"""

    try:
        with open(jd_path, encoding="utf-8") as file:
            jd = file.read()
        return jd

    except Exception as e:
        raise RuntimeError(
            f"An error occurred while reading the job description: {e}"
        ) from e
