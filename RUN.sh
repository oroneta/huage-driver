#!/bin/bash
echo "Select the model:"

read model

# check if model folder exist in /model
if [ ! -d "./model/$model" ]; then
    echo "Model not found"
    exit 1
fi

# Execute the script from /model/$models[$model]/driver.py
echo "Executing the script from /model/$model/driver.py"

cd ./model/$model

python3 -m pip install .
python3 ./driver.py