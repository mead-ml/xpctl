## building xpctl server container

### Prerequisite:

Put database credentials in [secrets](secrets) folder. The filename convention is `xpctlcred-<database_name>-<host_name>.yaml` 


### Using docker

#### Build the container

```
./build-docker.sh <database_name> <host_name>
```
#### Run the container

```
./run-docker.sh
```

You can override the database credentials put in the [secrets](secrets) folder. Run `./run-docker.sh --help` to see the options.

### Using kubernetes

```
./run-pod.sh <database_name> <host_name> <port> 
```

All this arguments are optional, the default values are 'mongo', 'local' and '5310' respectively. This runs the kubernetes service `xpctl-server` on port 5310 and forwards the system port to it. You can stop this port forward by killing the process itself.