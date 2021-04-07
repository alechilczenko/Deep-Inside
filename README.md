# Deep Inside 👁

Deep Inside is a simple command line tool designed in Python that allows you to explore IoT devices by using Shodan search engine, with multiple options. 

For use special modes and get more results from different pages you should have a pay API key.

![Screenshot](https://img.shields.io/badge/Platform-Linux-brightgreen)
![Screenshot](https://img.shields.io/badge/License-GPL-red)
![Screenshot](https://img.shields.io/badge/Language-Python%203-blue)
![Screenshot](/Screenshots/screen.png)

## Features
- [x] Search randomly by country.
- [x] Display and save collected data with [IP:PORT] format.
- [x] Search by page and set quantity of results.
- [x] Automatically save data with current time.
- [x] Easy to see results from terminal directly in browser. (Recommended for HTTP ports)
- [ ] Save data as HTML report.  

## Examples of usage
```python
python3 deep-inside.py
python3 deep-inside.py -R -L 500 -P 2
python3 deep-inside.py -R -S
```
![Screenshot](/Screenshots/screen1.png)
## Installation
```
git clone https://github.com/intrackeable/DeepInside.git
cd DeepInside 
pip install -r requirements.txt
python3 deep-inside.py -h
```

## Attention
This project was created for educational purposes and should not be used in environments without legal authorization.
## References
 * [Shodan](https://www.shodan.io/)
 * [The official Python library for the Shodan search engine](https://shodan.readthedocs.io/en/latest/)
 * [Awesome Shodan Queries](https://github.com/jakejarvis/awesome-shodan-queries)
