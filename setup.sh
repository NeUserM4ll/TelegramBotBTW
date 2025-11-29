#!/bin/bash


if command -v python3 &>/dev/null; then
    echo "Python already installed"
else 
    echo "Python is not installed in your computer. python is installing...."
    sudo apt update
    sudo apt install -y python3 python3-pip
    echo "python have been installed"

fi
if [[ ! -d ".venv" ]]; then
    python3 -m venv ./.venv
    
fi

if [[ -z "$VIRTUAL_ENV" ]]; then
    source ./.venv/bin/activate
    echo "Виртуальное окружение активно: $VIRTUAL_ENV"
fi


if [[ -f "requirements.txt" ]]; then
    echo "Устанавливаю библиотеки из requirements.txt..."
    pip install -r requirements.txt
    echo "Библиотеки успешно установлены."

else
    echo "Файл requirements.txt не найден."
fi
echo "sdsf"
if [[ ! -f ".env" ]]; then
    read -p "enter API token your telegram bot" TOKEN
    echo "TOKEN=$TOKEN" > .env
fi 

