from fastapi import WebSocket

class SocketMan():
    def __init__(self) -> None:
        pass

    async def connect(self, websocket: WebSocket) -> None:
        """
            Connect to the websocket and add it to all web
        """
        await websocket.accept()
        self.socket = websocket
        pass

    async def disconnect(self) -> None:
        """
            Disconnect from all websockets
        """
        await self.socket.close()
        pass

    async def send_acceleration(self, serial_port) -> None:
        """
            TODO: Get acceleration data from arduino
        """
        await self.socket.send_json({"fudge": [0, 0]})
        pass

    socket: WebSocket
