from IPython.core.display import HTML

def style_nb(path):
	styles = open(path, "r").read()
	return HTML("""<style>{}<style>""".format(styles))

