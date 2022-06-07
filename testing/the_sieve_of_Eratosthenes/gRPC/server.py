import asyncio
from grpc.aio import server, ServerInterceptor
import pickle
from common_package import (
    PrimeCalculateServicer,
    add_PrimeCalculateServicer_to_server,
    Blob,
    sieve_eratosthenes,
)
from prometheus_client import start_http_server, Counter

request_counter = Counter("request", "the number of received requests")
blob = Blob()

class Interceptor(ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        """
        Intercepts incoming RPCs before handling them over to a handler
        """
        request_counter.inc()
        return await continuation(handler_call_details)


class ServerImpl(PrimeCalculateServicer):
    def get_prime_list(self, request, context):
        n = len(pickle.loads(request.data))
        ans = sieve_eratosthenes(n)
        blob.data = pickle.dumps(ans)
        return blob


async def main():
    test_server = server(interceptors=(Interceptor(),))
    test_server.add_insecure_port("[::]:50051")
    add_PrimeCalculateServicer_to_server(ServerImpl(), test_server)
    await test_server.start()
    await test_server.wait_for_termination()


if __name__ == '__main__':
    try:
        start_http_server(1234)
        asyncio.run(main())
    except Exception as e:
        print(e.args)
