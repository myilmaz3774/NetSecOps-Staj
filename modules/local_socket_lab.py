"""Yalnızca loopback üzerinde çalışan güvenli TCP laboratuvarı."""

from __future__ import annotations

import ipaddress
import socket
import threading
from collections.abc import Iterable

from modules.storage import save_json, timestamp


class LocalTcpService:
    """Gerçek TCP bağlantısını göstermek için geçici bir loopback servisi."""

    def __init__(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("127.0.0.1", 0))
        self._server.listen()
        self._server.settimeout(0.1)
        self.port = self._server.getsockname()[1]
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def _serve(self) -> None:
        while not self._stop_event.is_set():
            try:
                connection, _ = self._server.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            with connection:
                connection.sendall(b"NETSECOPS_LOCAL_LAB\n")

    def __enter__(self) -> "LocalTcpService":
        self._thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self._stop_event.set()
        self._server.close()
        self._thread.join(timeout=1)


def _validate_loopback_target(host: str) -> None:
    try:
        address = ipaddress.ip_address(host)
    except ValueError as error:
        raise ValueError("Yerel laboratuvar hedefi doğrudan IP adresi olmalıdır.") from error
    if not address.is_loopback:
        raise ValueError("Yerel TCP laboratuvarı yalnızca loopback hedeflerini kabul eder.")


def scan_loopback_ports(
    ports: Iterable[int], host: str = "127.0.0.1", timeout: float = 0.2
) -> list[dict]:
    """Loopback üzerindeki TCP portlarına bağlantı kurulup kurulamadığını kontrol eder."""
    _validate_loopback_target(host)
    results = []
    for port in ports:
        if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            raise ValueError("TCP portu 1-65535 arasında bir tam sayı olmalıdır.")
        try:
            with socket.create_connection((host, port), timeout=timeout):
                status = "open"
        except (ConnectionRefusedError, TimeoutError, OSError):
            status = "closed"
        results.append({"port": port, "status": status})
    return results


def _reserve_closed_port() -> int:
    temporary = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temporary.bind(("127.0.0.1", 0))
    port = temporary.getsockname()[1]
    temporary.close()
    return port


def run_local_socket_demo() -> tuple[list[dict], str]:
    """Bir açık ve bir kapalı portla kontrollü TCP denetimi gerçekleştirir."""
    with LocalTcpService() as service:
        closed_port = _reserve_closed_port()
        results = scan_loopback_ports([service.port, closed_port])

    output_path = f"data/reports/local_socket_scan_{timestamp()}.json"
    save_json(
        output_path,
        {
            "mode": "local-loopback-lab",
            "target": "127.0.0.1",
            "results": results,
        },
    )
    return results, output_path
