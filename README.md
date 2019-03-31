* necessary python in the Enviromment Variable

install:
pip install git+https://github.com/huilaribeiro85/cut_video_processor.git


* create a file.py with this content:

from cut_processor.run import Processor
Processor().start_threads()

* The program will create the folders were the videos will be inputed to be cutted.
