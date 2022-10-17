#!/bin/sh
# Generates html and pdf documentation of the board

base=$1
thumbx=100

#Run from doc folder make file

# First copy files
mkdir -p static
cp ../pcb/doc/* static
mv static/"$base".pdf static/"$base"_sch.pdf
cp ../pcb/prod/*.csv static
rm -f static/doc_data.txt

#crop top and bottom images
mogrify -trim -fuzz 10% static/"$base"_brd*



#then split schematics and make png-images

pdftk static/"$base"_sch.pdf burst output static/"$base"_sch_%02d.pdf 

pdfs=static/"$base"_sch_??.pdf
for f in $pdfs
do
    b=${f%.*}
    convert -quality 100 -thumbnail $thumbx $f -compress None \
	    "$b"_thumb.png
    convert  -density 300 -trim $f -quality 100 \
	-background white -flatten -compress None  -rotate "-90"  "$b".png
done
