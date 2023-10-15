import multiprocessing
import time

from fastapi.testclient import TestClient
import pytest

from sys_stats.app_server import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sys Stats" in response.text


def loop_function():
    while True:
        time.sleep(10)


def _start_new_process_and_return_pid():
    new_process = multiprocessing.Process(target=loop_function)
    new_process.start()
    return new_process.pid


def test_kill_process_by_pid():
    pid = _start_new_process_and_return_pid()

    response = client.get(f"/kill/{pid}")
    assert response.status_code == 200


def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200


# Test the /ports endpoint
def test_get_net_connections():
    response = client.get("/ports")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
