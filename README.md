# RDB

[![PyPi](https://img.shields.io/badge/pypi-v21.0-blue)](https://pypi.org/project/pip/)
[![Python](https://img.shields.io/pypi/pyversions/django.svg)](https://pypi.org/pypi/django/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/pypi/status/django.svg)](https://pypi.org/pypi/django/)
 
Search through 1400+ Yale faculty listings across 60+ fields of study. Learn about professors who share your research interests and find potential research mentors.

## Important Notes

If this section is here, there is currently a free remote database hooked up to the project. This is just to promote faster setup, if you have a local postgres server setup, please comment out the remote one in the `settings.py` database section.

`secrets.json` is currently hidden, please reach out to recieve the file.
 
## macOS Setup

To make sure you're using the correct python version and to promote best practices, please follow the tutorial [here](https://github.com/pyenv/pyenv/blob/master/README.md) to install pyenv (if you already have python3 installed, feel free to skip).

1. Clone the repo
`git clone https://github.com/DanielKim0/RDB.git`
2. Change directories and create virtual python environment
`cd RDB && python -m venv .env`
3. Source environment
`source .env/bin/activate`
4. Install requirements
`pip install -r requirements.txt`
5. Run server
`python manage.py runserver`

## Windows Setup

1. Clone the repo
`git clone https://github.com/DanielKim0/RDB.git`
2. Change directories
`cd RDB`
3. Create virtual python environment
`py -m venv .env`
4. Source environment using a batch file
`.env\scripts\activate.bat`
5. Install requirements
`pip install -r requirements.txt`
6. Run server
`py manage.py runserver`
 
## License
 
The MIT License (MIT)

Copyright (c) 2021 Yale Undergraduate Research Association

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
