import asyncio
from grpc.aio import server, ServerInterceptor
from common_package import (
    PrimeCalculateServicer,
    add_PrimeCalculateServicer_to_server,
    NumberRange,
    Response,
    sieve_eratosthenes,
)
from prometheus_client import start_http_server, Counter

request_counter = Counter("request", "the number of received requests")
response_counter = Counter("response", "the number of responses")

class Interceptor(ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        """
        Intercepts incoming RPCs before handling them over to a handler
        """
        request_counter.inc()
        return await continuation(handler_call_details)


class ServerImpl(PrimeCalculateServicer):
    def get_prime_list(self, request: NumberRange, context)->Response:
        n = len(request.values)
        response_counter.inc()
        return Response(primes=sieve_eratosthenes(n))


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
