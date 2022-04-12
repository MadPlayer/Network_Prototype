PROTO = test
PY = python
CURRENT = $(shell pwd)


proto: ${PROTO}.proto
	${PY} -m grpc.tools.protoc -I./ --python_out=./ \
 --grpc_python_out=./ $<


clean:
	rm ${PROTO}_pb2.py ${PROTO}_pb2_grpc.py
	rm -r __pycache__
