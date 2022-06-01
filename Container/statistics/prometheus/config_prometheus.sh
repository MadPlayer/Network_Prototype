#!/bin/bash

cp prometheus.yml old_prometheus.yml

while [ $# -gt 0 ]; do
    case $1 in
        --ip=* )
            ip="${1#*=}"
            sed -i "s/<your local ip>/$ip/g" prometheus.yml
            ;;
    esac
    shift
done
