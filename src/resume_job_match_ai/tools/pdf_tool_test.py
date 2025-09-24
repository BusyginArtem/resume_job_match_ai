import os
import sys

# Add the src directory to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from resume_job_match_ai.tools.pdf_tools import (
    _extract_resume_core,
    _save_resume_as_pdf_core,
)


def test_pdf_extraction():
    """Test function to extract text from PDF resume"""

    resume_path = "./input/cv.pdf"
    extracted_text = _extract_resume_core(resume_path)
    assert extracted_text, "No text extracted from the PDF resume"
    print("Extracted Text:")
    print(extracted_text)


def test_pdf_creation():
    """Test the PDF creation functionality"""

    # Create output directory if it doesn't exist
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Test markdown content
    test_markdown = """
# John Doe
## Software Engineer

📧 john.doe@email.com | 📱 +1-555-123-4567 | 🔗 linkedin.com/in/johndoe

---

### Professional Summary
Experienced Software Engineer with 5+ years of expertise in full-stack development, specializing in Python, JavaScript, and modern web technologies. Proven track record of delivering scalable applications and leading cross-functional teams.

---

### Technical Skills
- **Languages:** Python, JavaScript, TypeScript, Java, SQL
- **Frameworks:** React, Django, Flask, Node.js, Express
- **Databases:** PostgreSQL, MongoDB, Redis
- **Cloud:** AWS, Docker, Kubernetes
- **Tools:** Git, Jenkins, Jira, VS Code

---

### Work Experience

#### Senior Software Engineer
**Tech Company Inc.** | *January 2021 - Present*

- Developed and maintained 5+ web applications serving 10,000+ daily active users
- Led a team of 4 developers in implementing microservices architecture
- Reduced application load time by 40% through code optimization and caching strategies
- Collaborated with product managers to define technical requirements and project timelines

#### Software Engineer
**StartUp Solutions** | *June 2019 - December 2020*

- Built RESTful APIs using Python/Django serving mobile and web applications
- Implemented automated testing procedures, improving code coverage by 60%
- Participated in agile development processes and sprint planning
- Mentored 2 junior developers on best practices and code review processes

---

### Education

#### Bachelor of Science in Computer Science
**University of Technology** | *2015 - 2019*

- **GPA:** 3.8/4.0
- **Relevant Coursework:** Data Structures, Algorithms, Software Engineering, Database Systems
- **Senior Project:** E-commerce platform built with React and Node.js

---

### Certifications
- **AWS Certified Solutions Architect** (2022)
- **Certified Kubernetes Administrator** (2021)
- **MongoDB Certified Developer** (2020)

---

### Projects

#### E-Commerce Platform
- Full-stack web application with React frontend and Django backend
- Integrated Stripe payment processing and inventory management
- **Technologies:** React, Django, PostgreSQL, Redis, Docker

#### Task Management API
- RESTful API for project and task management with real-time notifications
- Implemented JWT authentication and role-based access control
- **Technologies:** Node.js, Express, MongoDB, Socket.io
"""

    print("Testing PDF creation...")
    print("=" * 50)

    try:
        result = _save_resume_as_pdf_core(test_markdown)
        print("\nTest Result:")
        print(result)

        # Check if file was created
        if os.path.exists("./output/enhanced_resume.pdf"):
            file_size = os.path.getsize("./output/enhanced_resume.pdf")
            print("\n✅ File created successfully!")
            print(f"📄 File size: {file_size} bytes")
            print(f"📁 Location: {os.path.abspath('./output/enhanced_resume.pdf')}")
        else:
            print("\n❌ PDF file was not created")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("\nTroubleshooting tips:")
        print("1. Install wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html")
        print(
            "2. Make sure wkhtmltopdf is in your PATH or update the path in setup_pdfkit_windows()"
        )
        print("3. Try running: pip install pdfkit wkhtmltopdf")


if __name__ == "__main__":
    test_pdf_creation()
    test_pdf_extraction()
