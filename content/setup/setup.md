
# Before the course
Teachers, assistants and students should do the following:

- [Sign up on Github](https://github.com/join?source=header-home)
- [Please fill this form so we can get your github username](https://docs.google.com/forms/d/e/1FAIpQLSdivH004R2zfsD2f2h5CY34gueAsjf8_KsE8Q9xZIcHtxNzWQ/viewform)
- [Setup your laptop](#laptop-setup)
- [Setup on Abisko Jupyterhub](#jupyterhub-setup)


# Laptop setup

## Install packages

  To participate to Abisko course, you will need access to the software described below.
  In addition, you will need an up-to-date web browser.

  
  We maintain a list of common issues that occur during installation as a reference for instructors
  that may be useful on the
  [Configuration Problems and Solutions wiki page](https://github.com/swcarpentry/workshop-template/wiki/Configuration-Problems-and-Solutions).

  Follow setup instruction [here](https://uio-carpentry.github.io/2019-09-16_python/).

 ### Create a new Anaconda environment
 
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

### Download dataset for local installation

The sample dataset for Abisko course is freely available [here](https://doi.org/10.5281/zenodo.3475894)

([![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3475894.svg)](https://doi.org/10.5281/zenodo.3475894).

# Jupyterhub setup

Instructions for accessing Jupyter notebooks at Sigma2 server:

  - you should have received an email message titled "JupyterHub links for NeGi-Abisko-2019"
    - if not please request it to the course organizers 
  - follow "invitation link" in the email message 
    - If you don't already have a **Feide guest** user account (otherwise skip this step), click "Feide guest users". 
    - register a new account 
      - for the sake of simplicity try to use the same email that you are using for the course 
      - also try to use the same (or similar) user ID that you have for github 
      - finish the registration process
  - click again on the "invitation link" in the email
    - login with "Feide guest users"
      - accept the different policies
      - agree to become a member of the EScience-Abisko
    - the browser should display the message "Loading group details" 
  - now go to [Abisko Jupyterhub](http://abisko.uiogeo-apps.sigma2.no)
    - click "Sign in with Dataporten"
    - login with Feide Guest User 
  - finally the web browser should display a page with "jupyterlab" on the upper left side
  - for later usage of the notebooks just use the [Abisko Jupyterhub link](http://abisko.uiogeo-apps.sigma2.no/hub/user-redirect/git-pull?repo=https://github.com//NordicESMHub/NEGI-Abisko-2019&branch=gh-pages&subPath=content%2Fintro.md&app=lab) 

