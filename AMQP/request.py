from aio_pika import *
import asyncio


async def main():
    conn = await connect(login="client1", password="test")
    async with conn:
        channel = await conn.channel()
        queue = await channel.declare_queue("hello")
        await channel.default_exchange.publish(Message(b"Hello World"),
                                               routing_key=queue.name,
                                               )


if __name__ == '__main__':
    asyncio.run(main())
