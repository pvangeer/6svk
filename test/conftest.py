import pytest


def pytest_collection_modifyitems(config, items):
    # Running specific tests/files?
    explicitly_selected = any("::" in arg for arg in config.args)

    if explicitly_selected:
        return

    skip_product = pytest.mark.skip(reason="Product tests are excluded from normal test runs.")

    for item in items:
        if "product" in item.keywords:
            item.add_marker(skip_product)
