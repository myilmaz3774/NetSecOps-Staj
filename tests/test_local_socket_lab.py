import socket
import unittest

from modules.local_socket_lab import LocalTcpService, scan_loopback_ports


class LocalSocketLabTests(unittest.TestCase):
    def test_detects_temporary_loopback_service(self) -> None:
        with LocalTcpService() as service:
            results = scan_loopback_ports([service.port])

        self.assertEqual(results, [{"port": service.port, "status": "open"}])

    def test_detects_closed_loopback_port(self) -> None:
        temporary = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temporary.bind(("127.0.0.1", 0))
        closed_port = temporary.getsockname()[1]
        temporary.close()

        results = scan_loopback_ports([closed_port])

        self.assertEqual(results[0]["status"], "closed")

    def test_rejects_non_loopback_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "yalnızca loopback"):
            scan_loopback_ports([80], host="192.168.56.10")


if __name__ == "__main__":
    unittest.main()
