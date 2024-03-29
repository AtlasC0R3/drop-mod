# Drop
###### *also known as drop-mod*
Drop is a Python module focused on providing moderation commands for chat-bots (i.e. Discord, Matrix.org, etc.)
## How do I use it?
You can use it in chat-bots (for example, [drop-discord](https://github.com/AtlasC0R3/drop-discord/))
or simply as a GUI app with the drop\.gui app I made.

`python3 -m drop`

## How do I install it?
There are 3 ways: either cloning the GitHub repository, using `pip` or using `build.sh`
### Cloning from GitHub
1. Clone this repository, [by downloading this repository as a \*.zip file](https://github.com/AtlasC0R3/drop-mod/archive/main.zip), [by cloning this repository using Git](https://github.com/AtlasC0R3/drop-mod.git) or [by going into this repository's releases](https://github.com/AtlasC0R3/drop-mod/releases) and downloading the latest release. If you download from this repository's release, you have the stable release. If you cloned this repository directly, you have a more "canary" release.
2. Run `setup.py` using your preferred Python installation
### Using `pip`
1. Run `pip install drop-mod`
### Using `build.sh`
**NOTE:** this will *most likely* only work on Linux (or bash systems)
1. Run `./build.sh`
If you want to force reinstall, you can use `./build.sh force_install`.
Or if you want the opposite of that (no install at all), you can use `./build.sh no_install`.

Drop should be installed *unless `setup.py` threw an error*!

To use it, import `drop` into your Python scripts (or specific commands using `from drop.basic import owofy`) and, well, use them!

Example:
```python
from drop.basic import owofy
owofy("The quick brown fox jumps over the lazy dog.")
# This is just a simple command to work with, hence why I use it as a prime example.
# no im not a furry shhHHHHHH.
```

## F.A.Q.
### Q: Is this project abandoned?
**A:** **Yes.** This project is really low in my priorities.

### Q: Are there any open images for this project?
**A:** Yes, [they are updated in a Gitdab repository](https://gitdab.com/atlas_core/drop-misc/src/branch/master/images). *[License link](https://gitdab.com/atlas_core/drop-misc/src/branch/master/images/license.txt)*
### Q: Can I use this for my own projects?
**A:** Of course, it's a Python module! Just install it, set it up in your projects/scripts, and off you go! *note: this Python module still has a license, please make sure your project respects the license.*
### ~~Q: who are you?~~
~~**A:** a person why are you asking~~

### Dependencies
**None of these packages listed below are included directly into this software!** They are only installed from [PyPI](https://pypi.org/) when running `setup.py`!

[Parsedatetime](https://github.com/bear/parsedatetime/), licensed under [Apache 2.0](https://github.com/bear/parsedatetime/blob/master/LICENSE.txt)

[aiohttp](https://github.com/aio-libs/aiohttp/), licensed under [Apache 2.0](https://github.com/aio-libs/aiohttp/blob/master/LICENSE.txt)

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), licensed under [MIT License](https://mit-license.org/)
