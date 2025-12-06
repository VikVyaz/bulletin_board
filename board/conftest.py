import pytest


@pytest.fixture(autouse=True)
def mock_celery(monkeypatch):
    def fake_delay(*args, **kwargs):
        return None

    monkeypatch.setattr("board.tasks.send_notification.delay", fake_delay)
