#!/bin/bash

for d in 2 3
do
    echo "Running with $d s delay" && \
    hatch run server $d &
    serverID=$! && \
    hatch run client $d && \
    echo "Killing server ($serverID)" && \
    kill $serverID

done