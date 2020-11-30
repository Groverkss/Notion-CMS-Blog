#!/bin/bash

# Export environment variables``
[ -e .secrets ] && . ./.secrets

# Run script
python3 main.py
