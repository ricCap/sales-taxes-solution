SHELL=/bin/sh #Shell da utilizzare per l'esecuzione dei comandi

# if set to @ will hide which command are executed,
# otherwise it will show all executed commands
SILENT = @

help:
	$(SILENT)echo "Rules:"
	$(SILENT)echo	"- help"
	$(SILENT)echo	"\t show this help"
	$(SILENT)echo	"- tests"
	$(SILENT)echo	"\t run tests"

.SILENT: tests

doc:
	$(SILENT)sphinx-apidoc -f -o docs/ src/
	$(SILENT)cd docs && $(MAKE) html

tests:
	$(SILENT)echo ">>> Running tests..."
	$(SILENT)cd test && python -m unittest -v test.py
	$(SILENT)echo ">>> Done!\n"

format:
	$(SILENT)autopep8 -ia --experimental src/*.py 
	$(SILENT)autopep8 -ia --experimental test/*.py 

check_format:
	$(SILENT)pep8 src/*.py
	$(SILENT)pep8 src/*.py

### ===================== ###
###     Clean section     ###
### ===================== ###
# remove generated files
.PHONY: clean

clean:
	$(SILENT)echo ">>> Deleting temporary files..."
	$(SILENT)rm -f ./test/output*
	$(SILENT)echo ">>> Done!"
