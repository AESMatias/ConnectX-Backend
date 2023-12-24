from datetime import datetime


class chatAll:
    def __init__(self, active_sockets, active_clients_vinculed ):
        self.active_sockets = active_sockets
        self.active_clients_vinculed = active_clients_vinculed

    async def general_writer(self, message, writer):
        try:
            writer.write(message.encode('utf-8'))
            print('MESSAGE LOOPED TO ALL', message)
            await writer.drain()
        except Exception as e:
            print("Error sending message:", str(e))
            await writer.drain()


    async def generalChat(self, username, data, sender) -> None:
        if self.active_sockets:
            for client_socket in self.active_sockets:
                message = f"{username}: {data}"
                print(message)
                if client_socket != sender:
                    if message.startswith("MESSAGE_LOGIN"):
                        await client_socket.drain()
                    else:
                        await self.general_writer(message, client_socket)
            return True

    async def p2pChat(self, username, message, sender, destination):
        for user, client_info in self.active_clients_vinculed.items():
            if user == destination:
                destination_writer = client_info["writer"]
                formatted_message = f"{username} (private): {message}"

                try:
                    destination_writer.write(formatted_message.encode('utf-8'))
                    await destination_writer.drain()
                    print(f'MESSAGE SENT TO {destination}: {message}')
                except Exception as e:
                    print(f"Error sending private message to {destination}: {str(e)}")



