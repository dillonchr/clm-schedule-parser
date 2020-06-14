# CLM Schedule Parser

I have a cheap thermal printer that I can just pipe text into and it prints right out.

This is a script used in conjunction with another script that creates a somewhat sensible way to keep track of who's up next during the meeting. Handy for running sound.

As of now, here's how it works, don't laugh, I'm serious.

1. Download PDF version of schedule
2. Use imagemagick to create bitmaps `convert -density 300 schedule.pdf schedule.png`
3. Use tesseract to OCR all text out `for f in schedule-*.png; do tesseract $f - >>text.out.txt; done`
4. Connect all the pipes: `cat text.out.txt | python read.py | python ~/git/receiptprinter/print.py`
