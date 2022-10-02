#!/bin/bash
#mkdir notebook
cd notebook/
#virtualenv jupyterenv
#ls
source /home/mark/github/freqtrade/.env/bin/activate
#pip install jupyter
jupyter nbextension enable --py widgetsnbextension
jupyter notebook
