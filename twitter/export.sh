mongoexport --db mole --collection user --csv --fields id,followers | tr -d '"[]'  | sed '1d' | sed 's/,false/ /' > edgelist.csv
gzip -f edgelist.csv
