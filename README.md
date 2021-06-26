## XPCTL

`xpctl` is software to track experimental results and provide access to a global leaderboard. After running an experiment, the results and the logs are committed to a database. Commands are provided to show the best experimental results under various constraints.

`xpctl` was developed as the primary backend for experiment storage for [mead-baseline](https://github.com/dpressel/mead-baseline/).

### Prerequisite

`xpctl` requires a database to be installed locally or an accessible server. We currently support:  [mongodb](https://docs.mongodb.com/) and [postgresql](https://www.postgresql.org/)), but the base classes can be extended to support other databases. Create a database called `reporting_db` in your db instance.

The client API is packaged separately with minimal requirements.

 
### Installation

- There are 2 components: `mead-xpctl-client` and `mead-xpctl`
  - `mead-xpctl-client` provides the HTTP client and the addon required to run logging from inside `mead-baseline`
  - `mead-xpctl` contains the CLI and the server implementation
  - Both packages can be installed via pip:
    - `pip install mead-xpctl-client`
    - `pip install mead-xpctl` (this depends on the `mead-xpctl-client`)
-  [Install the server](https://github.com/mead-ml/xpctl/blob/master/orchestration/README.md)

### [Documentation](https://github.com/mead-ml/xpctl/blob/master/docs/main.md)
