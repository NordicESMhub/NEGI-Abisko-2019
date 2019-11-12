# What is Version Control?

*from [CodeRefinery](https://coderefinery.github.io) training material.*

The management of changes to documents, computer programs, large web sites, and other collections of information.

- **Records snapshots** of a project
- Implements **branching**:
  - you can work on several feature branches and switch between them
  - different people can work on the same code/project without interfering
  - you can experiment with an idea and discard it if it turns out to be a bad idea
  
![](https://coderefinery.github.io/git-intro/img/gitink/git-merge-2.svg)
- Implements **merging**:
  - tool to merge development branches for you


---

# Why is Version Control Essential?

![](https://smutch.github.io/VersionControlTutorial/_images/vc-xkcd.jpg)

![](https://aberdeenstudygroup.github.io/studyGroup/lessons/SG-T1-GitHubVersionControl/img/version-control-1.jpg)

![](https://itelligencegroup.com/wp-content/usermedia/SSL-VersionControl-and-Sync-Com-2-1200x392.png)

- Easy Modification of your codes
- Reverting Errors
- Collaboration
- Backup
- Reproducibility


### Roll-back functionality

- Mistakes happen - without recorded snapshots you cannot easily undo mistakes and go back to a working version.


### Branching

- Often you need to work on several issues in one code - without branching this can be messy and confusing.
- You can simulate branching by copying the entire code to multiple places but also this will be messy and confusing.


### Collaboration

- *I will just finish my work and then you can start with your changes.*.
- *Can you please send me the latest version?*.
- *Where is the latest version?*.
- *Which version are you using?*.
- *Which version have the authors used in the paper I am trying to reproduce?*.


### Reproducibility

- How do you indicate which version of your code you have used in your paper?
- When you find a bug, how do you know when precisely this bug was introduced
  (are published results affected? do you need to inform collaborators or users of your code?).


---

# Why Git and Github?

## Git 

[Git](https://git-scm.com) Open source (free to use) Version control software.

- Easy to set up - use even by yourself with no server needed.
- Very popular: chances are high you will need to contribute to somebody else's code which is tracked with Git.
- Distributed: good backup, no single point of failure, you can track and clean-up changes offline, simplifies collaboration model for open-source projects.
- Important platforms such as [GitHub](https://github.com), [GitLab](https://gitlab.com), and [Bitbucket](https://bitbucket.org)
  build on top of Git.
- Sharing software and data is getting popular and required in research context
  and [GitHub](https://github.com) is a popular platform for sharing software.


## GitHub 
A website (https://github.com/) that allows you to store your *Git repositories* online and makes it easy to collaborate with others.

- Share your code
- "*backup*"

---

# A quick introduction to Git

### Before you start you need to configure Git

If you haven't already configured Git, please follow the instructions in the 
[Git refresher lesson](https://coderefinery.github.io/git-refresher/01-setup/#configuring-git)


### Recording a snapshot with Git

- Git takes snapshots only if we request it.
- We will record changes always in two steps (we will later explain why this is a recommended practice):

```shell
$ git add somefile.txt
$ git commit

$ git add file.txt anotherfile.txt
$ git commit
```

- We first focus (`git add`, we "stage" the change), then shoot (`git commit`):

![Git staging](https://coderefinery.github.io/git-intro/img/git_stage_commit.svg)

### Check the status of your repository

```shell
$ git status
```

### Get command help

```shell
$ git help commit
```

### Git history and log

Now try `git log`:

```shell
$ git log

commit d619bf848a3f83f05e8c08c7f4dcda3490cd99d9
Author: Radovan Bast <bast@users.noreply.github.com>
Date:   Thu May 4 15:02:56 2017 +0200

    adding ingredients and instructions
```

- We can browse the development and access each state that we have committed.
- The long hashes uniquely label a state of the code.
- They are not just integers counting 1, 2, 3, 4, ... (why?).
- We will use them when comparing versions and when going back in time.
- `git log --oneline` only shows the first 7 characters of the commit hash and is good to get an overview.
- If the first characters of the hash are unique it is not necessary to type the entire hash.
- `git log --stat` is nice to show which files have been modified.

### Writing useful commit messages

Using `git log --oneline` we understand that the first line of the commit message is very important.

Good example:

```
increase threshold alpha to 2.0

the motivation for this change is
to enable ...
...
```

Convention: **one line summarizing the commit, then one empty line,
then paragraph(s) with more details in free form, if necessary**.

- Bad commit messages: "fix", "oops", "save work", "foobar", "toto", "qppjdfjd", "".
- [http://whatthecommit.com](http://whatthecommit.com)
- Write commit messages in English that will be understood
  15 years from now by someone else than you.
- Many projects start out as projects "just for me" and end up to be successful projects
  that are developed by 50 people over decades.
- [Commits with multiple authors](https://help.github.com/articles/creating-a-commit-with-multiple-authors/)

---


## Ignoring files and paths with .gitignore

- Should we add and track all files in a project?
- How about generated files?
- Why is it considered a bad idea to commit compiled binaries to version control?
- What types of generated files do you know?

As a general rule compiled files are not
committed to version control. There are many reasons for this:

- Your code could be run on different platforms.
- These files are automatically generated and thus do not contribute in any meaningful way.
- The number of changes to track per source code change can increase quickly.
- When tracking generated files you could see differences in the code although you haven't touched the code.

For this we use `.gitignore` files. Example:

```
# ignore compiled python 2 files
*.pyc
# ignore compiled python 3 files
__pycache__
```

`.gitignore` uses something called a
[shell glob syntax](https://en.wikipedia.org/wiki/Glob_(programming)) for
determining file patterns to ignore. You can read more about the syntax in the
[documentation](https://git-scm.com/docs/gitignore).

An example taken from [documentation](https://git-scm.com/docs/gitignore):

```
# ignore objects and archives, anywhere in the tree.
*.[oa]
# ignore generated html files,
*.html
# except foo.html which is maintained by hand
!foo.html
# ignore everything under build directory
build/
```

You can have `.gitignore` files in lower level directories and they affect the paths
relatively.

`.gitignore` should be part of the repository (why?).

---

### Clean working area

- Use `git status` a lot.
- Use `.gitignore`.
- Untracked files belong to .gitignore.
- **All files should be either tracked or ignored**.

---

### GUI tools

We have seen how to make commits directly via the GitHub website, and also via command line. 
But it is also possible to work from within a Git graphical user interface (GUI):

- [GitHub Desktop](https://desktop.github.com)
- [SourceTree](https://www.sourcetreeapp.com)
- [List of third-party GUIs](https://git-scm.com/downloads/guis)
- [Jupyterlab git](https://github.com/jupyterlab/jupyterlab-git) and [github](https://github.com/jupyterlab/jupyterlab-github) extensions
---

## Summary

Now we know how to save snapshots:

```shell
$ git add <file(s)>
$ git commit
```

And this is what we do as we program.

Every state is then saved and later we will learn how to go back to these "checkpoints"
and how to undo things.

```shell
$ git init    # initialize new repository
$ git add     # add files or stage file(s)
$ git commit  # commit staged file(s)
$ git status  # see what is going on
$ git log     # see history
$ git diff    # show unstaged/uncommitted modifications
$ git show    # show the change for a specific commit
$ git mv      # move tracked files
$ git rm      # remove tracked files
```

Git is not ideal for large binary files
(for this consider [http://git-annex.branchable.com](http://git-annex.branchable.com)).

# Want to learn more about git/github?

- [Introduction to version control with Git](https://coderefinery.github.io/git-intro/)
- [Archeology with Git](https://coderefinery.github.io/git-archaeology/)
- [Collaborative distributed version control](https://coderefinery.github.io/git-collaborative/)
- [Git branch design](https://coderefinery.github.io/git-branch-design/)
