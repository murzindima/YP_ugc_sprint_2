import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

pytest_plugins = [
    "tests.functional.fixtures.common",
    "tests.functional.fixtures.client",
    "tests.functional.fixtures.es_data",
    "tests.functional.fixtures.setup",
]
