import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def sync_mongodb():

    subprocess.run(
        [
            "python",
            str(
                PROJECT_ROOT
                / "scripts"
                / "sync_to_mongodb.py"
            ),
        ],
        check=True,
    )

    return {
        "message": "Synchronization completed."
    }