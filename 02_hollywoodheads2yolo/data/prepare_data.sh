#!/bin/bash

set -e

# check argument
if [[ -z $1 || ! $1 =~ [[:digit:]]x[[:digit:]] ]]; then
  echo "ERROR: This script requires 1 argument, \"input dimension\" of the YOLO model."
  echo "The input dimension should be {width}x{height} such as 640x480 or 416x256.".
  exit 1
fi

if which python3 > /dev/null; then
  PYTHON=python3
else
  PYTHON=python
fi


pushd $(dirname $0)/raw > /dev/null

# unzip image files
echo "** Unzip dataset files"
for f in HollywoodHeads.zip ; do
  unzip -n ${f}
done

echo "** Create the hollywoodheads-$1/ subdirectory"
rm -rf ../hollywoodheads-$1/
mkdir ../hollywoodheads-$1/
find HollywoodHeads/JPEGImages -maxdepth 1 -name "*.jpeg" -exec ln {} ../hollywoodheads-$1/ \;

# the hollywoodheads/ subdirectory now contains all train/val jpg images

echo "** Generate yolo txt files"
cd ..
${PYTHON} gen_txts.py $1

popd > /dev/null

echo "** Done."
