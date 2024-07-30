#!/bin/bash

# Function to replace multiple line breaks and multiple tabs
replace_line_breaks_and_tabs() {
  local file="$1"
  # Use perl to replace more than two consecutive line breaks with exactly two
  # and more than one consecutive tab with exactly one
  perl -0777 -pe 's/\n{3,}/\n\n/g; s/\t{2,}/\t/g' "$file" > temp_file && mv temp_file "$file"
}

# Export the function to use with find's -exec
export -f replace_line_breaks_and_tabs

# Find all .txt files and process them with the function
find . -type f -name "*.txt" -exec bash -c 'replace_line_breaks_and_tabs "$0"' {} \;

echo "Processing complete."
