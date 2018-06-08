from flask import Flask, Response, request
from difflib import SequenceMatcher
import getopt, sys

app = Flask(__name__)


@app.route('/')
def index():
    data = "Page Requested Unavailable at the moment"
    return Response(data, status=404)


def check_values_is_unique(value):
    value_set = list()
    return not any(each_value in value_set or value_set.append(each_value) for each_value in value)


def lcs_algorithm(value_list):
    common_strings = []
    for each_x in value_list:
        for each_y in value_list:
            if each_x != each_y:
                match = SequenceMatcher(None, each_x, each_y).find_longest_match(0, len(each_x), 0, len(each_y))
                if each_x[match.a:match.a + match.size] not in common_strings and each_x[
                                                                                  match.a:match.a + match.size] != '':
                    common_strings.append(each_x[match.a:match.a + match.size])
            else:
                continue
    return common_strings


def extract_value_list(value_data):
    return [each["value"] for each in value_data]


def make_value_list(common_string_data):
    return [{"value": each} for each in common_string_data]


@app.route('/lcs', methods=['GET', 'POST'])
def longest_common_string():
    if request.method == 'GET':
        info = 'Requested Method is not accepted'
        return Response(info, status=406)
    elif request.method == 'POST':
        if request.is_json:
            string_set = dict(request.get_json())
            if "setOfStrings" in string_set.keys():
                if string_set["setOfStrings"] is None or list(string_set["setOfStrings"]).__eq__(list()):
                    data = 'setOfStrings in POST data should not be empty'
                    return Response(data, status=409)
                else:
                    if check_values_is_unique(string_set["setOfStrings"]):
                        common_strings = lcs_algorithm(extract_value_list(string_set["setOfStrings"]))
                        data = {"lcs": make_value_list(common_strings)}
                        return Response(str(data), status=200, mimetype="application/json")
                    else:
                        data = "setOfStrings in POST data must be a Set (Unique)"
                        return Response(data, status=409)
            else:
                data = "JSON Data must contains setOfStrings as its key"
                return Response(data, status=409)
        else:
            data = "POST data must be in JSON Format"
            return Response(data, status=404)
    else:
        info = {'information': 'Requested {} Method is not allowed'.format(request.method)}
        return Response(str(info), status=404, mimetype='application/json')


if __name__ == '__main__':
    app.run()
