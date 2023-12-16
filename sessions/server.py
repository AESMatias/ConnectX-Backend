import asyncio
from sessions.chat import chatAll
from decouple import config
from app.utils.auth import get_current_user_by_token
from jose import JWTError, jwt
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class Server:

    def __init__(self):
        self.host = config('SOCKETS_HOST')
        self.port = config('SOCKETS_PORT', cast=int)
        self.active_sockets = []
        self.active_clients_vinculed = {}

    async def generalChat(self, message, sender):
        chat = chatAll(self.active_sockets)
        await chat.generalChat(message, sender)

    async def peer_to_peer(self, message, sender, destination):
        chat = chatAll(self.active_sockets)
        await chat.peer_to_peer(message, sender, destination)


        chat = chatAll(self.active_sockets)
        await chat.peer_to_peer(message, sender, destination)

    def close_connection(self, writer, addr):
        try:
            if self.active_sockets:
                for client_socket in self.active_sockets:
                    if client_socket == writer:
                        writer.write('close_the_connection'.encode('utf-8'))
                        print(f'{addr} has been closed')
                        writer.close()
                        self.active_sockets.remove(writer)
                        return True
        except Exception as e:
            print(f"Error closing connection {addr} with Exception:", str(e))
            return False


    def authenticate_user(self, token, writer, reader):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            self.active_clients_vinculed[writer] = {"user": username, "reader": reader}
            print(len(self.active_clients_vinculed))
        except JWTError as e:
            print("JWT Error:", str(e))

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.active_sockets.append(writer)
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    continue
                data = data.decode('utf-8')
                message_parts = data.split("|")
                chatType = message_parts[0]
                jwt = message_parts[1]
                destination = message_parts[2]
                message = message_parts[3]
                self.authenticate_user(jwt, writer, reader)
                if chatType == "general":
                    print(jwt)
                    await self.generalChat(message, writer)

                    #comparar si el usuario existe en la db

                    #Proceder a enviar o rebotar el mensaje

                #print(f"From user {str(addr)}:", str(message))
                
        except Exception as e:
            print("Error:", str(e))
        finally:
            print('finally')
            writer.close()
            self.active_sockets.remove(writer)
        

    def start_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = loop.run_until_complete(
            asyncio.start_server(self.handle_client, self.host, self.port))
        try:
            loop.run_until_complete(server.serve_forever())
        except KeyboardInterrupt:
            pass
