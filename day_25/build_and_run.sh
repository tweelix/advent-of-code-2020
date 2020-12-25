#!/bin/sh
rm -f a.o
g++ -o a.o day_25.cpp -std=c++2a -march=native -Wall -Wextra -O3
./a.o