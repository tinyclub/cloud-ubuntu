
# Cloud Ubuntu

This project aims to build a basic docker image with Ubuntu + ssh/tty.js/noVNC, it should be accessed easily from all over the world.

* ssh, traditional ssh protocol, require ssh client, support graphic/console
* noVNC, remote graphic desktop via web browser, platform independent
* tty.js, remote tty console via web browser, platform independent

It is based on:

* [tty.js](https://github.com/chjj/tty.js/)
* [noVNC](https://github.com/kanaka/noVNC)
* [websockify](https://github.com/kanaka/websockify)
* [docker-ubuntu-vnc-desktop](https://github.com/fcwu/docker-ubuntu-vnc-desktop)
* [docker-eclipse-novnc](https://github.com/mccahill/docker-eclipse-novnc.git)

It is functional, scalable, minimal but with necessary security enhancement:

* fail2ban for ssh login failure limitation.
* https for tty.js: ttyjs/server.{key,crt} from `gen_pem.sh`
* https for noVNC: noVNC/utils/self.pem from `gen_pem.sh`

People can build their own cloud environment with:

    # FROM tinylab/cloud-ubuntu

To customize the key/cert, please rerun `gen_pem.sh`.

## Usage

    $ ./build                 # build it from scratch
    $ ./rm                    # remove the container before run a new one
    $ ./run                   # run a new container

The ssh/noVNC/tty.js login password can be set via the according environment
variables in `./run`: `UNIX_PWD`, `VNC_PWD`, `TTY_PWD`. the default passwords
are `ubuntu`.

## Services

| Protocol    |  Internal port  | External port|
|------------:|----------------:|-------------:|
|ssh          | 22              | 2222         |
|noVNC        | 6080            | 6080         |
|tty.js       | 3000            | 3000         |

## Login

    $ ./login-ssh
    $ ./login-tty.js
    $ ./login-novnc
