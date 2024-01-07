from fastapi import WebSocket

class SocketMan():
    def __init__(self) -> None:
        self.socket = WebSocket()
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

    async def send_acceleration(self, data) -> None:
        """
            TODO: Get acceleration data from arduino
        """
        self.socket.send_json("""SOME DATA""")
        pass
