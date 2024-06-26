#!/bin/bash
#!/bin/bash
set -e

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"


# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $SCRIPTDIR/$VENV/bin/activate
else
    source $SCRIPTDIR/$VENV/Scripts/activate
fi

source .env
echo "Source Host - $S_HOST"
echo "Target Host - $ES_HOST"
# --
# default script for test indexing
python $SCRIPTDIR/reindex-script/Search-reindexing-script.py --es $S_HOST --source_index om_nci_10052020_20_5_1 --ts $ES_HOST

