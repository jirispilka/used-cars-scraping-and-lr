# Scrapping and simple linear regression of used cars

Web scaping of used cars data from sauto.cz. 

Simple linear regression on mileage and price

## Getting Started

### Prerequisites

* Python (>= 2.7 or >= 3.3)
* Selenium
* NumPy
* BeautifulSoup
* Pandas
* Seaborn
* argparse

[comment]: <> (* Selenium Standalone server)

### Installation

If you have pip installed just type
```
pip install numpy selenium beautifulsoup pandas seaborn argparse
```

[comment]: <> (Download the Selenium Standalone Server: http://www.seleniumhq.org/download)

Donwload Chrome driver: https://sites.google.com/a/chromium.org/chromedriver/ and add it somewhere into PATH, e.g. to ~/.local/bin:


### Usage

[comment]: <> (Start the Selenium Server:)
[comment]: <> (```)
[comment]: <> (java -jar selenium-server-standalone-3.3.0.jar &)
[comment]: <> (```)

I was a bit lazy, hence in each file below you need to setup several variables.

To download ads:

* set: file_prefix (prefix of saved htmls)
* set: data_dir (data directory)
```
python download_ads.py --url 'http://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&fuel=2&subCategory=6&manufacturer=93&model=705&page=1'
```

Parse saved html files:

* set: data_dir (data directory)
* set: csv_file

```
python parse_html.py
```

Plot linear regression:

* set: csv_file

```
python cars_linear_regression.py
```

