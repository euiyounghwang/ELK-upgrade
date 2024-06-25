#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"

# Activate virtualenv && run serivce
SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $SCRIPTDIR/$VENV/bin/activate
else
    source $SCRIPTDIR/$VENV/Scripts/activate
fi

py.test -v tests
# py.test -v ./tests --cov-report term-missing --cov
# poetry run py.test -sv ./tests --disable-warnings --cov-report term-missing --cov