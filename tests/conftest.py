import sys
from pathlib import Path

# Add project root dir to PATH so that tests can import modules
sys.path.append(str(Path(__file__).resolve().parents[1]))
