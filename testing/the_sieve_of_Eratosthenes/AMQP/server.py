import asyncio
import logging
import pickle
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from common_package import sieve_eratosthenes
from prometheus_client import Counter, start_http_server


URL = "localhost"
request_count = Counter("request_amqp",
                        "The number of Requests that server recieves")


async def main():
    user = "worker1"
    pw = "test"
    conn = await connect(f"amqp://{user}:{pw}@{URL}/")
    loop = asyncio.get_running_loop()
    start_http_server(1234)

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
                    request_count.inc()

                    msg = pickle.loads(message.body)

                    response = sieve_eratosthenes(len(msg))

                    loop.create_task(
                        exchange.publish(
                            Message(
                                body=pickle.dumps(response),
                                correlation_id=message.correlation_id,
                            ),
                            routing_key=message.reply_to,
                        )
                    )

            except Exception:
                logging.exception("Processing got Error %r", message)


if __name__ == '__main__':
    asyncio.run(main())
