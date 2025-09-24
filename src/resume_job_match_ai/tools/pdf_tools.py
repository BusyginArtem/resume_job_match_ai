import markdown
import pdfkit
from crewai.tools import tool
from pypdf import PdfReader

output_path = "./output/enhanced_resume.pdf"


def setup_pdfkit_windows():
    """
    Download wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html
    Install the Windows installer, then configure the path
    """
    # Configure path to wkhtmltopdf (adjust path as needed)
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    return config


@tool("Resume Extractor")
def extract_resume(resume_path: str) -> str:
    """
    Core function to extract text from PDF resume.
    This can be called directly for testing.
    """
    print(f"Extracting text from resume: {resume_path}")
    try:
        with open(resume_path, "rb") as file:
            reader = PdfReader(file)
            text = ""

            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    print(f"⚠️ No text found on page {i}. It might be scanned.")

        if not text.strip():
            raise RuntimeError(
                "No extractable text found in CV. The PDF may be scanned."
            )

        print(f"Extracted {len(text)} characters from the resume.")
        return text
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting the resume: {e}") from e


@tool("Resume Saver")
def save_resume_as_pdf(markdown_content: str) -> str:
    """
    Core function to convert markdown to PDF.
    This can be called directly for testing.
    """
    try:
        print("Converting markdown to PDF...")
        print(f"Markdown content preview: {markdown_content[:200]}...")

        html = markdown.markdown(markdown_content, extensions=["codehilite", "tables"])

        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
                    line-height: 1.6;
                    color: #333;
                }}
                h1, h2, h3 {{ 
                    color: #2c3e50; 
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }}
                code {{ 
                    background-color: #f4f4f4; 
                    padding: 2px 6px; 
                    border-radius: 3px;
                    font-family: Consolas, monospace;
                }}
                pre {{ 
                    background-color: #f8f9fa; 
                    padding: 15px; 
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin-left: 0;
                    padding-left: 20px;
                    color: #666;
                }}
                ul, ol {{
                    margin: 10px 0;
                    padding-left: 30px;
                }}
                li {{
                    margin: 5px 0;
                }}
                .contact-info {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 20px;
                }}
                .section {{
                    margin: 25px 0;
                }}
                .job-title {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .company {{
                    font-style: italic;
                    color: #7f8c8d;
                }}
                .date-range {{
                    float: right;
                    color: #95a5a6;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        try:
            config = setup_pdfkit_windows()
            pdfkit.from_string(styled_html, output_path, configuration=config)
            success_msg = f"✅ PDF successfully saved to {output_path}"
            print(success_msg)
            return success_msg
        except Exception as e1:
            print(f"Windows config failed: {e1}")
            # Try without config if wkhtmltopdf is in PATH
            try:
                pdfkit.from_string(styled_html, output_path)
                success_msg = f"✅ PDF successfully saved to {output_path}"
                print(success_msg)
                return success_msg
            except Exception as e2:
                error_msg = f"❌ Failed to create PDF: {e2}. Please install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html"
                print(error_msg)
                return error_msg

    except Exception as e:
        error_msg = f"❌ Error while processing markdown: {e}"
        print(error_msg)
        return error_msg


# CrewAI Tool wrappers
# @tool("Resume Extractor")
# def extract_resume(resume: str) -> str:
#     """
#     Extracts text content from a PDF resume located at {resume}.
#     Returns the extracted text content from the PDF resume.
#     """
#     return _extract_resume_core(resume)


# @tool("Resume Saver")
# def save_resume_as_pdf(markdown_content: str) -> str:
#     """
#     Converts markdown resume content to a professional PDF file.

#     This tool takes markdown-formatted resume content and converts it to a styled PDF.
#     The markdown should contain a complete resume with sections like:
#     - Name and contact information
#     - Professional summary
#     - Work experience
#     - Education
#     - Skills
#     - Any additional relevant sections

#     Args:
#         markdown_content: The complete resume content formatted in markdown

#     Returns:
#         str: Success message with file path or error description

#     Example:
#         To use this tool, pass the complete markdown resume like:
#         save_resume_as_pdf("# John Doe\\n## Software Engineer\\n\\n### Experience\\n...")
#     """
#     # Handle the case where the agent might pass unexpected data
#     if isinstance(markdown_content, dict):
#         print(
#             "⚠️ Warning: Received dict instead of string. Attempting to extract content..."
#         )
#         # Try to find markdown content in the dict
#         if "content" in markdown_content:
#             markdown_content = markdown_content["content"]  # type: ignore
#         elif "text" in markdown_content:
#             markdown_content = markdown_content["text"]  # type: ignore
#         elif "markdown_content" in markdown_content:
#             markdown_content = markdown_content["markdown_content"]  # type: ignore
#         else:
#             # If we can't find the content, return an error with helpful info
#             return f"❌ Error: Expected string markdown content, but received dict with keys: {list(markdown_content.keys())}"

#     if not isinstance(markdown_content, str):
#         return f"❌ Error: Expected string markdown content, but received {type(markdown_content)}"

#     return _save_resume_as_pdf_core(markdown_content)
