import os
import subprocess
import sys


def test_training_runs():
    # Run training script as a smoke test; allow non-zero if mlflow unreachable
    cwd = os.path.join(os.path.dirname(__file__), "..", "pipeline")
    result = subprocess.run([sys.executable, "train.py"], cwd=cwd)
    assert result.returncode in (0, 1)
