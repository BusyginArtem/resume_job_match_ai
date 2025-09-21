import asyncio
import os
import shutil
import sys
import warnings

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

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def run():
    """
    Run the crew.
    """

    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))

    inputs = {
        "resume": "./input/Artem Busyhin CV_CH.pdf",
        "jd": "./input/jd.txt",
    }

    try:
        ResumeJobMatchAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        print("Error while running the crew:", e)
        raise RuntimeError(f"An error occurred while running the crew: {e}") from e
