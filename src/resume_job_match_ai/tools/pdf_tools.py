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
def extract_resume(resume: str) -> str:
    """
    Extracts text content from a PDF resume located at {resume}.
    Reads the PDF file, iterates through its pages, and concatenates the extracted text.
    If a page contains no extractable text, a warning is printed. If no text is found in the entire document,
    raises a RuntimeError indicating the PDF may be scanned or non-extractable.
    Any other exceptions encountered during extraction are also raised as RuntimeError.
    Returns:
        str: The extracted text content from the PDF resume.
    Raises:
        RuntimeError: If no extractable text is found or if an error occurs during extraction.
    """
    print(f"Extracting text from resume: {resume}")
    try:
        with open(resume, "rb") as file:
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
        return text
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting the resume: {e}") from e


@tool("Resume Saver")
def save_resume_as_pdf(markdown_content: str):
    """
    Saves the provided resume text as a PDF file.

    Args:
        resume_text (str): The path to the resume file or the resume content to be saved as a PDF.

    Returns:
        str: A message indicating whether the CV was saved successfully.

    Raises:
        RuntimeError: If an error occurs while saving the CV as a PDF.
    """
    try:
        print("Markdown to HTML...", markdown_content)
        html = markdown.markdown(markdown_content, extensions=["codehilite", "tables"])
        print("Converting markdown to PDF...", html)
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
            print(f"PDF saved to {output_path}")
        except Exception:
            # Try without config if wkhtmltopdf is in PATH
            try:
                pdfkit.from_string(styled_html, output_path)
                print(f"PDF saved to {output_path}")
            except Exception as e2:
                print(f"Error while saving CV: {e2}")
                print(
                    "Please install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html"
                )

    except Exception as e:
        print(f"Error while saving CV: {e}")
        raise RuntimeError(f"An error occurred while saving the CV: {e}") from e
