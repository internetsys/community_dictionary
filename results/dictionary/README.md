### community_websites.txt

websites we find after crawling and filtering procedure.

each line is consist of `ASN  URL`.

### semanticdic_total.json

Using Json file to store community dictionary

The structure of the dictionary is as follows:

- AS Number
  - tag
    - rel (Commercial Relationship)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c = 'provider', 'peer', 'customer', 'partial customer', 'partial provider'
    - loc (Interconnected Geographic Location)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c = 'n-location name', where
          - n=1 indicates that the location is a continent.
          - n=2 indicates that the location is a country.
          - n=3 indicates that the location is a city.
          - n=4 indicates that the location is a geographic location within different time zones in the United States.
          - If there are multiple locations, they are separated by commas.
    - IXP (Interconnected IXP)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c = 'IX-IXP name'
          - If there are multiple names, they are separated by commas.
    - facility (Interconnected Facility)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c = 'FA-Facility name'
          - If there are multiple names, they are separated by commas.
    - asn (AS Number)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c is a numeric value representing the AS number.
  - blackhole (Routing Blackhole)
    - List, with items [a, b]
      - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
      - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
  - pref (Local Preference)
    - List, with items [a, b, c]
      - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
      - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
      - c is usually a numeric value indicating the size of the local preference, but it could also be 'lower than xxx' or 'higher than xxx'.
  - sel_ann (Selective Announcement)
    - no-export (Not Announce To)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c
          - Numeric value, representing the AS number.
          - 'IX-IXP name', representing an IXP.
          - 'FA-Facility name', representing a facility.
          - 'n-location name', n=1,2,3,4, representing a geographic location.
          - If there are multiple entries, they are separated by commas.
    - export (Announce To)
      - List, with items [a, b, c]
        - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
        - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
        - c
          - Numeric value, representing the AS number.
          - 'IX-IXP name', representing an IXP.
          - 'FA-Facility name', representing a facility.
          - 'n-location name', n=1,2,3,4, representing a geographic location.
          - If there are multiple entries, they are separated by commas.
  - prepend (Path Prepending)
    - List, with items [a, b, c]
      - a = 'explicit' indicates that the community value is a numeric value, and b is that value.
      - a = 'regular' indicates that the community value is a regular expression, and b is the regular expression.
      - c is a numeric value representing the number of times prepended.