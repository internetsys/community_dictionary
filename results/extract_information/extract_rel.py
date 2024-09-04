import json
import re
import datetime
import argparse
from _pybgpstream import BGPStream, BGPRecord


def get_community_dictionary():
    with open('../dictionary/semanticdic_total.json', 'r', encoding='utf-8') as f:
        semanticdic_merge = json.load(f)
    return semanticdic_merge

community_dictionary = get_community_dictionary()

def extract_relationship():
    relationship_list = []
    with open('./rib.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line_list = line.strip("\n").split("|")
            as_path = line_list[1]
            if as_path.find('{') > -1:
                continue
            asn_list = as_path.split(" ")
            # remove prepended ASes
            asn_list = [v for i, v in enumerate(asn_list)
                        if i == 0 or v != asn_list[i - 1]]
            asn_set = set(asn_list)
            # remove poisoned paths with AS loops
            if len(asn_set) == 1 or not len(asn_list) == len(asn_set):
                continue
            if line_list[2] != "":
                community_list = line_list[2]
            else:
                continue
            community_list = community_list.split(" ")
            for comm in community_list:
                ps = comm.split(':')
                if len(ps) != 2:
                    continue
                asn = ps[0]
                community_value = ps[1]
                if asn in community_dictionary.keys():
                    if "tag" in community_dictionary[asn].keys():
                        if "rel" in community_dictionary[asn]["tag"].keys():
                            for single in community_dictionary[asn]["tag"]["rel"]:
                                if single[0] == "explicit":
                                    if str(single[1]) == community_value:
                                        for i in range(0, len(asn_list)-1):
                                            if asn_list[i] == asn:
                                                relationship_list.append([asn_list[i], asn_list[i+1], str(single[2])])

                                if single[0] == "regular":
                                    if re.search(single[1], community_value):
                                        for i in range(0, len(asn_list) - 1):
                                            if asn_list[i] == asn:
                                                relationship_list.append([asn_list[i], asn_list[i + 1], str(single[2])])



    relationship_dict = dict()
    for tmp_list in relationship_list:
        if tmp_list[0] not in relationship_dict.keys():
            relationship_dict[tmp_list[0]] = dict()
            relationship_dict[tmp_list[0]][tmp_list[1]] = []
            relationship_dict[tmp_list[0]][tmp_list[1]].append(tmp_list[2])
        else:
            if tmp_list[1] in relationship_dict[tmp_list[0]].keys():
                if tmp_list[2] not in relationship_dict[tmp_list[0]][tmp_list[1]]:
                    relationship_dict[tmp_list[0]][tmp_list[1]].append(tmp_list[2])
            else:
                relationship_dict[tmp_list[0]][tmp_list[1]] = []
                relationship_dict[tmp_list[0]][tmp_list[1]].append(tmp_list[2])
    print(len(relationship_dict))



    with open(f"./relationship.txt", 'w', encoding='utf-8') as f1:
        for as1 in relationship_dict.keys():
            for as2 in relationship_dict[as1].keys():
                if len(relationship_dict[as1][as2]) == 1:
                    rel = relationship_dict[as1][as2][0]
                    if rel == 'peer':
                        f1.write(as1 + "|" + as2 + "|" + "0" + "\n")
                    elif rel == 'provider':
                        f1.write(as2 + "|" + as1 + "|" + "-1" + "\n")
                    elif rel == 'customer':
                        f1.write(as1 + "|" + as2 + "|" + "-1" + "\n")

def downloader(start_date, duration):
    """Download BGP paths from Routeviews and RIPE NCC from a start date for a certain duration."""

    # Start of UNIX time
    base = int(datetime.datetime.strptime(start_date, '%m/%d/%Y').strftime('%s'))
    # Create a new bgpstream instance and a reusable bgprecord instance
    stream = BGPStream()
    stream.add_interval_filter(base, base + int(duration))
    stream.add_filter('record-type', 'ribs')
    stream.start()
    f = open('rib.txt', 'w')
    while True:
        rec = stream.get_next_record()
        if rec is None:
            return
        if rec.status != "valid":
            continue
        else:
            elem = rec.get_next_elem()
            while(elem):
                path = elem.fields['as-path']
                if '{' in path or '(' in path:
                    elem = rec.get_next_elem()
                    continue
                prefix = elem.fields['prefix']
                communities = elem.fields['communities']
                f.write(prefix + '|' + path + '|' + communities + '\n')
                elem = rec.get_next_elem()
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download BGP paths from a start date for a duration')
    parser.add_argument('-s', '--start',
                        help='The start date',
                        required=True)
    parser.add_argument('-d', '--duration',
                        help='Duration in minutes',
                        required=True)
    args = parser.parse_args()
    downloader(args.start, args.duration)
    extract_relationship()
