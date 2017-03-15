#!/usr/bin/env bash
# Percentage printer.  eg percent.sh 50 100 => "50%"

. `type -p jjlib.sh` && usage_exit "$#" 2 "`basename $0` part total" "$@"

num=$(echo "scale=2; ($1 / $2) * 100" | bc | sed 's/[.].*//')

[[ -n "$num" ]] && echo "$num%" || echo "0%"
