We provide a script (extract_rel.py) for downloading BGP routes collected from all route collectors in RouteViews and RIPE NCC by using [BGPStream](https://bgpstream.caida.org/) and extracting relationship using our dictionary. Follow the [instructions](https://bgpstream.caida.org/download) to install BGPStream V2 first and then install pybgpstream.

```
$ python bgp_path_downloader.py -s <start date> -d <duration (in seconds)>

# for example, to download BGP routes on 06/01/2019 from all available route collectors and extract relationships using our dictionary
$ python extract_rel.py -s 06/01/2019 -d 86400
# BGP paths are written to 'rib.txt' and relationships are written to 'relationship.txt'
```





