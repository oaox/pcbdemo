
BASE=pcbdemo

all:doc pdf html
pdf: $(BASE).pdf
html:html/$(BASE).html
doc:
	mkdir -p static html/static
	../../scripts/genboarddoc.sh $(BASE)
	#cut -d';' -f2,4,5 ../pcb/doc/$(BASE)_bom.csv | \
	#sed s/\"//g  | sed s/\;/\:/g  | \
	#sed s/,/,\ /g > static/$(BASE)_bom.csv

$(BASE).pdf:$(BASE).adoc static/*.png
	a2x   $(BASE).adoc
html/$(BASE).html:$(BASE).adoc static/*.png  static/*.pdf
	mkdir -p static
	cp static/*.png html/static
	cp static/*.pdf html/static
	cp $(BASE).pdf html/static
	asciidoctor -Dhtml $(BASE).adoc 

