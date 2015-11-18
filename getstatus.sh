rm cutstatus.txt
for f in results/CL*.csv; do wc "$f" >> cutstatus.txt; done;
sort cutstatus.txt
