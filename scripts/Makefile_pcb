BASE=pcbdemo
SCRIPT=../../scripts/genproddoc.py $(BASE)
PCB=$(BASE).kicad_pcb
BOM_MOD=$(BASE)_BOM.csv
ROT_MOD=$(BASE)_ROT.csv
BOM_TOP=prod/$(BASE)_bom_T.csv
BOM_BOTT=prod/$(BASE)_bom_B.csv
BOM_ALL=prod/$(BASE)_bom_G.csv
CPL=prod/$(BASE)_cpl.csv


all:$(BOM_MOD) $(ROT_MOD) $(BOM_TOP) $(BOM_BOTT) $(BOM_ALL) $(CPL)


$(BOM_TOP) $(BOM_BOTT) $(BOM_ALL) $(CPL): csv.intermediate
.INTERMEDIATE: csv.intermediate
csv.intermediate: $(BOM_MOD) $(ROT_MOD)
	mkdir -p prod
	mkdir -p doc
	$(SCRIPT)
$(BOM_MOD) $(ROT_MOD): mod.intermediate
.INTERMEDIATE:mod.intermediate
mod.intermediate: $(PCB)
	$(SCRIPT)

#$(BOM_MOD): $(PCB)
#	$(SRIPT)
#$(ROT_MOD): $(PCB)
#	$(SCRIPT)

cleancsv:
	rm -f prod/*.csv 

zip:
	rm -f prod/$(BASE).zip
	zip -j prod/$(BASE).zip gerb/*	
