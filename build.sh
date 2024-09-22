#!/bin/bash

echo Building uSockets dependency...
set -x
cd "$(dirname "$0")"/uWebSockets/uSockets
rm -f *.o
gcc -DLIBUS_NO_SSL -std=c11 -Isrc -O3 -c src/*.c src/eventing/*.c
set +x

echo Building uWebsockets-based random number server...
set -x
cd ../..
g++  -march=native -O3 -std=c++17 -IuWebSockets/src -IuWebSockets/uSockets/src server.cpp uWebSockets/uSockets/*.o -lz -o server
set +x
