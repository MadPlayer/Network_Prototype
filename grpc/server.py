import grpc
import test_pb2_grpc as test_grpc
import test_pb2
from concurrent.futures import ThreadPoolExecutor


class ServerImpl(test_grpc.RemoteSumServicer):
    def sum(self, request, context):
        return test_pb2.Response(ans = sum(request.values))


if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor(max_workers=8))
    test_grpc.add_RemoteSumServicer_to_server(ServerImpl(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
