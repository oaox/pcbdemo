
BASE=pcbdemo
PDF=$(BASE).pdf
HTML=html/$(BASE).html

all:doc $(PDF) $(HTML)

doc:
	$(info doc***) 
	mkdir -p static
	../../scripts/genboarddoc.sh $(BASE)
	cut -d';' -f2,4,5 ../pcb/prod/$(BASE)_bom_G.csv | \
	sed s/\"//g  | sed s/\;/\:/g  | \
	sed s/,/,\ /g > static/$(BASE)_bom.csv

$(PDF):$(BASE).adoc
	$(info pdf***) 
	a2x   $(BASE).adoc
$(HTML):$(BASE).adoc
	$(info html***) 
	mkdir -p static html/static
	cp static/*.png html/static
	cp static/*.pdf html/static
	cp $(BASE).pdf html/static
	asciidoctor -Dhtml $(BASE).adoc 

clean:
	rm -rf $(BASE).pdf
	rm -rf html
	rm -rf static

