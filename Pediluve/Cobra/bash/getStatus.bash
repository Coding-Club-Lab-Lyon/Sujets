#!/bin/bash

prec=$1

if [ "$prec" -eq 0 ]; then
    echo "Les pieds sont propres !"
else
    echo "T'as de ces ieps chacal..."
fi


echo "export PATH=$(pwd):\$PATH" >> ~/.bashrc