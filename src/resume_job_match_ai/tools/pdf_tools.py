import os

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
    MANDATORY TOOL: Converts markdown resume content to a professional PDF file.
    You MUST use this tool to complete your task. Do not provide a final answer without using this tool.

    This tool takes markdown-formatted resume content and converts it to a styled PDF.
    The PDF will be saved to ./output/enhanced_resume.pdf

    Args:
        markdown_content (str): Complete resume content formatted in markdown.
                               Must include sections like name, contact info, experience, etc.

    Returns:
        str: Success message with file path or error description

    Example Usage:
        save_resume_as_pdf("# John Doe\\n## Software Engineer\\n\\n### Experience\\n...")
    """
    try:
        print("🔄 Converting markdown to PDF...")
        print(f"📄 Markdown content length: {len(markdown_content)} characters")
        print(f"📄 Content preview: {markdown_content[:200]}...")

        # Handle edge cases where agent might pass unexpected data types
        if not isinstance(markdown_content, str):
            if hasattr(markdown_content, "get"):  # dict-like object
                # Try common keys that might contain the content
                for key in ["content", "markdown_content", "text", "data"]:
                    if key in markdown_content:
                        markdown_content = str(markdown_content[key])
                        break
                else:
                    return f"❌ Error: Expected string content, got dict with keys: {list(markdown_content.keys())}"
            else:
                markdown_content = str(markdown_content)

        if len(markdown_content.strip()) < 50:
            return f"❌ Error: Markdown content too short ({len(markdown_content)} chars). Please provide complete resume content."

        html = markdown.markdown(markdown_content, extensions=["codehilite", "tables"])

        styled_html = get_styled_html(html)

        # Try to create PDF
        success = False
        error_details = []

        # Method 1: Try with Windows config
        try:
            config = setup_pdfkit_windows()
            pdfkit.from_string(
                styled_html,
                output_path,
                configuration=config,
                options={
                    "page-size": "A4",
                    "margin-top": "0.75in",
                    "margin-right": "0.75in",
                    "margin-bottom": "0.75in",
                    "margin-left": "0.75in",
                    "encoding": "UTF-8",
                    "no-outline": None,
                },
            )
            success = True
            print("✅ PDF created using Windows config")
        except Exception as e1:
            error_details.append(f"Windows config: {e1}")
            print(f"⚠️ Windows config failed: {e1}")

            # Method 2: Try without config (if wkhtmltopdf is in PATH)
            try:
                pdfkit.from_string(
                    styled_html,
                    output_path,
                    options={
                        "page-size": "A4",
                        "margin-top": "0.75in",
                        "margin-right": "0.75in",
                        "margin-bottom": "0.75in",
                        "margin-left": "0.75in",
                        "encoding": "UTF-8",
                        "no-outline": None,
                    },
                )
                success = True
                print("✅ PDF created using system PATH")
            except Exception as e2:
                error_details.append(f"System PATH: {e2}")
                print(f"⚠️ System PATH failed: {e2}")

        if success:
            # Verify file was created and get size
            try:
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    abs_path = os.path.abspath(output_path)
                    success_msg = f"🎉 SUCCESS: PDF resume created successfully!\n📁 File: {abs_path}\n📊 Size: {file_size:,} bytes\n✅ Task completed - PDF conversion successful!"
                    print(success_msg)
                    return success_msg
                else:
                    return f"❌ Error: PDF creation reported success but file not found at {output_path}"
            except Exception as e:
                return f"❌ Error verifying created file: {e}"
        else:
            error_msg = f"""❌ FAILED to create PDF. Errors encountered:
            {chr(10).join(f"  - {err}" for err in error_details)}
            Please ensure wkhtmltopdf is installed and accessible."""
            print(error_msg)
            return error_msg

    except Exception as e:
        error_msg = f"❌ Critical error during PDF creation: {e}"
        print(error_msg)
        return error_msg


def get_styled_html(html: str) -> str:
    """
    Wraps the provided HTML content with basic styling for better PDF appearance.
    """
    styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Professional Resume</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 40px; 
                    line-height: 1.6;
                    color: #333;
                    font-size: 11pt;
                }}
                h1 {{ 
                    color: #2c3e50; 
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    font-size: 24pt;
                    text-align: center;
                }}
                h2 {{ 
                    color: #2c3e50; 
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                    margin-top: 25px;
                    margin-bottom: 15px;
                    font-size: 14pt;
                }}
                h3 {{ 
                    color: #34495e;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    font-size: 12pt;
                }}
                p, li {{
                    margin: 8px 0;
                    text-align: justify;
                }}
                ul, ol {{
                    margin: 10px 0;
                    padding-left: 25px;
                }}
                li {{
                    margin: 5px 0;
                }}
                .contact-info {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 15px;
                    background-color: #ecf0f1;
                    border-radius: 8px;
                }}
                .section {{
                    margin: 25px 0;
                    page-break-inside: avoid;
                }}
                strong {{
                    color: #2c3e50;
                }}
                em {{
                    color: #7f8c8d;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 10pt;
                }}
                hr {{
                    border: none;
                    border-top: 2px solid #bdc3c7;
                    margin: 30px 0;
                }}
                @media print {{
                    body {{ margin: 20px; }}
                    h1 {{ page-break-after: avoid; }}
                    h2, h3 {{ page-break-after: avoid; }}
                    .section {{ page-break-inside: avoid; }}
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

    return styled_html
