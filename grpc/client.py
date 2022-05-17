import asyncio
from grpc.aio import insecure_channel, UnaryUnaryCall
import test_pb2
import test_pb2_grpc as test_grpc


DATA = [i for i in range(100000)]


def callback(outcome):
    print(f"outcome is {outcome.ans}")


async def main():
    async with insecure_channel("localhost:50051") as channel:
        stub = test_grpc.RemoteSumStub(channel)
        print("---start request---")
        future: UnaryUnaryCall = None
        for i in range(10):
            request_msg = test_pb2.Blob()
            request_msg.values.extend(DATA)
            if future:
                callback(await future)

            future = stub.sum(request_msg)
            print(type(future))


if __name__ == '__main__':
    asyncio.run(main())
