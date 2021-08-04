#!/bin/bash

install=true
reinstall=false

if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found"
    exit
fi

if python3 -c 'import pkgutil; exit(not pkgutil.find_loader("drop"))'; then
    echo drop already installed
    version=$(python3 -c 'from drop.__init__ import __version__; print(__version__)')
    installed=$(python3 -c 'import sys; sys.path = [x for x in sys.path if x]; print(sys.path); from drop import __version__; print(__version__)')
    # welcome to hell zone of one-liners.
    if  [ "$version" == "$installed" ]; then
      echo "drop's installed version equals this version: I will only build it then."
      install=false
    fi
fi

if [ "$1" == 'force_install' ]; then
  echo "force_install passed, forcing install"
  install=true
  reinstall=true
elif [ "$1" == 'no_install' ]; then
  echo "no_install passed, disabling install"
  install=false
fi

python3 -m pip install setuptools wheel  # make sure required installs are installed

if [ -d "build/" ]; then
  echo "build/ directory exists, renaming it"
  if [ -d "build-old/" ]; then
    echo "build-old/ exists, removing it"
    rm -rf build-old/
  fi
  mv build/ build-old/
fi

# warn the user "hey, I'm gonna build it now"
echo "building drop"
echo "---------------------------"
printf "\n\n\n\n"

python3 setup.py sdist bdist_wheel
# actually, y'know, build it.

if $install; then
  printf "\n\n"
  echo "installing drop using pip"
  echo "---------------------------"
  if $reinstall; then
    python3 -m pip install dist/drop_mod-*.whl --user --force-reinstall
  else
    python3 -m pip install dist/drop_mod-*.whl --user
  fi
fi
