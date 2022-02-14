.PHONY: run test
test:
	for f in $$(ls code_examples/); do python3 lexer.py code_examples/$$f > out/$$f.out.txt; done

run:
	python3 python_parser.py test_input.py
