#!/bin/bash

count_charo=$(ls Iseg/ | grep 'a$' | wc -l)

count_iseg_ladies=$(ls Epitech/ | grep 'z$' | wc -l)

if [ $count_charo -gt 0 ]; then
    mv Iseg/*a Epitech/
fi

if [ $count_iseg_ladies -gt 0 ]; then
    mv Epitech/*z Iseg/
fi

