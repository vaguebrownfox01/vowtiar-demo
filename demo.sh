#/bin/bash

source activate "env-vow/bin/activate"

if [ -d "praat_formants_python" ]; then
    echo "Folder exists"
    # Clone repository command here
else
    echo "Folder does not exist."
    git clone "https://github.com/mwv/praat_formants_python.git"
    
    cd "praat_formants_python"
    python3 setup.py install
    cd ..
fi

demp_path=$(pwd)

ln -sf "$demo_path/praat/praat" "/usr/local/bin/"

python3 "script/live_formant_estimation.py" $demp_path &
python3 "script/live_vowtiar_plot.py" $demp_path &
