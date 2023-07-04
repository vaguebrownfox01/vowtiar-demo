#/bin/bash

if [ -d "env-vow" ]; then
    echo "env-vow exists"
else
    echo "env-vow does not exist."
    python3 -m venv env-vow
    pip3 install -r requirements.txt
fi

source "env-vow/bin/activate"


if [ -f "/usr/local/sbin/praat" ]; then
    echo "praat exists"
else
    echo "praat does not exist."

    wget https://www.fon.hum.uva.nl/praat/praat6310_linux64.tar.gz -O praat/praat.tar.gz
    tar -xzf praat/praat.tar.gz -C praat/
    rm praat/praat.tar.gz
    sudo ln -sf "$(pwd)/praat/praat" "/usr/local/sbin/"
fi


if [ -d "praat_formants_python" ]; then
    echo "praat_formants_python exists"

else
    echo "pfp does not exist."
    git clone "https://github.com/mwv/praat_formants_python.git"
    
    cd "praat_formants_python"
    python3 setup.py install
    cd ..
fi

