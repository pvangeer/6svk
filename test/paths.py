from pathlib import Path

# TODO: Maybe consider changing all file paths to a Path instead of string and passing Path variables.
_test_data_dir = Path(__file__).parent / "test-data"
test_data_dir = str(_test_data_dir)

_test_output_dir = Path(__file__).parent / "test-output"
_test_output_dir.mkdir(parents=True, exist_ok=True)

test_output_dir = str(_test_output_dir)
