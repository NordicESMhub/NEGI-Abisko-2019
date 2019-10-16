# Managing pyaerocom version

Pyaerocom python package is open source project and is licensed under [GNU General Public License v3.0](https://github.com/metno/pyaerocom/blob/master/LICENSE). 

### Pyaerocom stable version

The latest release of pyaerocom is available via [conda-forge](https://conda-forge.org/) and [PyPi](https://pypi.org/) and has been installed in [Abisko JupyterHub](https://abisko.uiogeo-apps.sigma2.no).

If you need to install pyaerocom on your local laptop, follow the [documentation](https://pyaerocom.met.no/).

### Pyaerocom development version

Pyaerocom is open source and it is fast evolving so during the NEGI Abisko course, you may need to install a development version.

A development version is not a release yet but you can install it in your jupyterLab environment on  [Abisko JupyterHub](https://abisko.uiogeo-apps.sigma2.no).

Pyaerocom development versions are located in different branches (not in the master branch). So to install a development version, check first which branch to use.

In  [Abisko JupyterHub](https://abisko.uiogeo-apps.sigma2.no), [open a Terminal](https://jupyterlab.readthedocs.io/en/stable/user/terminal.html).

Then clone Pyaerocom:

```shell
git clone -b v081dev https://github.com/metno/pyaerocom.git
```

In the example above, we will be installing pyaerocom version v081dev available in v081dev branch.

```shell
cd pyaerocom
python setup.py install --user
```

If you had a notebook opened and running, make sure to restart the python kernel (Kernel menu --> Restart kernel). You will then have to re-run all the cells of your notebook.

### Check pyaerocom version

```python
import pyaerocom
pyaerocom.__version__
```

In our case it returns:
```
'0.8.1.dev0'
```



