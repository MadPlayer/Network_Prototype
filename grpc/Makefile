PROTO = test
PROTO_DIR = ./packet
PY = python


proto: ${PROTO}.proto ${PROTO_DIR}
	${PY} -m grpc.tools.protoc -I./ --python_out=${PROTO_DIR} \
 --grpc_python_out=${PROTO_DIR} $<

${PROTO_DIR}:
	mkdir -p $@

clean:
	rm -r ${PROTO_DIR}
