#### Starting

You can create a config file like: 

```
{
  "host": "localhost:31458/v2"
}  
```

Where `host` is the `ip:port` info from the [server](../orchestration/README.md).

You can start `xpctl` using `xpctl --config config-file`, or `xpctl --host <ip:port>`. You can save the config file at `~/xpctlcred.json` and start `xpctl` with just the command `xpctl`.
 
#### Commands

Details about any command can be found by `xpctl <command name> --help` on the terminal or `help <command-name>` inside the `xpctl` repl.
 
##### Analysis

- **results**: Provides a statistical summary of the results for a problem. A problem is defined by a (task, dataset) tuple. For each config used in the task, shows the average, and std dev and number of experiments done using config.
 
  Usage: `results [OPTIONS] TASK DATASET`

  Optionally: 
  - `--metrics`: choose metric(s) to show.
  - `--sort`: sort on this metric.
  - `--nconfig`: shows the statistical summaries for the last (sorted by time decreasing) _n_ experimental results per config. .
  - `--n`: shows _n_ results.
  - `--event_type`: show results for train/dev/test datasets. defaults to _test_. 
  - `--output`: put the results in an output file.
  - `--aggregate_fn [min|max|avg|std]`: aggregate functions to show, default is `avg` and `std`

```
(dl) x:~$ xpctl results tagger conll-iobes --metric f1 --sort f1 --n 5
       dataset                                      sha1 num_exps        f1          
                                                                        avg       std
0  conll-iobes  d96a35d18d6d68242a5bda05ff14938ce5c81269        1  0.919784  0.000000
0  conll-iobes  276e40e47da79fc5ffbb865c1860fac2557a5995       10  0.916224  0.001287
0  conll-iobes  7c683d15ffaf0d2070169ac72224bbc9ae6463d1       10  0.914731  0.002448
0  conll-iobes  c65a1050668a4a54a3ba5c65c1764df8c4b4a4b7       10  0.914512  0.001546
0  conll-iobes  5086e8f1f1df7990a1656ed7f787be511aa59752       10  0.914352  0.002199
```

- **details**: Shows the results for all experiments for a particular config (sha1). Optionally filter out by user(s), metric(s), or sort by one metric. Shows the results on the test data by default, provide event_type (train/valid/test) to see for other datasets. Optimally limit the number of results shown.

  Usage: `details [OPTIONS] TASK SHA1`
  
  Optionally: 
  - `--metric`: choose metric(s) to filter the results on. 
  - `--sort`: output all metrics but sort on one. 
  - `--n`: shows the last (by time) _n_ experimental results. 
  - `--event_type`: show results for train/dev/test datasets. defaults to _test_. 
  - `--output`: save the results in an output file.
  - `--output_fields`: which field(s) you want to see in output

```
(dl) schoudhury:~$ xpctl details tagger 276e40e47da79fc5ffbb865c1860fac2557a5995 --metric f1 --sort f1 --n 3 --output_fields username --output_fields label
  username                      label        f1
0  x  isloated_hottest_pyramids  0.917543
0  x     tuxedo-rental_local_ID  0.917454
0  x     big_Additional_Crispin  0.917152
```

#### Updating the database

- **updatelabel**: update the label for an experiment.
```
xpctl > help updatelabel
Usage: updatelabel [OPTIONS] TASK ID LABEL
  Update the label for an experiment (identified by its id) for a task
Options:
  --help  Show this message and exit.
```

- **delete**: deletes a record from the database and the associated model file from model-checkpoints if it exists.
```
Usage: xpctl delete [OPTIONS] TASK ID
  delete a record from database with the given object id. also delete the  associated model file from the checkpoint if it exists.
Options:
  --help  Show this message and exit.
```

##### Importing

- **putresult**: puts the result of an experiment in the database. Arguments:  task name (classify/ tagger/ etc.), location of the config file for the experiment, the log file storing the results for the experiment (typically <taskname>/reporting.log).
Optionally:
  - `--user`: Provide the username, by default reads from the system.
  - `--cbase`: Path to the base structure for the model checkpoint files:such as ../tagger/tagger-model-tf-11967 or /home/ds/tagger/tagger-model-tf-11967 or tagger-model-tf-123.zip. Stores the model files in a persistent model checkpoint store (will automatically zip them).
  - `--cstore`: Location of the persistent model checkpoint store, defaults to `/data/model-checkpoints`.
  - `--label`: Optionally provide a label, reads from the config if you have a description field there, else creates a default label.

```
xpctl > putresult --help
Usage: putresult [OPTIONS] TASK CONFIG LOG

  Puts the results in a database. provide task name, config file, the
  reporting log file, and the dataset file used in the experiment.
  Optionally can put the model files in a persistent storage.
  
Options:
  --user TEXT    username
  --cbase TEXT   path to the base structure for the model checkpoint
                 files:such as ../tagger/tagger-model-tf-11967 or
                 /home/ds/tagger/tagger-model-tf-11967
  --cstore TEXT  location of the model checkpoint store
  --label TEXT   label for the experiment
  --help         Show this message and exit.
xpctl >
```

```
x$ xpctl putresult classify sst2.json reporting-4444.log datasets.yaml --user me --cbase classify-model-tf-4444.zip --cstore <my-home>/model-checkpoints
```
The record id returned by this command can be used in *putmodel*

- **putmodel**: save model files in a persistent location. The location can be provided by the option -cstore, by default it is `/data/model-checkpoints` directory in your machine. 

```
xpctl > putmodel --help
Usage: putmodel [OPTIONS] TASK ID CBASE
  Puts the model from an experiment in the model store and updates the
  database with the location. Arguments:  task name (classify/ tagger), record id, and
  the path to the base structure for the model checkpoint files such as
  ../tagger/tagger-model-tf-11967 or /home/ds/tagger/tagger-model-tf-11967
Options:
  --cstore TEXT  location of the model checkpoint store
  --help         Show this message and exit.

```

##### Exporting

- **getmodelloc** : shows the model location for an id (**id, not SHA1**. An experiment can be run multiple times using the same config). 
```
xpctl > help getmodelloc
Usage: xpctl getmodelloc [OPTIONS] TASK ID
  get the model location for a particular task name (classify/ tagger) and record id
Options:
  --help  Show this message and exit.
```

```
xpctl > getmodelloc classify 5b1aacb933ed5901dc545af8

model loc is <store-path>/67105e2108885c5ee08e211537fbda602f2ba254/1.zip

```

- **config2json**
```
xpctl > help config2json
Usage: config2json [OPTIONS] TASK SHA FILENAME
  Exports the config file for an experiment as a json file. Arguments:
  task name (classify/ tagger), sha1 for the experimental config, output file path
Options:
  --help  Show this message and exit.
```
Here `sha1` is the model-checkpoint id.

```
xpctl > config2json classify 67105e2108885c5ee08e211537fbda602f2ba254 <path>/c_SST2.json

```

##### Summary


- **lbsummary**: provides a description of all tasks in the leaderboard. 
```
xpctl > lbsummary --help
Usage: lbsummary [OPTIONS]
  Provides a summary of the leaderboard. Options: taskname. If you provide a taskname, it will show all users, and datasets for that task. 
Options:
  --task TEXT
  --help       Show this message and exit.

```
