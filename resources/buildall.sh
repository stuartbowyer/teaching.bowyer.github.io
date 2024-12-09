#!/usr/bin/env bash
cd "$(dirname "$0")"
ipynbs="$(ls ../**/**/*.ipynb)"
jupyter nbconvert --config config.py --to slides $ipynbs
jupyter nbconvert --config config.py --to webpdf $ipynbs

python generate_index.py ../SDSAI
