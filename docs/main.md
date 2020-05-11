# Usage

In `mead` we have separate **tasks** such as classify or tagger. Each task can have multiple **experiments**, each corresponding to a model or different hyperparameters of the same model. An experiment is uniquely identified by the id. The configuration for an experiment is uniquely identified by hash(_sha1_) of the config file.

After an experiment is done, use `xpctl` to report the results to a database server. Then use it to analyze, compare and export your experimental results.

The results are posted to a database server through a REST service. They are accessed through a command line client that talks to the service.

The commands are described [here](commands.md).

