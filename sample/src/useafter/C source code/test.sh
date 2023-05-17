#! /bin/bash

cc=gcc
CFLAGS=Wall
for file in *.c
do
	echo "Compiling $file ..."
	$cc   -o "${file%.c}" $file -fcf-protection=none -fno-stack-protector
	mv "${file%.c}" ~/AutoDectVuln/sample/src/useafter/C source code
done
echo "Complation complete."
