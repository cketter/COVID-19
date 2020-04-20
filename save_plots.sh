#/bin/bash
cd COVID-19/
../gen_covid19_epi_curve.py "(Hawaii, Hawaii|Kauai|Honolulu|Maui)" --cut 35 --stacked --save
../gen_covid19_epi_curve.py Honolulu --cut 35 --stacked --save
../gen_covid19_epi_curve.py "(Italy|Korea|New York City|Russia)" --cut 25 --save
../gen_covid19_epi_curve.py Australia --cut 35 --stacked --regional --save
../gen_covid19_epi_curve.py Russia --cut 50 --stacked --save
../gen_covid19_epi_curve.py "(New York City|Hubei)" --regional --save