#!/bin/bash

# Check if dev.env already exists
if [ -f "dev.env" ]; then
    echo "dev.env already exists. Do you want to overwrite it? (y/n)"
    read -r answer

    if [ "$answer" != "y" ]; then
        echo "Exiting without overwriting dev.env"
        exit 0
    fi
fi

if [ -f "prod_env.json" ]; then
    echo "prod_env.json already exists. Do you want to overwrite it? (y/n)"
    read -r answer

    if [ "$answer" != "y" ]; then
        echo "Exiting without overwriting prod_env.json"
        exit 0
    fi
fi

# Copy the template to create a new dev.env file
cp dev.env.template dev.env
cp prod_env.json.template prod_env.json
echo "dev and prod env files generated, please update accordingly"
