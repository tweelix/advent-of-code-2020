#!/bin/sh
rm -f a.o
g++ -o a.o day_23.cpp -std=c++2a -march=native -Wall -Wextra -O3 -fno-exceptions -fno-rtti
./a.o