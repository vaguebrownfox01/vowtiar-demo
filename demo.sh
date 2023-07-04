#/bin/bash


source "env-vow/bin/activate"

demp_path=$(pwd)

ln -sf "$demo_path/praat/praat" "/usr/local/bin/"

python3 "script/live_formant_estimation.py" $demp_path &
python3 "script/live_vowtiar_plot.py" $demp_path
