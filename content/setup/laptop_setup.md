# Getting your laptop ready

## Installing an editor, git and python

  To be able to follow [Plotting and Programming in Python](https://swcarpentry.github.io/python-novice-gapminder) online lesson, you would need to install an editor, git and python. Follow the [setup](https://uio-carpentry.github.io/2019-09-16_python/#setup) instructions and contact any instructors/assistants if you encounter any problems.

  We maintain a list of common issues that occur during installation as a reference for instructors
  that may be useful on the
  [Configuration Problems and Solutions wiki page](https://github.com/swcarpentry/workshop-template/wiki/Configuration-Problems-and-Solutions).

## Create a new Anaconda environment
 
During the abisko course we will be using additional packages that are not part of the main (base) python anaconda environment. 

To install additional Python packages/libraries, you need to open a Terminal, and then follow the instructions below.

```
$ conda env create -f environment.yml
```

where environment.yml is a text file containing the list of packages required for running your analysis. 

We provide you with a non exhaustive list of useful packages. Feel free to add new packages:

```
name: esm-python-analysis

channels:
  - conda-forge
  - bioconda
  - defaults

dependencies:
  - python=3.7
  - numpy >=1.14
  - xarray >=0.10.8
  - pandas >=0.22.0
  - cartopy >=0.16.0
  - matplotlib 
  - seaborn >=0.8.1
  - geopy >=1.17.0
  - basemap
  - netcdf4
```
