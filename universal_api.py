import requests
import xml.etree.ElementTree as ET
from json2xml import json2xml, utils


def get_page_text(URL):
    """
    Get text from web page by URL.
    Arguments:
        - URL: str, url for web page.
    Returns:
        - str, text of web page by URL.
    """
    r = requests.get(URL)
    if not r:
        return "Error " + r.status_code
    else:
        return r.text


def process_page_text(text, text_format, tags_array):
    """
    Process text web page.
    Arguments:
        - text: str, text of web page;
        - text_format: format of text ('json' or 'xml');
        - tags_array: array of tuples (tag, value). 
            Appropriate values for value parameter in tuple:
                - 'all': find all entries connected with this tag;
                - 'one': find first entry connected with this tag;
                - 'upper': find all information about this tag for the uppest level of json.
            Example: [("name", "all"), ("time", "one"), ("meals", "upper")].
    Returns:
        - dict, dictionary with keys as inserted tags and values as found information from text.
    """

    if text_format == 'xml':
        data_xml = ET.fromstring(text)
    elif text_format == 'json':
        data_json = utils.readfromstring(text)
        data_xml_text = json2xml.Json2xml(data_json).to_xml()
        data_xml = ET.fromstring(data_xml_text)
    else:
        print("Unsupported format:", text_format, "!")
        return None

    result_dict = {}

    for tag, value in tags_array:

        if value == 'all':
            tag_list = data_xml.findall(".//" + tag)
            result_list = []

            for el in tag_list:
                if el.get('type') == 'list':
                    result_list.append(list(map(lambda x: x.text, el)))
                elif el.get('type') == 'int':
                    result_list.append(int(el.text))
                elif el.get('type') == 'float':
                    result_list.append(float(el.text))
                elif el.get('type') == 'str' or el.get('type') is None:
                    result_list.append(el.text)
                else:
                    print("There are no conditions for", el.get('type'))

            result_dict[tag] = result_list

        elif value == 'one':
            result = data_xml.find(".//" + tag)

            if result is None:
                print("There are no entries with", tag)

            else:
                if result.get("type") == 'list':
                    result_dict[tag] = list(map(lambda x: x.text, result))
                elif result.get('type') == 'int':
                    result_dict[tag] = int(result.text)
                elif result.get('type') == 'float':
                    result_dict[tag] = float(result.text)
                elif result.get('type') == 'str' or result.get('type') is None:
                    result_dict[tag] = result.text
                else:
                    print("There are no conditions for", result.get('type'))

        elif value == 'upper':
            if text_format == "json":
                try:
                    result_dict[tag] = data_json[tag]
                except:
                    print(tag, "isn't on the upper level in json!")
            else:
                print("Unsupported upper entry for xml!")

        else:
            print("Unsupported entry:", value)

    return result_dict
