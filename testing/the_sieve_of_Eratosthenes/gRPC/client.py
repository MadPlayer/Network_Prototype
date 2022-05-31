import asyncio
from grpc.aio import insecure_channel, UnaryUnaryCall
from common_package import (
    PrimeCalculateStub,
    NumberRange,
    Response,
)


DATA = [i for i in range(100000)]


def callback(outcome):
    print(f"outcome is {outcome.primes}")


async def main():
    async with insecure_channel("localhost:50051") as channel:
        stub = PrimeCalculateStub(channel)
        print("---start request---")
        future: UnaryUnaryCall = None
        for i in range(10):
            request_msg = NumberRange(values=DATA)
            if future:
                # callback(await future)
                await future

            future = stub.get_prime_list(request_msg)


if __name__ == '__main__':
    asyncio.run(main())
