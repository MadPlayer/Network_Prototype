import asyncio
import time
import uuid
import pickle
from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)
from common_package import Blob, URL, DATA
from prometheus_client import Counter, start_http_server
import sys

response_count = Counter("response_amqp", "the number of response that client recieves")

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
        self.callback_queue = \
            await self.channel.declare_queue(exclusive=True,
                                             auto_delete=True)

        await self.callback_queue.consume(self.callback)

        return self

    async def callback(self, message: AbstractIncomingMessage):
        if message.correlation_id is None:
            print(f"Bad message {message!r}")

        self.loop.create_task(message.ack())
        response_count.inc()
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def request(self, msg) -> asyncio.Future:
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        self.loop.create_task(
            self.channel.default_exchange.publish(
                Message(
                    msg,
                    correlation_id=correlation_id,
                    reply_to=self.callback_queue.name,
                ),
                routing_key="rpc_queue",
            )
        )

        return future


async def main():
    client = await OffloadingClient().connect(login=sys.argv[1], password="test")
    while True:
        request_msg = pickle.dumps(DATA)
        future = await client.request(request_msg)
        pickle.loads(await future)


if __name__ == '__main__':
    asyncio.run(main())
