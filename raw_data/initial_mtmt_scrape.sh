#!/bin/bash
set -o errexit
set -o nounset
set -eou pipefail

FILE_TO_SCRAPE=$1
SCRAPE_DIR="$(dirname $(readlink -f "$0"))/initial_scrapes"

base_file_to_scrape=$(basename "$FILE_TO_SCRAPE")
base_filename="${base_file_to_scrape%.*}"
extension="${base_file_to_scrape##*.}"

FILE_NAME="${base_filename}_initial_scrape.${extension}"

cat "$FILE_TO_SCRAPE" | grep -E -e "Interaction:" -e '[[:digit:]]\.' -e "Category:" -e "Description:" -e "Justification:" -e "Possible\ Mitigation\(s\)" -e "SDL\ Phase:" > ${SCRAPE_DIR}/${FILE_NAME}