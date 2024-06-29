# pyAGHT - Aeyohan's Genomics Helper Tools (Python)
Python genomics helper tools

# Prerequisites
- Python (3.6 or higher)
- git (to install without me adding this to pypi. Can be removed once aght is installed)

### On Windows
1. Open a terminal. (Don't know how? follow these instructions [Wikihow - How to open a terminal in Windows](https://www.wikihow.com/Open-Terminal-in-Windows))
1. Check if you have python installed by typing:
    ```
    python --version
    ```
    into the terminal and press enter (you may also need to change `python` to `python3`)

    * If you see something like this means you have python 3.9.2 installed (3.6 or higher is fine). Continue to 3.
        ```bat
        C:\Users\Aeyohan>python --version
        Python 3.9.2

        C:\Users\Aeyohan>
        ```
    * If it opens the Microsoft Store page for python, follow the prompts to install it

    * If you see something like this, it means you don't have python installed
        ```bat
        C:\Users\Aeyohan>python --version
        'python' is not recognized as an internal or external command,
        operable program or batch file.

        C:\Users\Aeyohan>
        ```
    * You can install python by running the following command to install python if you don't already:
        ```
        winget install -e --id Python.Python.3.10
        ```
        and this will install python 3.10
    * Once installed, run `python` in the terminal to ensure it worked.
    > You may need to reopen your terminal for the `python` command to work.

1. Check if you have git installed by running `git --version`.
    You will see something like this if you have it installed
    ```
    C:\Users\Aeyohan>git version
    git version 2.30.1.windows.1

    C:\Users\Aeyohan>
    ```
    * If you have git installed continue to _Installation_
    * Install git by using e.g. `winget install --id Git.Git` if you don't have it already. You may need need local
      admin on your account to install the software (this will appear as a prompt, as would when you normally install
      any software)
    * Run `git version` in the terminal again to make sure it works.
        >You may need to reopen your terminal for the `python` command to work.

### MacOS
* You should already have python installed (and may have git installed).
* Otherwise use _brew_ to install python and git yourself.

### Linux distros.
* If you're on Linux, you should know what you're doing already.

# Installation
1. Depending on your system, you will need to use `python` or `python3` for these commands. See above to figure out and
  don't forget to substitute this into your commands below.
1. If you had to install python in _Prerequisites_ (continue to step 3.) Otherwise:
    * If you have Anaconda, pyenv or a virtual environment manager, you should already know how to use this. Make a new
  environment if desired and follow the instructions.
1. Install ahgt running:
  ```
  python -m pip install git+https://github.com/Aeyohan/aght.git
  ```
  (where `python` at the start should be the same as the `python` or `python3` that you used to check your version) in
  your terminal.
> If you see something like this at the bottom: (mainly the WARNING about ava.exe)
>```
>Installing collected packages: aght
>  WARNING: The script ava.exe is installed in 'C:\Users\Aeyohan\AppData\Roaming\Python\Python39\Scripts' which is not on PATH.
>  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
>Successfully installed aght-0.0.1
>```
> It means you have to take a few extra steps to run Ava. If you know how, add `ava.exe` to path. Otherwise:
> Every time you want to run the script, you will need to use the full path to the script. You can find this by eiher:
> * running this in your console
>   ```
>   python -c "from pip._internal.commands.show import search_packages_info as info;import pathlib;data=next(info(['aght']));print(str((pathlib.Path(data.location) / data.files[0]).absolute())) if hasattr(data, 'location') else print(str((pathlib.Path(data['location']) / data['files'][0]).absolute()))"
>   ```
>   which will print out the location of `ava.exe` e.g.
>   `c:\users\{Aeyohan}\appdata\roaming\python\python39\site-packages\..\Scripts\ava.exe`
>
> or
> * running this in your console
>   ```
>   python -m pip show aght
>   ```
>   Look at the output and find the _Location:_ line
>   ```
>   C:\Users\Aeyohan>python -m pip show aght
>   Name: aght
>   Version: 0.0.1
>   Summary: Genomics helper python tools
>   Home-page: None
>   Author: Aeyohan Furtado
>   Author-email: aeyohanf@gmail.com
>   License: None
>   Location: c:\users\aeyohan\appdata\roaming\python\python39\site-packages
>   Requires: pyfaidx, tqdm, pandas
>   Required-by:
>
>   C:\Users\Aeyohan>
>   ```
>   Copy the path (above `c:\users\aeyohan\appdata\roaming\python\python39\site-packages`),
>   paste it into your terminal and then put `..\Scripts\ava.exe` on the end so it looks like
>   `c:\users\aeyohan\appdata\roaming\python\python39\site-packages\..\Scripts\ava.exe`
>
> Copy paste this and run the command to ran ava.
> It should look like this when you run it:
> ```
> C:\Users\Aeyohan>c:\users\aeyohan\appdata\roaming\python\python39\site-packages\..\Scripts\ava.exe
> usage: ava [-h] [--input INPUT] --config CONFIG --output OUTPUT
> ava: error: the following arguments are required: --config/-c, --output/-o
>
> C:\Users\Aeyohan>
> ```

# Updating?
since this is still in development (and not on pypi):
1. Run the following command to uninstall aght
  `python -m pip uninstall aght`
2. Run the following command to install aght
  `python -m pip install git+https://github.com/Aeyohan/aght.git`

# Usage
## Allele Variance Applicator (ava)
To run the ava script, run the command `ava` (or the full path to the `ava.exe` as per above)
Options:
* `-i/--input`: path to input folder. This folder should contain your input fasta files (.fasta/.fa) AND your variance
  .csv files.
* `-c/--config`: path to config/metadata csv file. Do not use an Excel file. This provides info between things
* `-o/--output`: path to output folder. Output fasta files will go here.

e.g.
`ava -i "22 SNP for 10 CDS" -c "22 SNP for 10 CDS\metadata.csv" -o "snip_output"`

example output
```
Loading sequence files: 100%|█████████████████████████████████████████████████████████████| 1/1 [00:00<?, ?it/s]
Loading variant files: 100%|██████████████████████████████████████████████████████████████| 30/30 [00:00<00:00, 714.28it/s]
Performing preprocessing
Preparing output files:: 100%|████████████████████████████████████████████████████████████| 29/29 [00:00<?, ?it/s]
Cleaning up: 100%|████████████████████████████████████████████████████████████████████████| 59/59 [00:00<00:00, 398.64it/s]
Output to {output dir} complete. Check log at {output dir}\output.log for more details
```

Example test case took < 5 mins to run. Dropped to 46 seconds when I enabled multiprocessing (8c/16t). (and too tired to
parallelise the other parts now).

Somehow uses basically no ram (70mb per process, so 1.2GB) Probably thanks to
[pyfaidx](https://pypi.org/project/pyfaidx/) which massively optimises memory and random access for fasta files via an
index file.

## ava extras

### preprocessor (optional)
Used to remove extra strings from the variant input files. Ideally run this on a copy of your files in case something goes wrong
* `-i/--input`: path to folder with variant files. This folder should contain your variant csv files (.csv).
Works [recursively](https://www.google.com/search?q=recursion).
* `-n/--name` **(optional)**: remove this from the file name. By default this is _" (Variants, filtered)"_. Leave this
  argument out if you are using the default name.
e.g.
`pre_ava -i "03 CDS CSV file"`
`pre_ava -i "03 CDS CSV file" -n " Remove This String"`

example out
```
100%|█████████████████████████████████████| 30/30 [00:00<00:00, 30109.86it/s]
Renamed 30 files
```


### postprocessor (optional)
Used to get a different output folder structure
* `-i/--input`: path to ava's output folder. This contains fasta files with variants applied.
* `-o/--output`: path to output folder. Output fasta files will go here. (This should not be the same as the input)

e.g.
`post_ava -i snip_output -o snip_output_restructure`

example out
```
100%|█████████████████████████████████████| 29/29 [00:00<00:00, 1094.97it/s]
Renamed 29 files with 0 potential issues.
```

> Note: if there are any issues detected, they will be in the output log e.g.
> ```
> Renamed 29 files with 2 potential issues. See [path to file.log]  for more details
>```
