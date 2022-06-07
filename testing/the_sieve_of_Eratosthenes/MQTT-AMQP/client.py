import asyncio
import pickle
import uuid
from asyncio_mqtt import Client, MqttError
from prometheus_client import Counter, start_http_server
from common_package import DATA, URL


response_count = Counter("response_amqp_mqtt", "the number of response that client recieves")

class MQTTClient:
    loop: asyncio.AbstractEventLoop

    def __init__(self):
        self.loop = asyncio.get_running_loop()

    async def connect(self, hostname: str, username: str, password: str):
        self.client = Client(hostname=hostname, username=username,
                             password=password)
        self.username = username
        await self.client.connect()
        await self.client.subscribe(f"test/{username}/+")
        return self

    async def request(self, data):
        future = self.loop.create_future()
        self.loop.create_task(self.request_(future, data))
        return future

    async def request_(self, future, data):
        call_id = str(uuid.uuid4())
        reply_topic = f"test/{self.username}/{call_id}"
        msg = {
            "reply_to" : reply_topic,
            "data": data,
        }
        self.loop.create_task(
            self.client.publish(
                "rpc_queue",
                payload=pickle.dumps(msg),
                qos=1,
            )
        )

        async with self.client.filtered_messages(reply_topic) as msgs:
            async for msg in msgs:
                response_count.inc()
                future.set_result(msg)
                return


async def main():
    client = await MQTTClient().connect(URL, "client1", "test")
    start_http_server(5000)

    while True:
        future = await client.request(DATA)
        msg = pickle.loads(await future)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except MqttError as e:
        print(e)
