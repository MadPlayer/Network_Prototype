import asyncio
from grpc.aio import insecure_channel, UnaryUnaryCall, UnaryUnaryClientInterceptor
from common_package import (
    PrimeCalculateStub,
    NumberRange,
    Response,
)
from prometheus_client import start_http_server, Counter

DATA = [i for i in range(100000)]
response_counter = Counter("response", "the number of responses")


class Interceptor(UnaryUnaryClientInterceptor):
    async def intercept_unary_unary(continuation, client_call_details, request):
        response_counter.inc()
        return await continuation(client_call_details, request)


def callback(outcome):
    print(f"outcome is {outcome.primes}")


async def main():
    request_msg = NumberRange(values=DATA)
    start_http_server(5000)
    async with insecure_channel("localhost:50051", interceptors=(Interceptor(), )) as channel:
        stub = PrimeCalculateStub(channel)
        print("---start request---")
        future: UnaryUnaryCall = None
        for i in range(10):
            if future:
                # callback(await future)
                await future

            future = stub.get_prime_list(request_msg)


if __name__ == '__main__':
    asyncio.run(main())
