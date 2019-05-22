## XPCTL

`xpctl` is a command-line interface to track experimental results and provide access to a global leaderboard. After running an experiment through `mead`, the results and the logs are committed to a database. Several commands are provided to show the best experimental results under various constraints.

Previously, it was a part of [baseline](https://github.com/dpressel/baseline).

### Usage

In `mead` we have separate **tasks** such as classify or tagger. Each 
1task can have multiple **experiments**, each corresponding to a model or different hyperparameters of the same model. An experiment is uniquely identified by the id. The configuration for an experiment is uniquely identified by hash(_sha1_) of the config file. 

After an experiment is done, use `xpctl` to report the results to a database server. Then use it to analyze, compare and export your experimental results. 

The results are posted to a database server through a REST service. They are accessed through a command line client that talks to the service.

The commands are described in [docs/commands.md](docs/commands.md).

### Prerequisite

`xpctl` requires a database to be installed locally or an accessible server. We currently support:  [mongodb](https://docs.mongodb.com/) and [postgresql](https://www.postgresql.org/)), but the base classes can be extended to support other databases. Create a database called `reporting_db` in your db instance.

 
### Installation

-  [Install the server](orchestration/README.md)
-  Install the client with `pip install -e .` 
-  add this directory to your `PYTHONPATH` 

#### Removing previous installation

If you already had `xpctl` installed from `baseline` do the following before installing the client.

- `pip uninstall xpctl`.
-  remove/rename `baseline/python/xpctl`
-  remove `xpctl.egg-info` from `baseline/python/`

If you are a contributor to `baseline`, you would need to `untrack` the `xpctl` files. That can be done running the following commands at your `baseline` installation.

```
git update-index --skip-worktree python/xpctl/cli.py
git update-index --skip-worktree python/xpctl/core.py
git update-index --skip-worktree python/xpctl/helpers.py
git update-index --skip-worktree python/xpctl/__init__.py
git update-index --skip-worktree python/xpctl/version.py
git update-index --skip-worktree python/xpctl/mongo/backend.py
git update-index --skip-worktree python/xpctl/mongo/__init__.py
git update-index --skip-worktree python/xpctl/sql/backend.py
git update-index --skip-worktree python/xpctl/sql/__init__.py```
``` 