embroider.tgz: makefile index.html embroider.py embroider.inx images/draft1.jpg images/draft2.jpg images/shirt.jpg PyEmb.py
	ln -fs embroider .
	tar czf $@ $^
