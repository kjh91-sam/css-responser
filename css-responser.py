import sys
import os
import re
import json

with open('config.json', 'r') as f:
    config = json.load(f)

DESKTOP = config['desktop']['default-size']
MOBILE = config['mobile']['default-size']
DESKTOP_BRKP = config['desktop']['break-points']
MOBILE_BRKP = config['mobile']['break-points']
DESKTOP_BRKP_RATIO = [round(p / DESKTOP, 2) for p in DESKTOP_BRKP]
# MOBILE_BRKP_RATIO = [round(p / MOBILE, 2) for p in MOBILE_BRKP]

f.close()


def responsive_styling(styling_units, isMobile=True, brkp_i=0):
    responsive_styling = ""

    for unit in styling_units:
        responsive_styling += unit['selector'] + " {\n"

        for style in unit['styles']:
            pixel_vals = re.findall(r"(\d+)px", style)
            for value in pixel_vals:
                int_val = int(value)
                style = style.replace(value + "px", str(round(int_val / 414 * 100, 2)) + "vw" if isMobile else
                                      str(round(int_val * DESKTOP_BRKP_RATIO[brkp_i], 2)) + "px")
            responsive_styling += style + "\n"

        responsive_styling += "\t}"

    return f"@media (max-width:{750 if isMobile else DESKTOP_BRKP[brkp_i]}px) {{ {responsive_styling} \n}}\n"


def css_response(stylesheet):
    matches = re.finditer(
        r"(?P<selector>.*?){(?P<styles>.*?)}", stylesheet, re.MULTILINE | re.DOTALL)
    styling_units = [
        {
            "selector": m.group('selector'),
            "styles": [style for style in m.group('styles').split("\n") if re.search(r"\d+px", style)]
        }
        for m in matches
    ]
    styling_units = [unit for unit in styling_units if len(unit["styles"]) > 0]

    result = ""

    # desktop
    for i in range(len(DESKTOP_BRKP)):
        result += responsive_styling(styling_units, False, i)

    # mobile
    result += responsive_styling(styling_units, True)

    return result


goal_file_names = sys.argv[1:]

for file_name in goal_file_names:
    f = open(file_name, "r")
    file_content = f.read()
    f.close()

    if os.path.splitext(file_name) == '.css':
        response = css_response(file_content)
    else:
        matches = re.findall(r"(?<=<style>)(.*?)(?=<\/style>)",
                             file_content, re.MULTILINE | re.DOTALL)
        response = css_response("\n".join(matches))

    f = open("responsive_css_for_" + file_name + ".css", "w")
    f.write(response)
    f.close()
