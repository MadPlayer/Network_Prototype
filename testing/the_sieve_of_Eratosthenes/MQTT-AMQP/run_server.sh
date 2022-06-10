#!/bin/bash


export PROMETHEUS_MULTIPROC_DIR=$(pwd)/prometheus
rm -rf $PROMETHEUS_MULTIPROC_DIR
mkdir $PROMETHEUS_MULTIPROC_DIR
ids=$(seq 1234 1238)

for i in $ids; do
	python server.py worker$i &
done

