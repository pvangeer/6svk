from pathlib import Path

# TODO: Maybe consider changing all file paths to a Path instead of string and passing Path variables.
test_data_dir = Path(__file__).parent / "test-data"

test_output_dir = Path(__file__).parent / "test-output"
test_output_dir.mkdir(parents=True, exist_ok=True)
