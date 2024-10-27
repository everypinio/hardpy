from __future__ import annotations

import socket

from .connection_data import ConnectionData


class SocketServer:
    """Socket server abstraction."""

    def __init__(self) -> None:
        self._server = socket.socket()
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con_data = ConnectionData()

        try:
            self._server.bind((con_data.socket_host, con_data.socket_port))
        except OSError as exc:
            self._server.close()
            msg = (
                "Socket creating error by"
                f"{con_data.socket_host}:{con_data.socket_port}"
            )
            raise RuntimeError(msg) from exc
        self._server.listen(1)

    def __del__(self) -> None:
        self._server.close()

    def accept(self) -> list[socket.socket, tuple]:
        """Accept server.

        Returns:
            list[socket.socket, tuple]: socket object, address info
        """
        return self._server.accept()
