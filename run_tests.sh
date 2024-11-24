#!/bin/bash

# If your blender is not available as just "blender" command, then you need
# to specify path to blender when running this script, e.g.
#
# $ BLENDER=~/soft/blender-2.79/blender ./run_tests.sh
#

set -e

BLENDER=${BLENDER:-blender}

$BLENDER -b --addons sverchok,sverchok_extra --python testing.py --python-exit-code 1

