#!/bin/bash

osascript -e 'tell application "Microsoft Excel" to close (every workbook whose name is "test.xlsx") saving no' >> /dev/null \
&& uv pip install -e . \
&& pg_summary -i -v localhost -u docker -d dev -s public -t books -o test.xlsx \
&& uv pip uninstall . \
&& open test.xlsx
