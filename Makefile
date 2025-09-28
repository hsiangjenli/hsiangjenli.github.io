PYTHON := $(shell command -v python3 2>/dev/null || command -v python)

html:
	uv run auto.py --dev True
	cp -r static/* hsiangjenli.github.io/static

gpa:
	$(PYTHON) core/gpa.py \
		--input config/gpa.xlsx \
		--sheet NTUST-CSIE \
		--bg-logo https://hsiangjenli.github.io/static/image/ntust.png\
		--gpa 4.3 \
		--university "National Taiwan University of Science and Technology" \
		--major "Department of Computer Science and Information Engineering" \
		--std_id "M11101T04" \
		--std_name "Hsiang-Jen, Li" \
		--output static/output/ntust.html

	python3 core/gpa.py \
		--input config/gpa.xlsx \
		--sheet NKUST-DMB \
		--bg-logo https://hsiangjenli.github.io/static/image/nkust.png\
		--gpa 4.3 \
		--university "National Kaohsiung University of Science and Technology" \
		--major "Department of Money and Banking" \
		--std_id "C107125248" \
		--std_name "Hsiang-Jen, Li" \
		--output static/output/nkust.html

	weasyprint static/output/ntust.html static/pdf/transcript_ntust.pdf
	weasyprint static/output/nkust.html static/pdf/transcript_nkust.pdf

cv:
	python auto.py --dev True
	docker run -it --rm -v "$(PWD):/workspace" hsiangjenli/xelatex:ntust-thesis-v1.8.1 xelatex cv_eng.tex
	# weasyprint static/output/cv_eng.html -s static/css/cv.css static/pdf/cv_eng.pdf
	# weasyprint static/output/cv_zh_tw.html -s static/css/cv.css static/pdf/cv_zh_tw.pdf

push:
	git pull origin html5
	rm -rf hsiangjenli.github.io
	git clone https://github.com/hsiangjenli/hsiangjenli.github.io.git
	git add .
	git commit -m "feat: update template"
	git push origin html5