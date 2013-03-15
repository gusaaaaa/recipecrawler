# Recipes crawler

Compilation of different and alternative techniques used to crawl and extract recipies from
the web.

## Requirements

- Python 2.7.3 (won't work with Python 3)
- [Scrapy 0.16][1]

## Setup

From the project's base directory run:

```$ bash script/setenv.sh```

That will create the necessary directories, files, environment variables and 
stuff to run the crawler.

## Prerrequisites

The following files are needed to run the crawler:

  - ```input/index.json``` (tf-idf index to compute similarities)
  - ```input/seeds.txt```  (start urls)

To generate these files, run:

```$ bash script/prepare.sh```

## Run

From the base directory:

```
$ bash run.sh
```

Different settings can be loaded. By default, file ```config/global.py``` is
copied to ```recipebot/settings.py``` before running the crawler. However,
is it possible to overwrite them adding custom files in the form
```config/custom_1```, ```config/custom_2```, etc.

Custom configuration files are appended to global settings and copied to 
```recipebot/settings.py```.

To run particular custom configuration (in the example, custom settings
number 2):

```
$ bash script/run.sh 2
```

[1]: https://github.com/scrapy/scrapy/tree/0.16.4
