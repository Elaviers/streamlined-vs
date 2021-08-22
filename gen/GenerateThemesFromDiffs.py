import copy
import os
import xml.etree.ElementTree as etree
from typing import List

filedir = os.path.dirname(__file__)

def applyDiffToCategories(diff: etree.ElementTree, dest: etree.ElementTree):
    categories = dest.findall('.//Category')
    for category in categories:
        guid = category.get('GUID')
        dcategory = diff.find(f'.//Category[@GUID=\'{guid}\']')
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

def GenThemeFile(diffFile: str):
    dfile = os.path.join(filedir, os.path.join(filedir, diffFile))
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
        
        runs = theme.findall('Run')
        for run in runs:
            tree = etree.parse(os.path.join(filedir, run.text))
            applyDiffToCategories(tree, out)

        applyDiffToCategories(dtree, out)
        out.write(outfile)

GenThemeFile('diff/ThemeDiff.xml')
