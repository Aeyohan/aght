# AGHT - Aeyohan's Genomics Helper Tools
Python genomics helper tools

# Prerequisites
- Python (3.6 or higher)
- git

### On Windows 
- Open a terminal ([Wikihow - How to open a terminal in Windows](https://www.wikihow.com/Open-Terminal-in-Windows))
- Check if you have python installed by typing `python --version` and pressing enter (you
  may also need to try `python3 --version` instead of `python`)

    Something like this means you have python 3.9.2 installed (3.6 or higher is fine)
    ```bat
    C:\Users\Aeyohan>python --version
    Python 3.9.2

    C:\Users\Aeyohan>
    ```
    Something like this means you don't
    ```bat
    C:\Users\Aeyohan>python --version 
    'python' is not recognized as an internal or external command,
    operable program or batch file.

    C:\Users\Aeyohan>
    ```
    * Run the following command to install python if you don't already: `winget install -e --id Python.Python.3.10` to
  install python 3.10

* Check if you have git installed by running `git --version`.
    You will see something like this if you have it installed
    ```
    C:\Users\Aeyohan>git version
    git version 2.30.1.windows.1

    C:\Users\Aeyohan>
    ```
* Install git by using e.g. `winget install --id Git.Git` if you don't have it already

### MacOS
* You should already have python installed. Otherwise use brew to install python and git yourself.

### Linux distros.
* You should know what you're doing already.

# Installation
* If you have Anaconda, pyenv or a virtual environment manager, you should already know how to use this. Make a new
  environment and follow the instructions. If you have no idea what this means, skip this and continue to the next
  instruction.
* Install py running `python -m pip install git+https://github.com/Aeyohan/aght.git` (where `python` at the start should
  be the same as the `python` or `python3` that you used to check your version) in your terminal.
> If you see something like this at the bottom: (mainly the WARNING about ava.exe)
>```
>Installing collected packages: aght
>  WARNING: The script ava.exe is installed in 'C:\Users\Aeyohan\AppData\Roaming\Python\Python39\Scripts' which is not on PATH.
>  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
>Successfully installed aght-0.0.1
>```
> You will need to add it to PATH (or if you don't know how), every time you want to run the script, you will need to
> use the full path which is based on the path above (e.g. as above
> `C:\Users\Aeyohan\AppData\Roaming\Python\Python39\Scripts` and then add `\ava.exe` on the end)

