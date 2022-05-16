import grpc
import test_pb2
import test_pb2_grpc as test_grpc

DATA = [i for i in range(100000)]


def callback(future):
    outcome = future.result()
    print(f"outcome is {outcome.ans}")


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = test_grpc.RemoteSumStub(channel)
        print("---start request---")
        future = None
        for i in range(10):
            request_msg = test_pb2.Blob()
            request_msg.values.extend(DATA)
            if future:
                callback(future)

            future = stub.sum.future(request_msg)


if __name__ == '__main__':
    main()
