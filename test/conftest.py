import pytest
from svk.io import RendererServer

skip_local = False


def pytest_collection_modifyitems(config, items):
    # Running specific tests/files?
    explicitly_selected = any("::" in arg for arg in config.args)

    if explicitly_selected:
        return

    skip_product = pytest.mark.skip(reason="Product tests are excluded from normal test runs.")

    for item in items:
        if "product" in item.keywords:
            item.add_marker(skip_product)
        if "localproduct" in item.keywords and skip_local:
            item.add_marker(skip_product)


@pytest.fixture(scope="session", autouse=True)
def renderer_server():
    RendererServer.start()

    yield

    RendererServer.stop()
