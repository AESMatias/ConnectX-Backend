class chatAll:
    def __init__(self, active_sockets):
        self.active_sockets = active_sockets

    async def generalChat(self, message, sender) -> None:
        if self.active_sockets:
            for client_socket in self.active_sockets:
                if client_socket != sender:
                    try:
                        client_socket.write(message.encode('utf-8'))
                        print('MESSAGE LOOPED TO ALL', message)
                        await client_socket.drain()
                    except Exception as e:
                        print("Error sending message:", str(e))
                        await client_socket.drain()

    async def p2pChat(self, message, sender, destination):
        pass



