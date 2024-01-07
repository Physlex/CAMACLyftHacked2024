from fastapi import WebSocket

class SocketMan():
    def __init__(self) -> None:
        self.CurrentBuffer = ""
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
                self.CurrentBuffer += incoming.decode("utf-8")
            except:
                print("WARN: Failed to decode bytestring, skipping.")


        # When there's an endline char in the buffer, its time to flush
        if("\n" in self.CurrentBuffer):

            # Update and flush buffer
            currRead = self.CurrentBuffer.split("\n", 1)[0]
            self.CurrentBuffer = self.CurrentBuffer.split("\n", 1)[1]


            # Filter current read, just focus on accelerometer logs (starts with "a:")
            if("a" == currRead.split(":", 1)[0]):
                currRead = currRead.split(":", 1)[1]
            else:
                currRead = ''


            # Print (not necessary, still here for debugging purposes)
            errorString = "ERROR: BUFFER SIZE IS " + str(len(self.CurrentBuffer)) + ", FALLING BEHIND | " if len(self.CurrentBuffer) > 500 else ""
            print(errorString + currRead)


            # Prevent null error
            if(currRead == ''):
                return
            
            # Catch steaming errors (if something unexpected happens, drop the sample)
            reading = ""
            
            try:
                reading = {
                    'ax': int(currRead.split("\t")[0]),
                    'ay': int(currRead.split("\t")[1]),
                    'az': int(currRead.split("\t")[2]),
                }

                # Send reading
                await self.socket.send_json(reading)
            except:
                print("oops")

        pass

    socket: WebSocket
