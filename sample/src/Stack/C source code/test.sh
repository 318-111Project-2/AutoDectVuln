#! /bin/bash

cc=gcc
CFLAGS=Wall
for file in *.c
do
	echo "Compiling $file ..."
	$cc   -o "${file%.c}" $file -fcf-protection=none -fno-stack-protector
	mv "${file%.c}" ~/AutoDectVuln/sample/demo/build
done
echo "Complation complete."
