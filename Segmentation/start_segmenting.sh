#! /bin/bash
source ~/miniconda/etc/profile.d/conda.sh
conda activate lecture 
# virtualenv is now active.
# This if ran using command below, you can log out of dice computer and it will still run in background, make sure it is executable by you
# e.g. ls -la, if you seen an "x" then good, else run "chmod +x start_segmenting.sh"
# you will want to run this script using this command "longjob -28day -c ./start_segmenting.sh"
python segment.py