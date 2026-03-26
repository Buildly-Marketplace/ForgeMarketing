#!/bin/bash

# Script to add dark mode classes to all remaining elements in the HTML file
# This will add dark: variants to common text and background classes

sed -i '' \
    -e 's/text-gray-900\([^-]\)/text-gray-900 dark:text-white\1/g' \
    -e 's/text-gray-800\([^-]\)/text-gray-800 dark:text-white\1/g' \
    -e 's/text-gray-700\([^-]\)/text-gray-700 dark:text-gray-200\1/g' \
    -e 's/text-gray-600\([^-]\)/text-gray-600 dark:text-gray-300\1/g' \
    -e 's/text-gray-500\([^-]\)/text-gray-500 dark:text-gray-400\1/g' \
    -e 's/bg-white\([^-]\)/bg-white dark:bg-gray-900\1/g' \
    -e 's/bg-gray-50\([^-]\)/bg-gray-50 dark:bg-gray-800\1/g' \
    -e 's/bg-gray-100\([^-]\)/bg-gray-100 dark:bg-gray-800\1/g' \
    -e 's/border-gray-200\([^-]\)/border-gray-200 dark:border-gray-700\1/g' \
    -e 's/border-gray-300\([^-]\)/border-gray-300 dark:border-gray-600\1/g' \
    index.html

echo "Dark mode classes added to index.html"
