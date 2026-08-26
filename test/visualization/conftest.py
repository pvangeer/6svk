import pytest
from svk.io import RendererServer


@pytest.fixture(scope="session", autouse=True)
def renderer_server():
    RendererServer.start()

    yield

    RendererServer.stop()
