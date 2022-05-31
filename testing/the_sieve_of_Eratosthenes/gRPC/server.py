import asyncio
from grpc.aio import server
from common_package import (
    PrimeCalculateServicer,
    add_PrimeCalculateServicer_to_server,
    NumberRange,
    Response,
    sieve_eratosthenes,
)


class ServerImpl(PrimeCalculateServicer):
    def get_prime_list(self, request: NumberRange, context)->Response:
        n = len(request.values)
        return Response(primes=sieve_eratosthenes(n))


async def main():
    test_server = server()
    test_server.add_insecure_port("[::]:50051")
    add_PrimeCalculateServicer_to_server(ServerImpl(), test_server)
    await test_server.start()
    await test_server.wait_for_termination()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(e.args)
