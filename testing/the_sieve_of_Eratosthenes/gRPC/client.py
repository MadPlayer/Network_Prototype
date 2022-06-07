import asyncio
import pickle
from grpc.aio import insecure_channel, UnaryUnaryCall, UnaryUnaryClientInterceptor
from common_package import (
    PrimeCalculateStub,
    Blob,
    URL,
    DATA,
)
from prometheus_client import start_http_server, Counter


response_counter = Counter("response", "the number of responses")


class Interceptor(UnaryUnaryClientInterceptor):
    async def intercept_unary_unary(self, continuation, client_call_details,
                                    request):
        response_counter.inc()
        return await continuation(client_call_details, request)


def callback(outcome):
    print(f"outcome is {outcome.primes}")


async def main():
    request_msg = Blob(data=pickle.dumps(DATA))
    start_http_server(5000)
    async with insecure_channel(f"{URL}:50051", interceptors=(Interceptor(), )) as channel:
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
