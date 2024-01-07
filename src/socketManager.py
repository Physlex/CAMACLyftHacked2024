from fastapi import WebSocket

class SocketManager():
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        pass

    async def connect(self) -> None:
        """
            Connect to the websocket
        """
        await self.websocket.accept()
        pass

    async def disconnect(self) -> None:
        """
            Disconnect from the websocket
        """
        await self.websocket.close()
        pass

    async def send_acceleration(self, data) -> None:
        """
            TODO: Get acceleration data from arduino
        """
        self.websocket.send_json("""SOME DATA""")
        pass
