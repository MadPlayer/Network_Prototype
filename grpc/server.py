import grpc
import test_pb2_grpc as test_grpc
import test_pb2
from concurrent.futures import ThreadPoolExecutor


class ServerImpl(test_grpc.RemoteSumServicer):
    def sum(self, request, context):
        return test_pb2.Response(ans = sum(request.values))


def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=8))
    server.add_insecure_port("[::]:50051")
    test_grpc.add_RemoteSumServicer_to_server(ServerImpl(), server)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e.args)
