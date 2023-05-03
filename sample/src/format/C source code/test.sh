#! /bin/bash

cc=gcc
for file in *.c
do
	echo "Compiling $file ..."
	$cc   -o "${file%.c}" $file -fcf-protection=none -fno-stack-protector
	mv "${file%.c}" ~/AutoDectVuln/sample/src/format/o
done
echo "Complation complete."
