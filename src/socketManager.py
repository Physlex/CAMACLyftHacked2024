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
            TODO: harvest acceleration data from arduino
        """

        incoming = (serial_port.read(serial_port.inWaiting()))
        if(incoming != b''):
            try:
                CurrentBuffer += incoming.decode("utf-8")
            except:
                print("WARN: Failed to decode bytestring, skipping.")


        # When there's an endline char in the buffer, its time to flush
        if("\n" in CurrentBuffer):

            # Update and flush buffer
            currRead = CurrentBuffer.split("\n", 1)[0]
            CurrentBuffer = CurrentBuffer.split("\n", 1)[1]


            # Print (not necessary, still here for debugging purposes)
            # errorString = "ERROR: BUFFER SIZE IS " + str(len(CurrentBuffer)) + ", FALLING BEHIND | " if len(CurrentBuffer) > 500 else ""
            # print(errorString + currRead)


            # Send reading
            await self.socket.send_json({
                'ax': int(currRead.split("\t")[0]),
                'ay': int(currRead.split("\t")[1]),
                'az': int(currRead.split("\t")[2]),
            })
        pass

    socket: WebSocket
