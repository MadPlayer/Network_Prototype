import asyncio
import pickle
import logging
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from common_package import (
    NumberRange,
    Response,
    MQTT_AMQP_Request,
    sieve_eratosthenes,
)
from prometheus_client import Counter, start_http_server

URL = "localhost"
request_msg = MQTT_AMQP_Request()
request_count = Counter("request_amqp_mqtt",
                        "The number of Requests that server recieves")


async def main():
    user = "worker1"
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
                    request_msg.ParseFromString(message.body)
                    data = request_msg.number_range
                    reply_to = request_msg.reply_to

                    loop.create_task(
                        exchange.publish(
                            Message(
                                body=sieve_eratosthenes(
                                    len(data.values)).SerializeToString()
                            ),
                            # AMQP routing_key to MQTT topic
                            routing_key=reply_to.replace("/", "."),
                        )
                    )

            except Exception:
                logging.exception("Processing got Error %r", message)


if __name__ == '__main__':
    start_http_server(1234)
    asyncio.run(main())
