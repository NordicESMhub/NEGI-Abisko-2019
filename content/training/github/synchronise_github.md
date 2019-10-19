# How to synchronize your fork github repository?

It is possible to synchronize your fork from the github interface but we recommend to follow the steps from the command line.

## Step-1: Clone your fork 

- Open a terminal in Jupyterhub
- Then clone **your** fork e.g. make sure you replace **USERNAME** by your github username

```
git clone https://github.com/USERNAME/NEGI-Abisko-2019.git NEGI-Abisko-2019-fork
```

The command above makes a copy of your online fork NEGI-Abisko-2019 repository and store it in a folder locally. We named this folder NEGI-Abisko-2019-fork so we remember it is our fork and not the main NordicESMHub repository.

Then change directory to your fork:

```
cd NEGI-Abisko-2019-fork
```

## Step-2: Link your fork to NordicESMHub repository

Your local `NEGI-Abisko-2019-fork` is *linked* to your github repository but **NOT** to NordicESMHub.

How do we know that? 

```
git remote -v
```

It should return something like (with your github username, instead of *USERNAME*):

```
origin        https://github.com/USERNAME/NEGI-Abisko-2019.git (fetch)
origin        https://github.com/USERNAME/NEGI-Abisko-2019.git (push)
```

So let's do it now:

```
git remote add upstream https://github.com/NordicESMHub/NEGI-Abisko-2019.git
```

The name **upstream** is arbitrary and can be changed with any other name of your choice. You then need to use it instead of **upstream**.

We can check it:


```
git remote -v
```

And now we have two new lines.

```
origin          https://github.com/USERNAME/NEGI-Abisko-2019.git (fetch)
origin          https://github.com/USERNAME/NEGI-Abisko-2019.git (push)
upstream        https://github.com/NordicESMHub/NEGI-Abisko-2019.git (fetch)
upstream        https://github.com/NordicESMHub/NEGI-Abisko-2019.git (push)

```

## Step-3: update your local repository

```
git pull upstream master
```

The command above updated your local fork (on jupyterhub).

In case a merge happens, a window will pop pup and ask you to merge. By default, we have emacs editor in git so use **F10 --> Save** and **F10 --> exit**. 

## Step-4: push your local changes to github

Our fork is now up to date locally on Jupyterhub but still not yet updated online on github. So now we need to push our changes on github:

```
git push origin master
```

You are now ready to update your local repository and add new contributions!

**Whenever you need to make new contribution, the best is to update your fork before.
