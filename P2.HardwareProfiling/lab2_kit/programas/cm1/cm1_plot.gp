#!/usr/bin/gnuplot

set logscale x 2;
plot "cm1_plot.dat" using 1:2 with lines title "8192B",  \
     "cm1_plot.dat" using 1:3 with lines title "16384", \
     "cm1_plot.dat" using 1:4 with lines title "32768", \
     "cm1_plot.dat" using 1:5 with lines title "65536";

pause mouse
