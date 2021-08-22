import os
import xml.etree.ElementTree as etree
from typing import List

def genDiffFile(diffFrom: str, diffTo: str, diffOut: str, themes: List[tuple]):
	filedir = os.path.dirname(__file__)
	basefile = os.path.join(filedir, diffFrom)
	baseroot = etree.parse(basefile).getroot()
	basetheme = baseroot.find('Theme')

	themefile = os.path.join(filedir, diffTo)
	themeroot = etree.parse(themefile).getroot()
	theme = themeroot.find('Theme')

	outfile = os.path.join(filedir, diffOut)
	outDiff = etree.Element('ThemeDiff')
	outroot = etree.ElementTree(outDiff)

	for reftheme in themes:
		themeref = etree.SubElement(outDiff, 'Theme')
		themeref.attrib = etree.parse(os.path.join(filedir, reftheme[0])).find('Theme').attrib
		themeref.set('Input', reftheme[1])
		themeref.set('Output', reftheme[0])

		for i in range(2, len(reftheme)):
			etree.SubElement(themeref, 'Run').text = reftheme[i]

	categories = theme.findall('Category')
	for category in categories:
		guid = category.get('GUID')
		basecategory = basetheme.find(f'Category[@GUID=\'{guid}\']')
		outCategory = None

		if basecategory != None:
			colours = category.findall('Color')
			for colour in colours:
				name = colour.get('Name')
				basecolour = basecategory.find(f'Color[@Name=\'{name}\']')

				skip1 = skip2 = True
				fg = colour.find('Foreground')
				if fg != None:
					fg = fg.get('Source')

					if basecolour != None:
						basefg = basecolour.find('Foreground')
						skip1 = basefg != None and basefg.get('Source') == fg

				bg = colour.find('Background')
				if bg != None:
					bg = bg.get('Source')

					if basecolour != None:
						basebg = basecolour.find('Background')
						skip2 = basebg != None and basebg.get('Source') == bg
				
				if basecolour == None:
					print(f'Error: Colour \"{name}\" is not in base!')
				elif skip1 and skip2:
					continue

				#colour is changed, add it to our thing
				if outCategory == None:
					outCategory = etree.SubElement(outDiff, 'Category', {'Name': category.get('Name'), 'GUID': guid})

				item = etree.SubElement(outCategory, 'Item', {'Name': name })
				if fg != None: item.set('Foreground', fg)
				if bg != None: item.set('Background', bg)

				print(name)

	outroot.write(outfile)

############
############
############
############
############
############

genDiffFile('base/Dark.xml', 'Streamlined.vstheme', 'diff/ThemeDiff.xml', [
	('Streamlined.vstheme', 'base/Dark.xml'),
	('StreamlinedGreen.vstheme', 'base/Dark.xml', 'diff/GreenDiff.xml', 'diff/GreenDiff_CommonElements.xml')
])

#
# Regens GreenDiff.xml
#  vvvv
#genDiffFile('base/Dark.xml', 'base/DarkGreen.xml', 'diff/GreenDiff.xml', [])
#

genDiffFile('base/Dark.xml', 'base/DarkGreen_CommonElements.xml', 'diff/GreenDiff_CommonElements.xml', [])
