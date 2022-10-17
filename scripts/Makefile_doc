
BASE=pcbdemo

all:doc 

doc:
#       copy and arrange files
	mkdir -p static
	../../scripts/genboarddoc.sh $(BASE)
#       Extract some columns, remove "", ;->:, , ->,<space>
	cut -d';' -f2,4,5 ../pcb/prod/$(BASE)_bom_G.csv | \
	sed s/\"//g  | sed s/\;/\:/g  | \
	sed s/,/,\ /g > static/$(BASE)_bom.csv
#	generate html
	mkdir -p static html/static
	cp static/*.png html/static
	cp static/*.pdf html/static
	asciidoctor -Dhtml $(BASE).adoc 
#	generate pdf
	prince html/$(BASE).html -o $(BASE).pdf

clean:
	rm -rf $(BASE).pdf
	rm -rf html
	rm -rf static

