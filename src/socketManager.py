import copy
from fastapi import WebSocket

class SocketMan():
    def __init__(self) -> None:
        self.CurrentBuffer = ""
        # self.SendBuffer = [[],[]]
        self.SendBuffer = []
        # self.ActiveBuffer = 0
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
            # print("b4", len(self.CurrentBuffer))
            self.CurrentBuffer = self.CurrentBuffer.split("\n", 1)[1]
            # print("aft", len(self.CurrentBuffer))


            # Filter current read, just focus on accelerometer logs (starts with "a:")
            if("a" == currRead.split(":", 1)[0]):
                currRead = currRead.split(":", 1)[1]
            else:
                currRead = ''
                return


            # Print (not necessary, still here for debugging purposes)
            # errorString = "ERROR: BUFFER SIZE IS " + str(len(self.CurrentBuffer)) + ", FALLING BEHIND | " if len(self.CurrentBuffer) > 500 else ""
            # print(errorString + currRead)



            # Prevent null error
            if(currRead == ''):
                return
            
            # Catch steaming errors (if something unexpected happens, drop the sample)
            # reading = ""
            
            # try:
            # reading = {
            #     'ax': int(currRead.split("\t")[0]),
            #     'ay': int(currRead.split("\t")[1]),
            #     'az': int(currRead.split("\t")[2]),
            #     'gx': int(currRead.split("\t")[3]),
            #     'gy': int(currRead.split("\t")[4]),
            #     'gz': int(currRead.split("\t")[5]),
            # }

            # self.SendBuffer[self.ActiveBuffer].append(reading)
            # await self.socket.send_json(reading)
            await self.socket.send_json({
                'ax': int(currRead.split("\t")[0]),
                'ay': int(currRead.split("\t")[1]),
                'az': int(currRead.split("\t")[2]),
                'gx': int(currRead.split("\t")[3]),
                'gy': int(currRead.split("\t")[4]),
                'gz': int(currRead.split("\t")[5]),
            })

            # except KeyboardInterrupt:
            #     exit()

            # except:
            #     print("Failed to decode.")



            # Send reading (old non-batched method)
            # await self.socket.send_json(reading)
            # except:
            #     print("oops")

        
        # if(len(self.SendBuffer[self.ActiveBuffer]) >= 10):
        #     # Send reading
        #     print("SENDOING", self.SendBuffer)
        #     await self.socket.send_json({"batched": self.SendBuffer[self.ActiveBuffer]})

        #     # Swap buffers
        #     nextBuffer = self.ActiveBuffer + 1
        #     if(nextBuffer >= 2): nextBuffer = 0
        #     self.SendBuffer[nextBuffer] = []
        #     self.ActiveBuffer = nextBuffer


        pass

    socket: WebSocket
