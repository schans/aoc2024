#!/bin/bash
#

set -eu -o pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

sessionkey="not-valid"
source ~/.aoc2024

a=$( echo "${1}" | bc )
b=$( printf %02d "${a}" )

mkdir -p "${b}"

curl -s -b "session=${sessionkey}" "https://adventofcode.com/2024/day/${a}/input" | tee "${b}/input"

wc "${b}/input"
