from . import test_pb2, test_pb2_grpc
from .test_pb2_grpc import (
    PrimeCalculate,
    add_PrimeCalculateServicer_to_server,
    PrimeCalculateStub,
    PrimeCalculateServicer,
)
from .test_pb2 import Blob
from .eratosthenes import sieve_eratosthenes

URL = "localhost"
DATA = [i for i in range(100000)]


__all__=(
    PrimeCalculate,
    add_PrimeCalculateServicer_to_server,
    PrimeCalculateStub,
    PrimeCalculateServicer,
    Blob,
    sieve_eratosthenes,
    URL,
    DATA,
)
