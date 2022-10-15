#!/bin/sh
# Generates html and pdf documentation of the board

base=$1
thumbx=100

#Run from doc folder make file

# First copy files
mkdir -p static
cp ../pcb/doc/* static
cp ../pcb/prod/*.csv static
rm -f static/doc_data.txt

#crop top and bottom images
mogrify -trim -fuzz 10% static/"$base"_brd*


# make thumbs of images
convert -resize $thumbx  static/"$base"_brd_top.png \
	static/"$base"_brd_top_thumb.png 

if [ -f static/"$base"_brd_bottom.png ]; then
    convert -resize $thumbx static/"$base"_brd_bottom.png \
	    static/"$base"_brd_bottom_thumb.png
fi


#then split schematics and make png-images

pdftk static/"$base".pdf burst output static/"$base"_sch_%02d.pdf 

pdfs=static/"$base"_sch_??.pdf
for f in $pdfs
do
    b=${f%.*}
    convert -quality 100 -thumbnail $thumbx $f -compress None \
	    "$b"_thumb.png
    convert  -density 300 -trim $f -quality 100 \
	-background white -flatten -compress None  -rotate "-90"  "$b".png
done
