#!/bin/bash

count_iseg_ladies=$(ls Iseg/ | grep 'a$' | wc -l)

if [ $count_iseg_ladies -eq 0 ]; then
    statut=0
else
    statut=$count_iseg_ladies
fi

exit $statut

