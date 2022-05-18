import asyncio
import pickle
import logging
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage

URL = "localhost"


async def main():
    user = "worker1"
    pw = "test"
    conn = await connect(f"amqp://{user}:{pw}@{URL}/")

    channel = await conn.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue("rpc_queue")
    exchange = await channel.get_exchange("amq.direct")
    await queue.bind(exchange)

    print(" [X] Awaiting RPC requests")

    async with queue.iterator() as it:
        message: AbstractIncomingMessage
        async for message in it:
            try:
                async with message.process(requeue=False):
                    payload = pickle.loads(message.body)
                    data = payload["data"]
                    reply_to = payload["reply_to"]
                    # some code
                    print(f"Request: {data}")
                    print(f"Reply to: {reply_to}")
                    await exchange.publish(
                        Message(
                            body="done".encode(),
                        ),

                        # AMQP routing_key to MQTT topic
                        routing_key=reply_to.replace("/", "."), 
                    )
                    print("Reply Done")

            except Exception:
                logging.exception("Processing got Error %r", message)


if __name__ == '__main__':
    asyncio.run(main())
