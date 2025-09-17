NAME := main

pdf: 
	latexmk -f -shell-escape -bibtex -pdf $(NAME)
	rm -f $(NAME).{ps,log,lot,lof,toc,out,dvi,bbl,blg} *.aux

clean:
	ls $(NAME)* | grep -v ".tex" | grep -v ".bib" | xargs rm -f
	rm -f *.bak *~
	rm -f $(NAME).fdb_latexmk
