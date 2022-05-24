import asyncio
import pickle
import uuid
from asyncio_mqtt import Client, MqttError


URL = "localhost"


class MQTTClient:
    loop: asyncio.AbstractEventLoop

    def __init__(self):
        self.loop = asyncio.get_running_loop()

    async def connect(self, hostname: str, username: str, password: str):
        self.client = Client(hostname=hostname, username=username,
                             password=password)
        await self.client.connect()
        return self

    async def request(self):
        future = self.loop.create_future()
        self.loop.create_task(self.request_(future))
        return future

    async def request_(self, future):
        call_id = str(uuid.uuid4())
        reply_topic = f"test/{call_id}"
        await self.client.subscribe(reply_topic)
        self.loop.create_task(
            self.client.publish(
                "rpc_queue",
                payload=pickle.dumps({
                    "data": "hello world",
                    "reply_to": reply_topic,
                }),
                qos=1,
            )
        )
        print(f"reply_to {reply_topic}")

        async with self.client.filtered_messages(reply_topic) as msgs:
            async for msg in msgs:
                print(f"outcome: {msg.payload.decode()}")
                await self.client.unsubscribe(reply_topic)
                future.set_result(msg)


async def main():
    client = await MQTTClient().connect(URL, "client1", "test")

    for i in range(10000):
        future = await client.request()
        print("middle")
        msg = await future
        print(f"outcome2: {msg.payload.decode()}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except MqttError as e:
        print(e)
