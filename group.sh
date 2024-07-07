#!/bin/bash

mapfile -td '' files < <(find . -mindepth 1 -maxdepth 1 -type f -print0)

pad=${#files[@]}
pad=${#pad}

for i in "${!files[@]}"; do
	if ! ((i%60)); then
		printf -v dir %0${pad}d $((++n))
		mkdir "$dir"
        mkdir "$dir/png"
        touch "$dir/png/.gitkeep"
	fi

	mv "${files[i]}" "./$dir/"
done