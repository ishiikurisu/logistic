.PHONY: default
default: test

.PHONY: build
build:
	mypyc generate_image.py
	mypyc generate_inputs.py

.PHONY: test
test: build
	time python -c "import generate_image" -w 4000 -h 1000 -f 0 -t 4 -o output/n000.ppm

.PHONY: frames
frames: build
	time python -c "import generate_inputs" context.json | parallel

.PHONY: video
video: frames
	ffmpeg -framerate 12 -pattern_type glob -i 'output/*.ppm' -c:v libx264 -r 30 -pix_fmt yuv420p output/logistic.mp4

