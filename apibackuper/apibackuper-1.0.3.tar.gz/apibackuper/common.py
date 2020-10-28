# coding: utf-8
import lxml.etree as etree
from collections import defaultdict


def etree_to_dict(t, prefix_strip=True):
    tag = t.tag if not prefix_strip else t.tag.rsplit('}', 1)[-1]
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
#            print(dir(dc))
            for k, v in dc.items():
                if prefix_strip:
                    k = k.rsplit('}', 1)[-1]
                dd[k].append(v)
        d = {tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[tag].update(('@' + k.rsplit('}', 1)[-1], v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            tag = tag.rsplit('}', 1)[-1]
            if text:
              d[tag]['#text'] = text
        else:
            d[tag] = text
    return d

def get_dict_value(adict, key, prefix=None, as_array=False, splitter='.'):
    if prefix is None:
        prefix = key.split(splitter)
    if len(prefix) == 1:
        if type(adict) == type({}):
            if as_array:
                return [adict[prefix[0]], ]
            return adict[prefix[0]]
        elif type(adict) == type([]):
            if as_array:
                result = []
                for v in adict:
                    result.append(v[prefix[0]])
                return result
            else:
                return adict[0][prefix[0]]
        return None
    else:
        if type(adict) == type({}):
            return get_dict_value(adict[prefix[0]], key, prefix=prefix[1:], as_array=as_array)
        elif type(adict) == type([]):
            if as_array:
                result = []
                for v in adict:
                    res = get_dict_value(v[prefix[0]], key, prefix=prefix[1:], as_array=as_array)
                    if res:
                        result.extend(res)
                return result
            else:
                return get_dict_value(adict[0][prefix[0]], key, prefix=prefix[1:], as_array=as_array)
        return None


def xml_to_dict(source, output, tagname, prefix_strip=True, dolog=True, encoding='utf8'):
    n = 0

    for event, elem in etree.iterparse(source, recover=True):
        shorttag = elem.tag.rsplit('}', 1)[-1]
        if shorttag == tagname:
            n += 1
            if prefix_strip:
                j = etree_to_dict(elem, prefix_strip)
            else:
                j = etree_to_dict(elem)
            elem.clear()
