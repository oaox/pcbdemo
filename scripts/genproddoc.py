#!/usr/bin/python3
# Generates documentation for board assembly

import sys
import csv
from pcbnew import *

FP_EXCLUDE_FROM_BOM         = 0x0008

def format(x):
    if type(x) == str:
        y= float(x)
    else: y= x
    return str(round(y,2))

def format2(x):
    return str(round(x[0],2)) + ' ' +str(round(x[1],2))

def loadPcbFile(basename):
    fname= basename +  '.kicad_pcb'
    pcb= LoadBoard(fname)
    return pcb

def loadComponents(pcb, reflist, compdir):
    for module in pcb.GetFootprints():
        x, y= module.GetPosition()
        rot= module.GetOrientationDegrees()
        ref= module.GetReference()
        value= module.GetValue()
        if  module.IsOnLayer(0):layer='F.Cu'
        else: layer='B.Cu'
        foot= module.GetFPIDAsString()
        value=module.GetValue()
        comp={}
        comp['ref']= ref
        comp['value']= value
        comp['x']= x
        comp['y']= y
        comp['rot']= rot
        comp['layer']= layer
        comp['foot']= foot
        comp['xbomfile']= module.GetAttributes() &  \
            FP_EXCLUDE_FROM_BOM  
        compdir[ref]= comp
        reflist.append(ref)
    reflist.sort()
    
def writePositionFile(basename, reflist, compdir, x0, y0):
    posfile= open("prod/"+basename+'_cpl.csv', 'w')
    posfile.write("Designator, Mid X, Mid Y, Layer, Rotation\n")
    for ref in reflist:
        c=compdir[ref]
        if c['xbomfile'] != 0 : continue
        x= format((c['x'] - x0)*1e-6)
        y= format((y0 - c['y'])*1e-6)
        rot= c['rot']
        if c['layer'] == 'F.Cu': layer= 'top'
        else: layer= 'bottom'
        posfile.write(ref +','+x +','+ y +','+ layer +','+ format(rot) \
                      +','+'\n')
    posfile.close()

def correctRotation(basename, reflist, compdir):
    fn= basename+'_ROT.csv'
    try:
        rotfile= open(fn, 'r')
        rotfile.close()
    except: 
        print ('creates new rot file ')
        rotfile=open(fn, 'w')
        rotfile.write("Ref, Rot\n")
        for ref in reflist:
            if compdir[ref]['xbomfile'] != 0 : continue
            rot= compdir[ref]['rot']
            rotfile.write(ref + ', ' + format(rot) + '\n')
        rotfile.close()
    
    rotfile= open(fn, mode ='r')
    csvData= csv.reader(rotfile)
    for r in csvData:
        if r[0]=='Ref': continue
        ref= r[0]
        rot= r[1]
        if ref in compdir:
            compdir[ref]['rot']=  rot
    rotfile.close()

def writeRotationFile(basename, reflist, compdir):
    fn= basename+'_ROT.csv'
    print ('updates ROT file ')
    rotfile=open(fn, 'w')
    rotfile.write("Ref, Rot\n")
    for ref in reflist:
        if compdir[ref]['xbomfile'] != 0 : continue
        rot= compdir[ref]['rot']
        rotfile.write(ref + ', ' + str(rot) + '\n')
    rotfile.close()
    
def loadBOMFile(basename, pcb, reflist, compdir):
    fn= basename +'_BOM.csv'
    modules=  pcb.GetFootprints()
    try:
        bomfile= open(fn, 'r')
        bomfile.close()
    except: 
        print ('creates new bom file ')
        bomfile=open(fn, 'w')
        bomfile.write("Ref, Value, Vendor, SKU\n")
        for ref in reflist:
            if compdir[ref]['xbomfile'] == 0 :
                value= compdir[ref]['value']
                bomfile.write(ref  +', '+  value +',,\n')
        bomfile.close()
    
    bomfile= open(fn, mode ='r')
    csvData= csv.reader(bomfile)
    for b in csvData:
        if b[0]=='Ref': continue
        ref= b[0]
        value= b[1]
        vendor=b[2]
        sku=b[3]
        if ref in compdir:
            compdir[ref]['value']= value
            compdir[ref]['vendor']= vendor
            compdir[ref]['sku']= sku
        
    bomfile.close()

def writeBOMFile(basename, reflist, compdir):
    fn= basename +'_BOM.csv'
    bomfile=open(fn, 'w')
    print("Updates BOM file")
    bomfile.write("Ref, Value, Vendor, SKU\n")
    for ref in reflist:
        if compdir[ref]['xbomfile']: continue
        value= compdir[ref]['value']
        try:
            vendor= compdir[ref]['vendor']
        except:
            vendor=''
        try:
            sku= compdir[ref]['sku']
        except:
            sku=''
        bomfile.write(ref  +', '+  value +', '+vendor + ', ' +\
                      sku + '\n')
    bomfile.close()
    
def writeBomFiles(basename, reflist, compdir):
    print ("Updates top and bottom BOM files")
    bomfileT= open('prod/'+basename+'_bom_T.csv', 'w')
    bomfileB= open('prod/'+basename+'_bom_B.csv', 'w')
    bomfileT.write("Ref, Value, Footprint, Vendor, SKU\n")
    bomfileB.write("Ref, Value, Footprint, Vendor, SKU\n")
    
    for ref in reflist:
        if compdir[ref]['xbomfile'] != 0: continue
        part= compdir[ref]
        value= part['value'].strip()
        footprint= part['foot'].split(':')[1]
        try: 
            vendor= part['vendor']
        except:
            vendor= ''
        try:
            sku=part['sku']
        except:
            sku= ''
        layer= part['layer']
        if part['xbomfile'] == 0:
            if layer=='F.Cu':
                bomfileT.write(ref+','+ value+','+footprint+','\
                               +vendor+','+sku+'\n') 
            else:bomfileB.write(ref+','+ value+','+footprint+','\
                          +vendor+','+sku+'\n') 
    bomfileT.close()
    bomfileB.close()
    
def writeGroupedBomFile(basename, reflist, compdir):
    readLines= []
    groupLines= []
    firstList=[]
    print ("Updates grouped BOM file")
    for layer in ('T','B'):
        fn= 'prod/' + basename + '_bom_' + layer + '.csv'
        bomfile= open(fn, mode ='r')
        csvData= csv.reader(bomfile)
        for b in csvData:
            line={}
            if b[0]=='Ref': continue
            ref= b[0]
            value= b[1]
            footprint= b[2]
            vendor=b[3]
            sku=b[4]
            line['valuefoot']=value+footprint
            line['ref']= ref
            line['value']= value
            line['footprint']= footprint
            line['vendor']= vendor
            line['sku']= sku
            line['consumed']= False
            readLines.append(line)
        bomfile.close()
        
    for c in readLines:
        if c['consumed']: continue
        for g in groupLines:
            if g['valuefoot'] == c['valuefoot']:
                g['reflist'].append(c['ref'])
                c['consumed'] =True
                break
        if c['consumed']: continue
        a= {}
        a['reflist']= []
        a['reflist'].append(c['ref'])
        a['valuefoot']= c['valuefoot']
        a['vendor']= c['vendor']
        a['sku']= c['sku']
        c['consumed']= True
        groupLines.append(a)
        
    for g in groupLines:
        g['reflist'].sort()
        firstList.append(g['reflist'][0])
    firstList.sort()

    of= open('prod/' + basename + '_bom_G.csv', 'w')
    of.write("References:Value:Footprint:Quantity:Vendor:SKU\n") 
    for f in firstList:
        for g in groupLines:
            gfirst= g['reflist'][0]
            if gfirst == f:
                for e in readLines:
                    if gfirst == e['ref']:
                        break
                s=''
                for r in g['reflist']: s=s+r+', '
                of.write(s[:-1]+':'+e['value']+':'+e['footprint']+':'+\
                         str(len(g['reflist']))+':'+e['vendor']+':'+\
                         e['sku']+'\n')
                break
    of.close()
 
#--------------------------------    

basename= sys.argv[1]
compdir= {}
reflist= []

pcb= loadPcbFile(basename)
loadComponents(pcb, reflist, compdir)
settings= pcb.GetDesignSettings()
x0,y0= settings.GetAuxOrigin()
print ('origin: ', format2((float(x0)*1e-6,float(y0)*1e-6)))
correctRotation(basename, reflist, compdir)

writePositionFile(basename, reflist, compdir, x0, y0) 
loadBOMFile(basename, pcb,reflist, compdir)
writeBomFiles(basename, reflist, compdir)
writeGroupedBomFile(basename, reflist, compdir)
writeRotationFile(basename, reflist, compdir)
writeBOMFile(basename, reflist, compdir)
