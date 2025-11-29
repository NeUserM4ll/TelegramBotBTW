#!/bin/bash

if [[ -z "$VIRTUAL_ENV" ]]; then
    source ./.venv/bin/activate
fi

if [[ -f ".env" ]]; then
    set -a
    source .env
    set +a

    if [[ -z "$TOKEN" ]]; then
        echo "по какой-то невведомоной причине отказывается работать программа укажите токен"
        exit 
    fi
    python3 ./app/main.py "$TOKEN"

else 
    read -p "файла не существует .env но сейчас создам)). введите токен : " TOKEN
    echo "TOKEN= $TOKEN " > .env
fi