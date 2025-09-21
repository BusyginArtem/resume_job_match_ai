from crewai.tools import tool


@tool("JD Extractor")
def extract_job_description() -> str:
    """Always use this tool to extract uploaded job description and return string"""

    try:
        with open("input/jd.txt", encoding="utf-8") as file:
            jd = file.read()
        return jd

    except Exception as e:
        raise RuntimeError(
            f"An error occurred while reading the job description: {e}"
        ) from e
