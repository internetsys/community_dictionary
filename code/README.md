The construction of the community semantic dictionary consists of code in the following four subdirectories:

- `1-search`: crawling procedure.
- `2-filter`: stop-sites filter and PU-Bagging filter.
- `3_download`: Download 50,000 candidate community pages and furth filter using regexes.
- `4_parser`: parse community semantics from IRR records and websites.

The specific instructions are as follows:

* 1-search/

  - 1-buildurls.py
    - Input：[customer cone file](https://publicdata.caida.org/datasets/as-relationships/serial-1/), lgrecord.csv(search terms of [LG search method](https://publicdata.caida.org/datasets/as-relationships/serial-1/)), orgnamenew.csv(asn2org_name)
    - Build search terms for crawlers, i.e. BGP community+ASN and BGP community+ORG.
    - The built search terms are saved in the URLrecord.csv file.

  - 2-crawl.py
    - Crawls Bing query results based on search terms of 1-buildurls.py and inputseed.csv (seed community pages), multi-threaded search.
    - Each thread will open a browser for crawling, and the page opened is the homepage of BING. Please set the number of search results displayed per page to 30.
    - The crawler results are saved in Middle_results_i.csv.

  - 3-deal.py
    - Save the results of 10 threads in the json file.
    - The results are saved in search_results.json.

* 2-filter
  * 0-getseedtitle.py
    * Obtain titles of each seed URLs.
  * 1-stopsiteFIlter.py
    - Filter candidate sites according to the list of stop-sites.
    - For the remaining sites, the seed sites are positive samples, and the remaining crawler results are unlabeled samples.
  * 2-URLPUBagging.py
    * Train PU-Bagging model  based on its url.
  * 3-TitlePUbagging.py
    * Train PU-Bagging model  based on its title.
  * 4-runPUBagging.py
    * Use PU-Bagging to score each candidate site based on its url and title (probability value).
  * 5-mixResult.py
    * Add the probability based on URL and title and and sort it.
* 3-download
  * 1-download.py
    * Download the html files of the 50,000 websites with the highest probability.
  * 2-regularFilter.py
    * Filter Websites that record semantic information using regular expressions.
* 4-parser
  * 1-asrank.py
    * Generate the script `asns.sh` that gets the IRR records.
  * run `asns.sh`
  * 2-IRRparser.py
    * Build semantic dictionaries from IRR records.
  * 3-webdownload.py
    * Download webpages that record community semantic information.
  * 4-webparser.py
    * Build semantic dictionaries from webpages.







