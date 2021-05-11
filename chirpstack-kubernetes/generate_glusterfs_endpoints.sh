#!/bin/bash

# Generate GlusterFS endpoint for mosquitto, postgre and influxdb


echo "apiVersion: v1
kind: Endpoints
metadata:
  name: mosquitto-gluster
subsets:" > mosquitto/mosquitto-glusterfs-endpoint.yaml

echo "apiVersion: v1
kind: Endpoints
metadata:
  name: postgre-gluster
subsets:" > postgres/postgre-glusterfs-endpoint.yaml

echo "apiVersion: v1
kind: Endpoints
metadata:
  name: influxdb-gluster
subsets:" > influxdb/influxdb-glusterfs-endpoint.yaml


for i in {140..143}
do
echo "- addresses:
  - ip: 131.254.150.$i
  ports:
  - port: 49152
    protocol: TCP" >> mosquitto/mosquitto-glusterfs-endpoint.yaml
echo "- addresses:
  - ip: 131.254.150.$i
  ports:
  - port: 49153
    protocol: TCP" >> postgres/postgre-glusterfs-endpoint.yaml
echo "- addresses:
  - ip: 131.254.150.$i
  ports:
  - port: 49154
    protocol: TCP" >> influxdb/influxdb-glusterfs-endpoint.yaml
done
