#!/bin/sh
set  -e

conda activate hsf-india
#source /opt/_activate_conda.sh

exec "$@"
