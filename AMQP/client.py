import asyncio
import time
import uuid
from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)


URL = "localhost"


class OffloadingClient:
    conn: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop


    def __init__(self):
        self.futures = {}
        self.loop = asyncio.get_running_loop()


    async def connect(self, login: str, password: str) -> "OffloadingClient":
        self.conn = await connect(
            f"amqp://{login}:{password}@{URL}/", loop=self.loop,
        )
        self.channel = await self.conn.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True,
                                                               auto_delete=True)
        await self.callback_queue.consume(self.callback)

        return self


    async def callback(self, message: AbstractIncomingMessage):
        if message.correlation_id is None:
            print(f"Bad message {message!r}")

        await message.ack()
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)


    async def request(self, n: int)->asyncio.Future:
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                str(n).encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key="rpc_queue",
        )

        return future


async def main():
    client = await OffloadingClient().connect(login="client1", password="test")
    print(" [x] Requesting fib(30)")
    for i in range(1000):
        future = await client.request(30)
        response = int(await future)
        print(f" [.] Got {response!r}")
        time.sleep(0.5)


if __name__ == '__main__':
    asyncio.run(main())
