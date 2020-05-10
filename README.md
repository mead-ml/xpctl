## XPCTL

`xpctl` is a command-line interface to track experimental results and provide access to a global leaderboard. After running an experiment, the results and the logs are committed to a database. Several commands are provided to show the best experimental results under various constraints.

`xpctl` was developed as the primary backend for experiment storage for [mead-baseline](https://github.com/dpressel/baseline/).

### Usage

In `mead` we have separate **tasks** such as classify or tagger. Each task can have multiple **experiments**, each corresponding to a model or different hyperparameters of the same model. An experiment is uniquely identified by the id. The configuration for an experiment is uniquely identified by hash(_sha1_) of the config file. 

After an experiment is done, use `xpctl` to report the results to a database server. Then use it to analyze, compare and export your experimental results. 

The results are posted to a database server through a REST service. They are accessed through a command line client that talks to the service.

The commands are described in [docs/commands.md](docs/commands.md).

### Prerequisite

`xpctl` requires a database to be installed locally or an accessible server. We currently support:  [mongodb](https://docs.mongodb.com/) and [postgresql](https://www.postgresql.org/)), but the base classes can be extended to support other databases. Create a database called `reporting_db` in your db instance.

 
### Installation

-  [Install the server](orchestration/README.md)
-  Install the client with `pip install mead-xpctl` or locally with `pip install -e .`
-  add this directory to your `PYTHONPATH` 

#### Removing previous installation

If you already had `xpctl` installed from `baseline` do the following before installing the client.

- `pip uninstall xpctl`.
-  remove/rename `baseline/python/xpctl`
-  remove `xpctl.egg-info` from `baseline/python/`

