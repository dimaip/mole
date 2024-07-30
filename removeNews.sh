#!/bin/bash

# Function to delete files containing '~p' in their name
delete_files_with_pattern() {
  local pattern="$1"
  find scrape -type f -name "*${pattern}*" -exec rm -f {} \;
}

# Call the function with the pattern '~p'
delete_files_with_pattern "~p"

echo "Files containing '~p' in their name have been removed."
