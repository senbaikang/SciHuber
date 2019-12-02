# SciHuber

SciHuber is a command-line tool written in python3 (currently only on macOS) helping download literature on SciHub. Internally, it acquires access to the service of SciHub, working in a similar way to any web browser. Due to all respect to SciHub, users of this tool are required to input captcha codes popping out by SciHub when accessing to the service too frequently.

## Install

To clone the code to your local machine, simply type in your terminal: `git clone git@github.com:senbaikang/SciHuber.git`.

SciHuber depends on some python libraries, which has been listed in the file named `requirements.txt`. To install these libraries, simply use `pip3 install -r /path/to/requirements.txt`.

Currently, SciHuber depends on xquartz on macOS to display the captcha code. To install xquartz, use brew cask: `brew cask install xquartz`.

If you have better alternatives to xquartz, please raise an issue. If you are using windows and have a good option to display the code, please modify the code and pull a request.

## Usage

SciHuber must be invoked from its root directory. To enter that directory, use `cd /path/to/scihuber/folder`.

There are two ways to use SciHuber, depending on the number of literature you would like to download at the same time.

1. If you would like to download only one document, use keyword `-l` (standing for link) or `--link=`, followed by the web link or doi to your literature, such as `python3 main.py -l yourlink` or `python3 main.py --link=yourlink`.

2. SciHuber could also download a bunch of literature consecutively, whose web links or dois are stored into a text file in separated lines. In this case, use keyword `-f` or `--file=`, followed by the path to the text document, such as `python3 main.py -f yourfile` or `python3 main.py --file=yourfile`.

In total, the above commands can be combined as `cd /path/to/scihuber/folder && python3 main.py -l yourlink`.

For help, input `python3 main.py -h`.

## Note

Should any problem emerges, please raise an issue.
