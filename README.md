## XPCTL

`xpctl` is a command-line interface to track experimental results and provide access to a global leaderboard. After running an experiment, the results and the logs are committed to a database. Several commands are provided to show the best experimental results under various constraints.

`xpctl` was developed as the primary backend for experiment storage for [mead-baseline](https://github.com/dpressel/mead-baseline/).

### Prerequisite

`xpctl` requires a database to be installed locally or an accessible server. We currently support:  [mongodb](https://docs.mongodb.com/) and [postgresql](https://www.postgresql.org/)), but the base classes can be extended to support other databases. Create a database called `reporting_db` in your db instance.

 
### Installation

-  [Install the server](orchestration/README.md)
-  Install the client
  - `pip install mead-xpctl`
  - or locally with `pip install -e .`

### [Documentation](docs/main.yml)
