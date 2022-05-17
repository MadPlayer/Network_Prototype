import asyncio
import logging
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage

URL = "localhost"

fib_vals = [0, 1]
def fib(n: int):
    i = len(fib_vals)
    while i <= n:
        fib_vals.append(
            fib_vals[i - 1] + fib_vals[i - 2]
        )
        i += 1

    return fib_vals[n]


async def main():
    user = "worker1"
    pw = "test"
    conn = await connect(f"amqp://{user}:{pw}@{URL}/")

    channel = await conn.channel()
    exchange = channel.default_exchange

    queue = await channel.declare_queue("rpc_queue")
    await channel.set_qos(prefetch_count=1)
    print(" [X] Awaiting RPC requests")

    async with queue.iterator() as it:
        message: AbstractIncomingMessage
        async for message in it:
            try:
                async with message.process(requeue=False):
                    assert message.reply_to is not None

                    n = int(message.body.decode())

                    print(f" [.] fib({n})")
                    response = str(fib(n)).encode()

                    await exchange.publish(
                        Message(
                            body=response,
                            correlation_id=message.correlation_id,
                        ),
                        routing_key=message.reply_to,
                    )
                    print("Request complete")
            except Exception:
                logging.exception("Processing got Error %r", message)


if __name__ == '__main__':
    asyncio.run(main())
