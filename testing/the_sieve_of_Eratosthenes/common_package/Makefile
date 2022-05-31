PROTO = test
PY = python
CURRENT = $(shell pwd)


proto: ${PROTO}.proto
	${PY} -m grpc.tools.protoc -I./ --python_out=./ \
	 --grpc_python_out=./ $<

	sed -i \
	's/import\ ${PROTO}_pb2/from\ .\ import\ ${PROTO}_pb2/' ${PROTO}_pb2_grpc.py


clean:
	rm -f ${PROTO}_pb2.py ${PROTO}_pb2_grpc.py
	rm -rf __pycache__
