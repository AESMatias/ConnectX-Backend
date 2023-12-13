import asyncio
from sessions.chat import chatAll
from decouple import config



class Server:

    def __init__(self):
        self.host = config('SOCKETS_HOST')
        self.port = config('SOCKETS_PORT', cast=int)
        self.active_sockets = []

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

    async def handle_client(self, reader,
                            writer):  # Make the method asynchronous
        addr = writer.get_extra_info('peername')
        print("Connection established with:", str(addr))
        self.active_sockets.append(writer)

        try:
            while True:
                data = await reader.read(4096)  # Await the coroutine
                if not data:
                    continue
                elif data.decode('utf-8').lower().endswith('close') \
                        or data.decode('utf-8').lower().endswith('exit'):
                    print(f'The user {addr} wants to exit', str(addr))
                    has_been_closed = self.close_connection(writer, addr)
                    print('The session has been closed?', has_been_closed)
                    self.return_to_All(f'The user {addr} has left the chat',
                                       writer)
                    continue
                data = data.decode('utf-8')
                print(f"From user {str(addr)}:", str(data))
                await self.return_to_All(data, writer)
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
