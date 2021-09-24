# Use this file if you've done the styling of the mobile version in pixels.
# All pixel values ​​are converted to vw based on their default size.
# Not like the css-responser, it copies the entire stylesheet as is and only converts the pixel values.

import sys
import os
import re
import json

with open('config.json', 'r') as f:
    config = json.load(f)

MOBILE = config['mobile']['default-size']
MOBILE_BRKP = config['mobile']['break-points']

f.close()

def stylesheet_parser(stylesheet):
    matches = re.finditer(
        r"(?P<selector>.*?){(?P<styles>.*?)}", stylesheet, re.MULTILINE | re.DOTALL)
    styling_units = [
        {
            "selector": m.group('selector'),
            # "styles": [style for style in m.group('styles').split("\n") if re.search(r"\d+px", style)]
            "styles": [style for style in m.group('styles').split("\n")] #this program copies the stylesheet as it is and only change the pixel values
        }
        for m in matches
    ]
    # styling_units = [unit for unit in styling_units if len(unit["styles"]) > 0]
    return styling_units

def convert_stylesheet(stylesheet):

    def calc_to_vw(match):
        num_str = match.group(1)
        return str(round(int(num_str) / MOBILE * 100, 2)) + "vw"

    return re.sub(r"(\d+)px", calc_to_vw, stylesheet)


goal_file_names = sys.argv[1:]

for file_name in goal_file_names:
    f = open(file_name, "r")
    file_content = f.read()
    f.close()

    if os.path.splitext(file_name) == '.css':
        response = convert_stylesheet(file_content)
    else:
        matches = re.findall(r"(?<=<style>)(.*?)(?=<\/style>)",
                             file_content, re.MULTILINE | re.DOTALL)
        response = convert_stylesheet("\n".join(matches))

    f = open(file_name + "_converted_to_vw" + ".css", "w")
    f.write(response)
    f.close()
