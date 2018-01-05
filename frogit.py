import sublime
import sublime_plugin
import re

# Dictionnary file path
dictionnary = r'C:\My\ENGLISH_FRENCH.md'

class FrogitCommand(sublime_plugin.TextCommand):
	def run(self, edit):				
		translated = ""
		term = ""
		for region in self.view.sel():  #get user selection
			term = self.view.substr(self.view.word(region))
			if len(term) > 2:
				pattern = re.compile("	(" + term + ")[ \t]+(.*)")
				for line in open(dictionnary):
					for match in re.finditer(pattern, line):
						translated += "• " + term + ": " + match.group(2) + '<br>'
				html = """
			    	<body>
			        	<style>
			            	.arrow-down { width: 0; height: 0; border-style: solid; border-width: 7px 5px; border-color: #ffd500 transparent transparent transparent}
			            	div { color: #ffd500; border:solid 1px black; margin-top:-5px}
			        	</style>
			        	<div class="arrow-down"></div>
			        	<div>%s</div>
			    	</body>
				""" % (translated)
				self.view.show_popup(html, max_width=256)

				# Add missing translation in the dictionnay. Todo: Use an api to automatic add the translation in right position
				if (len(translated)=0):
					with open(dictionnary, "a") as f:
						f.write("\r\n"+term)
