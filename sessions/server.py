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

    async def return_to_All(self, message, sender):
        chat = chatAll(self.active_sockets)
        await chat.send_to_all(message, sender)

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


    async def authenticate_user(self, token, writer, reader):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            self.active_clients_vinculed[writer] = {"user": username, "reader": reader}
            print(self.active_clients_vinculed)
        except JWTError as e:
            print("JWT Error:", str(e))

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwMjUwODMzMX0.WP-hIcoms8iujnzZnD0y2kYliV5nMN9BtYXJBZk0fnk"

        print("Connection established with:", str(addr))
        self.active_sockets.append(writer)

        try:
            authentication_task = asyncio.create_task(self.authenticate_user(token, writer, reader))
            while True:
                data = await reader.read(4096)
                if not data:
                    continue
                elif data.decode('utf-8').lower().endswith('close') \
                        or data.decode('utf-8').lower().endswith('exit'):
                    print(f'The user {addr} wants to exit', str(addr))
                    has_been_closed = self.close_connection(writer, addr)
                    print('The session has been closed?', has_been_closed)
                    self.return_to_All(f'The user {addr} has left the chat', writer)
                    continue

                data = data.decode('utf-8')
                print(f"From user {str(addr)}:", str(data))
                await self.return_to_All(data, writer)
                await authentication_task  # Wait for authentication to complete
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
