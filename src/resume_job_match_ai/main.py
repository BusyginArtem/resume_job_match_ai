import asyncio
import os
import shutil
import sys
import traceback
import warnings

# Import both implementations
from .crew import ResumeJobMatchAi

warnings.filterwarnings(
    "ignore",
    category=SyntaxWarning,
    module="pysbd",
    message="There is no current event loop",
)

# Fix for Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Create event loop if none exists
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

OUTPUT_DIR = "output"
INPUT_DIR = "input"


def setup_directories():
    """Create necessary directories"""
    for directory in [OUTPUT_DIR, INPUT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")


def clean_output_directory():
    """Clean the output directory"""
    if os.path.exists(OUTPUT_DIR):
        for filename in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                print(f"🗑️ Deleted: {filename}")
            except OSError as e:
                print(f"❌ Failed to delete {file_path}. Reason: {e}")


def verify_input_files(resume_path: str, jd_path: str):
    """Verify that input files exist and are readable"""
    print("🔍 Verifying input files...")

    issues = []

    # Check resume file
    if not os.path.exists(resume_path):
        issues.append(f"Resume file not found: {resume_path}")
    elif not os.path.isfile(resume_path):
        issues.append(f"Resume path is not a file: {resume_path}")
    elif not resume_path.lower().endswith(".pdf"):
        issues.append(f"Resume file is not a PDF: {resume_path}")
    else:
        file_size = os.path.getsize(resume_path)
        print(f"✅ Resume file found: {resume_path} ({file_size:,} bytes)")

    # Check job description file
    if not os.path.exists(jd_path):
        issues.append(f"Job description file not found: {jd_path}")
    elif not os.path.isfile(jd_path):
        issues.append(f"Job description path is not a file: {jd_path}")
    else:
        file_size = os.path.getsize(jd_path)
        print(f"✅ Job description file found: {jd_path} ({file_size:,} bytes)")

    if issues:
        print("❌ Input file issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    return True


def run_with_debugging():
    """
    Run the crew with enhanced debugging and fallback options
    """
    print("🚀 Starting Resume Job Match AI with debugging...")
    print("=" * 60)

    # Setup
    setup_directories()
    clean_output_directory()

    # File paths
    resume_path = "./input/cv.pdf"
    jd_path = "./input/jd.txt"

    # Verify input files
    if not verify_input_files(resume_path, jd_path):
        print("\n💡 Please ensure you have:")
        print("  1. A PDF resume file at: ./input/cv.pdf")
        print("  2. A job description text file at: ./input/jd.txt")
        return False

    # Try CrewAI approach
    print("\n🤖 STEP 3: Running CrewAI approach...")
    print("-" * 40)
    try:
        inputs = {
            "resume": resume_path,
            "jd": jd_path,
        }

        print(f"📋 Inputs: {inputs}")

        # Initialize and run crew
        crew_instance = ResumeJobMatchAi()
        result = crew_instance.crew().kickoff(inputs=inputs)

        print("✅ CrewAI execution completed")
        print(f"📄 Result: {result}")

        # Check outputs
        check_outputs()

        return True

    except Exception as e:
        print(f"❌ CrewAI execution failed: {e}")
        traceback.print_exc()

        # Additional debugging
        print("\n🔍 DEBUGGING INFO:")
        print(f"  - Python version: {sys.version}")
        print(f"  - Current working directory: {os.getcwd()}")
        print(f"  - Output directory exists: {os.path.exists(OUTPUT_DIR)}")
        print(f"  - Input directory exists: {os.path.exists(INPUT_DIR)}")

        return False


def check_outputs():
    """Check and report on output files"""
    print("\n📊 CHECKING OUTPUTS:")
    print("-" * 30)

    expected_files = [
        "analyst_report.md",
        "job_matching_report.md",
        "web_research_summary.md",
        "resume_advising_report.md",
        "enhanced_resume.pdf",
    ]

    found_files = []
    missing_files = []

    for filename in expected_files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            found_files.append(f"{filename} ({file_size:,} bytes)")

            # Check if file has content or just action calls
            if filename.endswith(".md") and file_size < 100:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "Action:" in content and len(content.split("\n")) < 5:
                            print(f"⚠️ {filename}: Appears to contain only action calls")
                        else:
                            print(f"✅ {filename}: Contains proper content")
                except Exception as e:
                    print(f"⚠️ {filename}: Could not read content - {e}")
            else:
                print(f"✅ {filename}: Found with {file_size:,} bytes")
        else:
            missing_files.append(filename)
            print(f"❌ {filename}: Not found")

    print(f"\n📈 SUMMARY: {len(found_files)} found, {len(missing_files)} missing")

    # Special check for PDF
    pdf_path = os.path.join(OUTPUT_DIR, "enhanced_resume.pdf")
    if os.path.exists(pdf_path):
        print(f"🎉 PDF SUCCESSFULLY CREATED: {pdf_path}")
        return True
    else:
        print(f"❌ PDF NOT CREATED: {pdf_path}")
        return False


def run():
    """
    Main entry point - runs with debugging and fallbacks
    """
    try:
        success = run_with_debugging()
        if success:
            print("\n🎉 MISSION ACCOMPLISHED!")
        else:
            print("\n💥 MISSION FAILED - Check the logs above for details")

            # Provide troubleshooting tips
            print("\n🔧 TROUBLESHOOTING TIPS:")
            print("1. Ensure wkhtmltopdf is installed and in PATH")
            print("2. Check that input files exist and are readable")
            print("3. Verify CrewAI and dependencies are properly installed")
            print("4. Try running the explicit pipeline separately")
            print("5. Check the direct tool testing results")

    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        traceback.print_exc()


# import asyncio
# import os
# import shutil
# import sys
# import warnings

# from .crew import ResumeJobMatchAi

# warnings.filterwarnings(
#     "ignore",
#     category=SyntaxWarning,
#     module="pysbd",
#     message="There is no current event loop",
# )

# # Fix for Windows
# if sys.platform.startswith("win"):
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# # Create event loop if none exists
# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

# OUTPUT_DIR = "output"

# if not os.path.exists(OUTPUT_DIR):
#     os.makedirs(OUTPUT_DIR)


# def run():
#     """
#     Run the crew.
#     """

#     for filename in os.listdir(OUTPUT_DIR):
#         file_path = os.path.join(OUTPUT_DIR, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except OSError as e:
#             print("Failed to delete %s. Reason: %s" % (file_path, e))

#     resume_path = "./input/cv.pdf"
#     jd_path = "./input/jd.txt"

#     if not os.path.exists(resume_path) or not os.path.isfile(jd_path):
#         raise FileNotFoundError("The files are not provided.")

#     inputs = {
#         "resume": resume_path,
#         "jd": jd_path,
#     }

#     try:
#         print("Starting the crew...", inputs)
#         ResumeJobMatchAi().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         print("Error while running the crew:", e)
#         raise RuntimeError(f"An error occurred while running the crew: {e}") from e
