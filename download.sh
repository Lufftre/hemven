#!/bin/bash
for i in {2..35}
do
    URL="https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=18031&location_ids%5B%5D=18028&location_ids%5B%5D=17892&location_ids%5B%5D=17846&page=$i"
    curl $URL > page$i.html
    sleep 1
done
