# SciHuber

SciHuber is a command-line tool on macOS helping download literature on SciHub written in python3. Internally, it works in a similar way of accessing to the service of SciHub in any web browser. With all respect to SciHub, users of this tool are required to input captcha codes popping out by SciHub when accessing to the service too frequently.

## Install

SciHuber depends on some python libraries, which has been listed in the file named `requirements.txt`. To install these libraries, simply use `pip3 install -r /path/to/requirements.txt`.

In addition, to display the captcha code, SciHuber currently uses xquartz. If you have better alternatives, please raise an issue.

## Usage

SciHuber must be called from its root directory. To enter that directory, use `cd /path/to/scihuber/folder`.

There are two ways to use SciHuber, depending on the number of literature you would like to download at the same time.

1. If you would like to download only one document, use keyword `-l` (standing for link) or `--link=`, followed by the web link or doi to your literature, such as `python3 main.py -l yourlink` or `python3 main.py --link=yourlink`.

2. SciHuber could also download a bunch of literature consecutively, whose web links or dois are stored into a text file in separated lines. In this case, use keyword `-f` or `--file=`, followed by the path to the text document, such as `python3 main.py -f yourfile` or `python3 main.py --file=yourfile`.

In total, the above commands can be combined as `cd /path/to/scihuber/folder && python3 main.py -l yourlink`.

For help, input `python3 main.py -h`.

## Note

Should any problem emerge, please raise an issue.

## Issues

The author recommend the user run SciHuber directly on macOS, not under anaconda. There are issues that SciHuber does not work properly under anaconda for unknown reasons.