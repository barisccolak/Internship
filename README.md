

## Markdown links

1. [Basic Syntax](https://www.markdownguide.org/basic-syntax/)
2. [Advanced Syntax](https://daringfireball.net/projects/markdown/syntax)


## Git Commands

1. `git add . -n` : Shows the dry changes 
2. `git add .` : Adds the changes
3. `git commit -m "message"` : Commits
4. `git <x> --help` : Documentation for x
5. `git --help` : Documentation for Git
6. `git push` : Pushes the commit
7. `git checkout branch_name` : Changes the branch
8. `git push --set-upstream origin sidebranch` : Pushes and sets upstream for current branch
9. `git status` : Shows the status
10. `git checkout -b ＜new-branch＞` : Creates and changes to new branch


## Conda Commands

1. `conda create -n test-env <python=3.10 numpy pandas> -y` : Creates a test environment and installs the listed packages
2. `conda activate test-env`: Activates test environment
3. `conda list`: show all packages installed in the currently active environment
3. `conda list pandas`: show all packages that contain the name `pandas` installed in the currently active environment
3. `conda uninstall <package_name>`: uninstall a package from the envrionment
3. `conda env remove -n <envrionment_name>`: remove a conda environment completely


## Pip Commands

1. `pip install pint` : Install a package from the internet (PyPi)
1. `pip uninstall pint` : remove a package previously installed using `pip`
1. `pip install -e .` : Installs the local folder as python package

## Command Shell 

1. `python`
2. `ipython`
2. `python -m ipykernel install --user --name test-env --display-name "test-env"`: register a conda environment as a jupyter kernel (you need this to make the environment selectable in Jupyter notebook)
