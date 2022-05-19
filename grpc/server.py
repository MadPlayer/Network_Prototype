from grpc.aio import server
import asyncio
import test_pb2_grpc as test_grpc
import test_pb2


class ServerImpl(test_grpc.RemoteSumServicer):
    def sum(self, request, context):
        return test_pb2.Response(ans = sum(request.values))


async def main():
    test_server = server()
    test_server.add_insecure_port("[::]:50051")
    test_grpc.add_RemoteSumServicer_to_server(ServerImpl(), test_server)
    await test_server.start()
    await test_server.wait_for_termination()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(e.args)
