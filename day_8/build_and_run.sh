#!/bin/sh
rm -f a.o
g++-10 -o a.o day_8.cpp -std=c++2a -Wall -Wextra -O3 -I .
./a.o