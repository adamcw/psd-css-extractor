#!/usr/bin/env python
"""Usage: ./extract.py FILENAME

Arguments:
    FILENAME    The PSD to be processed.
"""

from __future__ import (absolute_import, print_function, division,
        unicode_literals)
import os
import sys
import json
import docopt
import subprocess
from collections import defaultdict

#
# This code will not work without modification to the default PDF ruby gem.
# https://github.com/adamcw/psd.rb
#

FONT_TYPE_MAP = {
    "Bold":   [("font-weight",  600)],
    "Italic": [("font-style",   "italic")],
    "Light":  [("font-weight",  300)],
}

class PSD:
    def __init__(self, filename):
        dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))
        ruby_cmd = "{}{}_parse_psd.rb".format(dirname, os.path.sep)
        output = subprocess.check_output([ruby_cmd, filename])
        self.doc = json.loads(json.loads(output))

    def get_layers(self):
        return _get_layers(self.doc['children'])

    def get_texts(self):
        return [PSDText(x) for x in self._get_layers(self.doc['children'])
            if 'text' in x and x['text']]

    def _get_layers(self, root):
        layers = []
        for layer in root:
            if 'children' in layer:
                layers += self._get_layers(layer['children'])
            else:
                layers.append(layer)
        return layers

class PSDText:
    def __init__(self, layer):
        self.value = ""
        self.style = PSDTextStyle()
        self.width = 0
        self.height = 0
        self.extract_text(layer)

    def extract_text(self, layer):
        self.style.extract_style(layer['text'])
        self.value = layer['text']['value']
        self.width = layer['width']
        self.height = layer['height']

    def __str__(self):
        out = ""
        out += self.value + "\n\n"
        out += str(self.style)
        out += "width: {}px;".format(self.width)
        out += "height: {}px;".format(self.height)

class PSDTextStyle:
    def __init__(self, styles=None):
        self._styles = []
        if isinstance(styles, list):
            self._styles += styles

    def extract_style(self, text):
        font = text['font']

        for fname in font['fonts']:
            if fname == "AdobeInvisFont":
                break

            name, typ = fname, "Regular"
            bits = name.split("-")
            if len(bits) == 2:
                name, typ = bits
            self._styles.append(("font-family", name))

        if typ in FONT_TYPE_MAP:
            self._styles += FONT_TYPE_MAP[typ]

        for size in font['sizes']:
            self._styles.append(("font-size", "{}px".format(
                int(round(size * text['transform']['yy'], 0)))))

        for (r,g,b,a) in font['colors']:
            if a == 255:
                self._styles.append(("color", "rgb({}, {}, {})".format(r, g, b)))
            else:
                self._styles.append(("color", "rgba({}, {}, {}, {})".format(r, g, b, a)))

        for leading in font['leadings']:
            self._styles.append(("line-height", "{}px".format(
                int(round(leading * text['transform']['yy'], 0)))))

        self._styles.append(("text-align", font['alignment'][0]))

    def __str__(self):
        out = ""
        for k, v in self._styles:
            out += "{}: {};\n".format(k, v)
        return out

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self._styles == other._styles

if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    psd = PSD(args["FILENAME"])
    texts = psd.get_texts()
    print(len(texts))

    styles = defaultdict(list)
    for text in texts:
        styles[text.style].append(text)

    for style, texts in styles.items():
        print(unicode(style).encode('utf-8'))
        for text in texts:
            print(unicode(text.value).encode('utf-8'))
            print("")
        print("-------------------------------------------\n")
