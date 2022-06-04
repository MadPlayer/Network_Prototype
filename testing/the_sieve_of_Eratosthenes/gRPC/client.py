import asyncio
from grpc.aio import insecure_channel, UnaryUnaryCall, UnaryUnaryClientInterceptor
from common_package import (
    PrimeCalculateStub,
    NumberRange,
    Response,
)
from prometheus_client import start_http_server, Counter, Histogram
from prometheus_async.aio import time


DATA = [i for i in range(100000)]
response_counter = Counter("response", "the number of responses")
request_time = Histogram("request_time", "Histogram for networking time which spent to send resquest")


class Interceptor(UnaryUnaryClientInterceptor):
    @time(request_time)
    async def intercept_unary_unary(self, continuation, client_call_details,
                                    request):
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
        while True:
            if future:
                # callback(await future)
                await future

            future = stub.get_prime_list(request_msg)


if __name__ == '__main__':
    asyncio.run(main())
