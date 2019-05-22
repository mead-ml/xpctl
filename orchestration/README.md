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

This will run the `xpctl server` at `<host_name>:5310/v2`. You can change the port (5310) and override the database credentials put in the [secrets](secrets) folder. Run `./run-docker.sh --help` to see all options.

### Using kubernetes

```
./run-pod.sh <database_name> <host_name> <docker_command> 
```

All this arguments are optional, the default values are `mongo`, `local` and `docker` respectively. In some ubuntu installation the `docker_command` is going to be `microk8s.docker`.

Do `kubectl describe services xpctl-server`, and look at the line 
that starts with `NodePort` to get the ip. `xpct-server` services will be available at `<host_name>:<ip>/v2`
