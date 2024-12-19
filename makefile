.PHONY: default
default: test

.PHONY: build
build:
	mypyc generate_image.py

.PHONY: test
test: build
	time python -c "import generate_image" -w 4000 -h 1000 -f 0 -t 4 -o output/n000.ppm 

