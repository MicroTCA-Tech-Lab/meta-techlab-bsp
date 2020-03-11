#! /bin/bash

SIZE=$((128*1024*1024))
echo "init udmabuf with size $SIZE"

modprobe udmabuf udmabuf0=$SIZE

