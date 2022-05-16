from aio_pika import *
import asyncio


async def task(msg):
    print(f" [x] Received msg {msg}")
    print(f"{msg.body}")
    await asyncio.sleep(1)
    print(f"done {msg}")


async def main():
    conn = await connect(login="worker1", password="test")
    async with conn:
        channel = await conn.channel()
        queue = await channel.declare_queue("hello")
        await queue.consume(task, no_ack=True)

        print("waiting for msg.")
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
