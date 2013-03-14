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

[1]: https://github.com/scrapy/scrapy/tree/0.16.4
