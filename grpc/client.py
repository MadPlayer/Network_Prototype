import grpc
import test_pb2
import test_pb2_grpc as test_grpc


if __name__ == '__main__':
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = test_grpc.RemoteSumStub(channel)
        print("---start request---")
        for i  in range(10):
            request_msg = test_pb2.Blob()
            request_msg.values.extend([i for i in range(10)])
            outcome = stub.sum(request_msg)
            print(f"outcome is {outcome.ans}")
