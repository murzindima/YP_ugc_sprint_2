import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

pytest_plugins = [
    "tests.functional.fixtures.common",
]
