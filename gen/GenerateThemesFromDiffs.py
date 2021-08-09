import copy
import os
import xml.etree.ElementTree as etree

filedir = os.path.dirname(__file__)

dfile = os.path.join(filedir, os.path.join(filedir, 'ThemeDiff.xml'))
dtree = etree.parse(dfile)
themes = dtree.findall('Theme')

for theme in themes:
    basefile = os.path.join(filedir, theme.get('Input'))
    basetree = etree.parse(basefile)

    outfile = os.path.join(filedir, theme.get('Output'))
    out = copy.deepcopy(basetree)

    otheme = out.find('Theme')
    otheme.set('Name', theme.get('Name'))
    otheme.set('GUID', theme.get('GUID'))
    otheme.set('BaseGUID', theme.get('BaseGUID'))
    
    categories = out.findall('.//Category')
    for category in categories:
        guid = category.get('GUID')
        dcategory = dtree.find(f'.//Category[@GUID=\'{guid}\']')
        if dcategory != None:
            colours = category.findall('Color')
            for colour in colours:
                name = colour.get('Name')
                dcolour = dcategory.find(f'Item[@Name=\'{name}\']')
                if dcolour != None:
                    dforeground = dcolour.get('Foreground')
                    dbackground = dcolour.get('Background')

                    if dforeground != None: colour.find('Foreground').set('Source', dforeground)
                    if dbackground != None: colour.find('Background').set('Source', dbackground)

                    print(name)

    out.write(outfile)
