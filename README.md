# psd-css-extractor

Extracts all text from a PSD and relevant style information as CSS

## Usage

    ./extract.py your.psd

## Installation

This code requires both `python` and `ruby` to operate.

# Install Ruby Dependencies

## Install Locally (recommended)

    gem install --user-install bundler
    bundle install --path vendor/bundle

## Install Globally

    gem install bundler
    bundle install

# Install Python Dependencies

## Install Locally (recommended)

    virtualenv venv
    source ./venv/bin/activate
    pip install -r requirements.txt

You can then either type `source ./venv/bin/activate` to activate the virtual
environment to the code each time, or you can invoke the code as:

    ./venv/bin/python ./extract.py FILENAME

## Install Globally

    pip install -r requirements.txt

## About

This code makes use of the very good PSD gem available to `ruby` to parse the
PSD file and output the layer information as JSON. The `python` script,
`extract.py` calls `_parse_psd.rb` internally in order to make use of this
parsed information to do post-processing on the information to output the
results as CSS.

Note that the PSD gem does output some CSS by default, however I found it quite
lacking. For example, it does not output the following:

- No support for `line-height`
- Correct `font-size` when transformations are involved
- The `width` or `height` of the text area
- No support for `font-style` or `font-weight`

## Future

There is potential that this project will be rewritten to use only `ruby`
rather than also requiring `python`. I have not yet taken the time to learn the
`ruby` syntax and this project began as a simple proof of concept.

## Customised PSD.rb

Unfortunately, this code will not work without modification to the default PSD `ruby` gem.

    https://github.com/adamcw/psd.rb

This fork adds support for determining line spacing, as well as allowing wider
PDF support, fixing an error I encountered with a file during development.

