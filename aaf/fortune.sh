#!/usr/bin/env bash
set -o errexit && set -o pipefail && : # set -o xtrace

declare -r __basename="$(basename "${BASH_SOURCE[0]}")"
declare -r __dirname="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# tempfile doesn't exist on Mac, silently fail and use mktemp instead
# FIXME: Is mktemp more portable?
declare -r __tmpfile="$(tempfile -s fortune 2>/dev/null || mktemp /tmp/fortune.XXXXXXXXXXX)"
declare -r __fortune_file="fortune.txt"

__usage_exit() {
    echo "Usage:    $__basename update|fortune|string"
    exit 0
}

__update() {
    local -r my_file="$1"
    local -r http_aaf="aHR0cDovL3d3dy5hc2NpaWFydGZhcnRzLmNvbS9mb3J0dW5lLnR4dA=="

    curl --progress-bar $(echo "$http_aaf"|base64 --decode) >"${my_file}"
    strfile "${my_file}" "${my_file}.dat"
}

# Old Mac code, not sure what it was for
# my_script_dir() {
#     local my_path="`dirname \"$0\"`"  # relative
#     my_path="`( cd \"$my_path\" && pwd )`"  # absolute, normalized
#     if [ -z "$my_path" ]
#     then
#         echo "Error: '$my_path' doesn't exist"
#         exit 1
#     fi
#     echo "$my_path"
# }

__gasbgone() {
    fortune "${__fortune_file}" >${__tmpfile}
    ./gasbgone.sh ${__tmpfile}
}

# Main
trap "rm -f '$__tmpfile'" exit  # clean up __tmpfile on exit
cd "$__dirname"

case "$1" in
    u*) __update "${__fortune_file}" ;;
    f*) fortune   "${__fortune_file}" ;;
    s*) __gasbgone ;;
    *)  __usage_exit ;;
esac
