#! /bin/sh

# rename output of uberdownloader to expose date and players
# currently operates on files in the current directory

# test for existence of files first
ls -1 OGS_game_*.sgf > /dev/null 2>&1 || exit

for file in OGS_game_*.sgf
do
    game_number=${file##*_}
    game_number=${game_number%.*}
    date=$(grep -o 'DT\[.*]' $file | sed -e 's/DT\[//' | sed -e 's/]//')
    black=$(grep -o 'PB\[.*]' $file | sed -e 's/PB\[//' | sed -e 's/]//')
    white=$(grep -o 'PW\[.*]' $file | sed -e 's/PW\[//' | sed -e 's/]//')

    new_filename=$(echo "OGS-$date-$game_number-$black-$white" | sed -e 's/[^0-9a-zA-Z-]/_/g').sgf
    echo "$file\t-> $new_filename"
    mv $file $new_filename
done