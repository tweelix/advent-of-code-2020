#!/bin/sh
rm -f a.o
g++-10 -o a.o day_1.cpp -std=c++2a -Wall -Wextra -O2
./a.o