import asyncio
import pickle
import logging
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from common_package import sieve_eratosthenes
from prometheus_client import Counter, start_http_server, multiprocess, CollectorRegistry
import sys

URL = "localhost"
request_count = Counter("request_amqp_mqtt",
                        "The number of Requests that server recieves")


async def main():
    user = sys.argv[1]
    pw = "test"
    conn = await connect(f"amqp://{user}:{pw}@{URL}/")
    loop = asyncio.get_running_loop()

    channel = await conn.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue("rpc_queue")
    exchange = await channel.get_exchange("amq.topic")
    await queue.bind(exchange)

    print(" [X] Awaiting RPC requests")

    async with queue.iterator() as it:
        message: AbstractIncomingMessage
        async for message in it:
            try:
                async with message.process(requeue=False):
                    request_count.inc()
                    request_msg = pickle.loads(message.body)
                    data = request_msg["data"]
                    reply_to = request_msg["reply_to"]

                    loop.create_task(
                        exchange.publish(
                            Message(
                                body=pickle.dumps(sieve_eratosthenes(len(data)))
                            ),
                            # AMQP routing_key to MQTT topic
                            routing_key=reply_to.replace("/", "."),
                        )
                    )

            except Exception:
                logging.exception("Processing got Error %r", message)


if __name__ == '__main__':
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    if "worker1234" in sys.argv:
        start_http_server(1234, registry=registry)
    asyncio.run(main())
