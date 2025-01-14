#MenuTitle: Webfont Test HTML
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Create a Test HTML for the current font inside the current Webfont Export folder, or for the current Glyphs Project in the project’s export path.
"""

from AppKit import NSBundle, NSClassFromString
from os import system

Glyphs.registerDefault( "com.mekkablue.WebFontTestHTML.includeEOT", 0 )
if Glyphs.defaults["com.mekkablue.WebFontTestHTML.includeEOT"]:
	fileFormats = ( "woff", "woff2", "eot" )
else:
	fileFormats = ( "woff", "woff2" )

def saveFileInLocation( content="blabla", fileName="test.txt", filePath="~/Desktop" ):
	saveFileLocation = "%s/%s" % (filePath,fileName)
	saveFileLocation = saveFileLocation.replace( "//", "/" )
	f = open( saveFileLocation, 'w' )
	print("Exporting to:", f.name)
	f.write( content )
	f.close()
	return True

def currentWebExportPath():
	exportPath = Glyphs.defaults["WebfontPluginExportPathManual"]
	if Glyphs.defaults["WebfontPluginUseExportPath"]:
		exportPath = Glyphs.defaults["WebfontPluginExportPath"]
	return exportPath

def replaceSet( text, setOfReplacements ):
	for thisReplacement in setOfReplacements:
		searchFor = thisReplacement[0]
		replaceWith = thisReplacement[1]
		text = text.replace( searchFor, replaceWith )
	return text

def allUnicodeEscapesOfFont( thisFont ):
	allUnicodes = ["&#x%s;" % g.unicode for g in thisFont.glyphs if g.unicode and g.export ]
	return " ".join( allUnicodes )

def getInstanceInfo( thisFont, activeInstance, fileFormat ):
	# Determine Family Name
	familyName = thisFont.familyName
	individualFamilyName = activeInstance.customParameters["familyName"]
	if individualFamilyName != None:
		familyName = individualFamilyName
	
	# Determine Style Name
	activeInstanceName = activeInstance.name
	
	# Determine font and file names for CSS
	menuName = "%s %s-%s" % ( fileFormat.upper(), familyName, activeInstanceName )
	
	firstPartOfFileName = activeInstance.customParameters["fileName"]
	if not firstPartOfFileName:
		firstPartOfFileName = "%s-%s" % ( familyName.replace(" ",""), activeInstanceName.replace(" ","") )
		
	fileName = "%s.%s" % ( firstPartOfFileName, fileFormat )
	return fileName, menuName, activeInstanceName

def activeInstancesOfFont( thisFont, fileFormats=fileFormats ):
	activeInstances = [i for i in thisFont.instances if i.active]
	listOfInstanceInfo = []
	for fileFormat in fileFormats:
		for activeInstance in activeInstances:
			fileName, menuName, activeInstanceName = getInstanceInfo(thisFont, activeInstance, fileFormat)
			listOfInstanceInfo.append( (fileName, menuName, activeInstanceName) )
	return listOfInstanceInfo

def activeInstancesOfProject( thisProject, fileFormats=fileFormats ):
	thisFont = thisProject.font()
	activeInstances = [i for i in thisProject.instances() if i.active]
	listOfInstanceInfo = []
	for fileFormat in fileFormats:
		for activeInstance in activeInstances:
			fileName, menuName, activeInstanceName = getInstanceInfo(thisFont, activeInstance, fileFormat)
			listOfInstanceInfo.append( (fileName, menuName, activeInstanceName) )
	return listOfInstanceInfo

def optionListForInstances( instanceList ):
	returnString = ""
	for thisInstanceInfo in instanceList:
		returnString += '		<option value="%s">%s</option>\n' % ( thisInstanceInfo[0], thisInstanceInfo[1] )
		# <option value="fileName">baseName</option>
	
	return returnString

def fontFaces( instanceList ):
	returnString = ""
	for thisInstanceInfo in instanceList:
		fileName = thisInstanceInfo[0]
		nameOfTheFont = thisInstanceInfo[1]
		returnString += "\t\t@font-face { font-family: '%s'; src: url('%s'); }\n" % ( nameOfTheFont, fileName )
	
	return returnString

def featureListForFont( thisFont ):
	returnString = ""
	featureList = [f.name for f in thisFont.features if not f.name in ("ccmp", "aalt", "locl", "kern", "calt", "liga", "clig") and not f.disabled()]
	for f in featureList:
		returnString += """		<label><input type="checkbox" id="%s" value="%s" class="otFeature" onchange="updateFeatures()"><label for="%s" class="otFeatureLabel">%s</label>
""" % (f,f,f,f)
	return returnString

htmlContent = """<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=9">
	<title>familyName</title>
	<style type="text/css" media="screen">
		<!-- fontFaces -->
		
		body { 
			font-family: "nameOfTheFont"; 
			font-feature-settings: "kern" on, "liga" on, "calt" on;
			-moz-font-feature-settings: "kern" on, "liga" on, "calt" on;
			-webkit-font-feature-settings: "kern" on, "liga" on, "calt" on;
			-ms-font-feature-settings: "kern" on, "liga" on, "calt" on;
			-o-font-feature-settings: "kern" on, "liga" on, "calt" on;
		}
		p {
			padding: 5px;
			margin: 10px; 
		}
		.features, .label, a {
			font-size: small;
			font-family: sans-serif;
			color: #888;
		}
		.label {
			background: #ddd;
			padding: 2px 3px;
		}
		
		span#p08 { font-size: 08pt; }
		span#p09 { font-size: 09pt; }
		span#p10 { font-size: 10pt; }
		span#p11 { font-size: 11pt; }
		span#p12 { font-size: 12pt; }
		span#p13 { font-size: 13pt; }
		span#p14 { font-size: 14pt; }
		span#p15 { font-size: 15pt; }
		span#p16 { font-size: 16pt; }
		span#largeParagraph { font-size: 32pt; }
		span#veryLargeParagraph { font-size: 100pt; }
		
		.otFeatureLabel {
			color: #666;
			background-color: #ddd;
			padding: 0.2em 0.5em 0.3em 0.5em;
			margin: 0 .04em;
			line-height: 2em;
			border-radius: 0.3em;
			border: 0;
			text-align:center;
		}
		input[type=checkbox]:checked + label { 
			visibility: visible;
			color: #fff;
			background-color: #888; 
		}
		.otFeature {
			visibility: collapse;
			margin: 0 -1em 0 0;
		}
		
		@media (prefers-color-scheme: dark) {
			body { 
				background: #333;
				color: #fff;
			}
			.features, .label, a  {
				color: #fff;
			}
			.label {
				background: #000;
				padding: 2px 3px;
			}
			.otFeatureLabel {
				color: #999;
				background-color: #000;
			}
			input[type=checkbox]:checked + label { 
				color: #000;
				background-color: #aaa; 
			}
		}
			
	</style>
	<script type="text/javascript">
		function updateParagraph() {
			// update paragraph text based on user input:
			var txt = document.getElementById('textInput');
			var paragraphs = ['p08','p09','p10','p11','p12','p13','p14','p15','p16','largeParagraph','veryLargeParagraph'];
			for (i = 0; i < paragraphs.length; i++) {
				paragraphID = paragraphs[i];
				var paragraph = document.getElementById(paragraphID);
				paragraph.textContent = txt.value;
			}
		}
		function updateFeatures() {
			// update features based on user input:
			// first, get feature on/off line:
			var cssCode = "";
			var codeLine = "";
			var checkboxes = document.getElementsByClassName("otFeature")
			for (i = 0; i < checkboxes.length; i++) {
				var checkbox = checkboxes[i];
				codeLine += '"'+checkbox.id+'" ';
				codeLine += checkbox.checked ? 'on, ' : 'off, ';
				if (checkbox.name=="kern") {
					cssCode += "font-kerning: "
					cssCode += checkbox.checked ? 'normal; ' : 'none; ';
				} else if (checkbox.name=="liga") {
					codeLine += '"clig" '
					codeLine += checkbox.checked ? 'on, ' : 'off, ';
					cssCode += "font-variant-ligatures: "
					cssCode += checkbox.checked ? 'common-ligatures contextual; ' : 'no-common-ligatures no-contextual; ';
				} else if (checkbox.name=="dlig") {
					cssCode += "font-variant-ligatures: "
					cssCode += checkbox.checked ? 'discretionary-ligatures; ' : 'no-discretionary-ligatures; ';
				} else if (checkbox.name=="hlig") {
					cssCode += "font-variant-ligatures: "
					cssCode += checkbox.checked ? 'historical-ligatures; ' : 'no-historical-ligatures; ';
				}
			}
			codeLine = codeLine.slice(0, -2)
			
			// then, apply line for every browser:
			var prefixes = ["","-moz-","-webkit-","-ms-","-o-",];
			var suffix = "font-feature-settings: "
			for (i = 0; i < prefixes.length; i++) {
				var prefix = prefixes[i];
				cssCode += prefix
				cssCode += suffix
				cssCode += codeLine
				cssCode += "; "
			}
			
			document.getElementById('fontTestBody').style.cssText = cssCode;
			document.getElementById('featureLine').innerHTML = cssCode.replace(/;/g,";<br/>");
			changeFont();
		}
		function changeFont() {
			var selector = document.getElementById('fontFamilySelector');
			var selected_index = selector.selectedIndex;
			var selected_option_text = selector.options[selected_index].text;
			document.getElementById('fontTestBody').style.fontFamily = selected_option_text;
		}
		function setDefaultText(defaultText) {
			document.getElementById('textInput').value = decodeEntities(defaultText);
			updateParagraph();
		}
		function setLat1() {
			var lat1 = "abcdefghijklm nopqrstuvwxyz ABCDEFGHIJKLM NOPQRSTUVWXYZ &Agrave;&Aacute;&Acirc;&Atilde;&Auml;&Aring;&AElig;&Ccedil;&Egrave;&Eacute;&Ecirc;&Euml;&Igrave;&Iacute;&Icirc;&Iuml;&ETH;&Ntilde;&Ograve;&Oacute;&Ocirc;&Otilde;&Ouml;&Oslash;&OElig;&THORN;&Ugrave;&Uacute;&Ucirc;&Uuml;&Yacute;&Yuml; &agrave;&aacute;&acirc;&atilde;&auml;&aring;&aelig;&ccedil;&egrave;&eacute;&ecirc;&euml;&igrave;&iacute;&icirc;&iuml;&eth;&ntilde;&ograve;&oacute;&ocirc;&otilde;&ouml;&oslash;&oelig;&thorn;&szlig;&ugrave;&uacute;&ucirc;&uuml;&yacute;&yuml; .,:;&middot;&hellip;&iquest;?&iexcl;!&laquo;&raquo;&lsaquo;&rsaquo; /|&brvbar;\\()[]{}_-&ndash;&mdash;&sbquo;&bdquo;&lsquo;&rsquo;&ldquo;&rdquo;&quot;&#x27; #&amp;&sect;@&bull;&shy;*&dagger;&Dagger;&para; +&times;&divide;&plusmn;=&lt;&gt;&not;&mu; ^~&acute;`&circ;&macr;&tilde;&uml;&cedil; &yen;&euro;&pound;$&cent;&curren;&fnof; &trade;&reg;&copy; 1234567890 &ordf;&ordm;&deg;%&permil; &sup1;&sup2;&sup3;&frac14;&frac12;&frac34;";
			return setDefaultText(lat1);
		}
		function setCharset() {
			var completeCharSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
			setDefaultText(completeCharSet);
		}
		function decodeEntities(string){
			var elem = document.createElement('div');
			elem.innerHTML = string;
			return elem.textContent;
		}
	</script>
</head>
<body id="fontTestBody">
	<select size="1" id="fontFamilySelector" name="fontFamilySelector" onchange="changeFont()">
		<!-- moreOptions -->
	</select>
	<input type="text" value="Type Text Here." id="textInput" onclick="this.select();" onkeyup="updateParagraph()" size="100%" />
	<p class="features">
		<a href="javascript:setCharset();">Charset</a>
		<a href="javascript:setLat1();">Lat1</a>
		&emsp;
		<a href="https://caniuse.com/#feat=eot">eot</a>
		<a href="https://caniuse.com/#feat=woff">woff</a>
		<a href="https://caniuse.com/#feat=woff2">woff2</a>
		&emsp;
		OT Features:
		<label><input type="checkbox" id="kern" value="kern" class="otFeature" onchange="updateFeatures()" checked><label for="kern" class="otFeatureLabel">kern</label>
		<label><input type="checkbox" id="liga" value="liga" class="otFeature" onchange="updateFeatures()" checked><label for="liga" class="otFeatureLabel">liga/clig</label>
		<label><input type="checkbox" id="calt" value="calt" class="otFeature" onchange="updateFeatures()" checked><label for="calt" class="otFeatureLabel">calt</label>
		<!-- moreFeatures -->
		<label><input type="checkbox" id="show" value="show" onchange="updateFeatures();document.getElementById('featureLine').style.display=this.checked?'':'none'">Show CSS</label>
	</p>
	<p class="features" id="featureLine" style="display:none;">font-feature-settings: "kern" on, "liga" on, "calt" on;</p>
	<p><span class="label">08</span> <span id="p08">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">09</span> <span id="p09">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">10</span> <span id="p10">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">11</span> <span id="p11">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">12</span> <span id="p12">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">13</span> <span id="p13">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">14</span> <span id="p14">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">15</span> <span id="p15">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span class="label">16</span> <span id="p16">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span id="largeParagraph">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
	<p><span id="veryLargeParagraph">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span></p>
</body>
"""

# brings macro window to front and clears its log:
Glyphs.clearLog()
Glyphs.showMacroWindow()

# Query app version:
GLYPHSAPPVERSION = NSBundle.bundleForClass_(NSClassFromString("GSMenu")).infoDictionary().objectForKey_("CFBundleShortVersionString")
appVersionHighEnough = not GLYPHSAPPVERSION.startswith("1.")

if appVersionHighEnough:
	firstDoc = Glyphs.orderedDocuments()[0]
	if firstDoc.isKindOfClass_(GSProjectDocument):
		# Frontmost doc is a .glyphsproject file:
		thisFont = firstDoc.font() # frontmost project file
		firstActiveInstance = [i for i in firstDoc.instances() if i.active][0]
		activeFontInstances = activeInstancesOfProject( firstDoc )
		exportPath = firstDoc.exportPath()
	else:
		# Frontmost doc is a .glyphs file:
		thisFont = Glyphs.font # frontmost font
		firstActiveInstance = [i for i in thisFont.instances if i.active][0]
		activeFontInstances = activeInstancesOfFont( thisFont )
		exportPath = currentWebExportPath()
		
		
	familyName = thisFont.familyName
	
	print("Preparing Test HTML for:")
	for thisFontInstanceInfo in activeFontInstances:
		print("  %s" % thisFontInstanceInfo[1])
	
	optionList = optionListForInstances( activeFontInstances )
	fontFacesCSS = fontFaces( activeFontInstances )
	firstFileName =  activeFontInstances[0][0]
	firstFontName =  activeFontInstances[0][1]

	replacements = (
		( "familyName", familyName ),
		( "nameOfTheFont", firstFontName ),
		( "ABCDEFGHIJKLMNOPQRSTUVWXYZ", allUnicodeEscapesOfFont(thisFont) ),
		( "fileName", firstFileName ),
		( "		<!-- moreOptions -->\n", optionList ),
		( "		<!-- moreFeatures -->\n", featureListForFont(thisFont) ),
		( "		<!-- fontFaces -->\n", fontFacesCSS  )
	)

	htmlContent = replaceSet( htmlContent, replacements )
	
	# Write file to disk:
	if exportPath:
		if saveFileInLocation( content=htmlContent, fileName="fonttest.html", filePath=exportPath ):
			print("Successfully wrote file to disk.")
			terminalCommand = 'cd "%s"; open .' % exportPath
			system( terminalCommand )
		else:
			print("Error writing file to disk.")
	else:
		Message( 
			title="Webfont Test HTML Error",
			message="Could not determine export path. Have you exported any webfonts yet?",
			OKButton=None
		)
else:
	print("This script requires Glyphs 2. Sorry.")
