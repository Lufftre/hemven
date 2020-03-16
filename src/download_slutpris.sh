#!/bin/bash
for i in {1..50}
do
    URL="https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=898741&page=$i"
    curl $URL > slutpriser/page$i.html
    sleep 1
done
