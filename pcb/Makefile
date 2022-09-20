BASE=pcbdemo
SCRIPT=../../scripts/gendoc.py $(BASE) 

all:  prod/$(BASE)_cpl.csv


prod/$(BASE)_cpl.csv:  $(BASE).kicad_pcb $(BASE)_ROT.csv $(BASE)_BOM.csv
	rm -f prod/$(BASE)_bom_T.csv
	rm -f prod/$(BASE)_bom_B.csv
	rm -f prod/$(BASE)_bom_G.csv
	rm -f prod/$(BASE)_cpl.cvs
	$(SCRIPT)

$(BASE)_ROT.csv: 
	$(SRIPT)

$(BASE)_BOM.csv: 
	$(SCRIPT)
