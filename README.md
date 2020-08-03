# Deep Inside 👁

Deep Inside is a command line tool designed in Python3 that allows you to explore IoT devices by using Shodan search engine, with multiple options.  
For use special modes and get more results from different pages you should have a pay API key.

![Screenshot](/Screenshots/screenshot.png)

## Features
It has three optional search modes:

* COUNTRY: Select a country code at random and add it in query  
* DEVICE: Select a random search filter  
* MIX: Randomly joins the previous two

Note: Only country mode can be added with your custom search.  

## Examples of Usage
```text
./DeepInside.py -t 'FTP country:US' -o SavedFile
./DeepInside.py -t 'FTP' -r COUNTRY -o SavedFile -w
./DeepInside.py -r MIX -o SavedFile -w
./DeepInsde.py -r DEVICE -o SavedFile -w -n 2 
```
![Screenshot](/Screenshots/screenshot2.png)

## Attention
Use this tool only with educational purposes and not for evil.
## References
 * [Shodan](https://www.shodan.io/)
 * [Awesome Shodan Queries](https://github.com/jakejarvis/awesome-shodan-queries) 
