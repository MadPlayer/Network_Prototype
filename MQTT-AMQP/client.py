import asyncio
import pickle
import uuid
from asyncio_mqtt import Client, MqttError
import time
import uuid


URL = "localhost"

async def main():
    reply_topic = "test/" + str(uuid.uuid4())
    async with Client(hostname=URL,
                      username="client1",
                      password="test") as client:
        await client.subscribe(reply_topic)
        await client.publish(
            "rpc_queue",
            payload=pickle.dumps({
                "data": "hello world",
                "reply_to": reply_topic,
            }),
            qos=1,
        )
        print(f"reply_to {reply_topic}")

        async with client.filtered_messages(reply_topic) as msgs:
            async for msg in msgs:
                print(f"outcome: {msg.payload.decode()}")
                return


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except MqttError as e:
        print(e)
