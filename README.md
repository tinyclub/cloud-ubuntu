
# Cloud Ubuntu

This project aims to build a basic docker image with Ubuntu + ssh/gateone/noVNC, it should be accessed easily from all over the world.

* ssh, traditional ssh protocol, require ssh client, support graphic/console
* noVNC, remote graphic desktop via web browser, platform independent
* gateone, web ssh client, platform independent

It is based on:

* [gateone](https://github.com/liftoff/GateOne)
* [noVNC](https://github.com/kanaka/noVNC)
* [websockify](https://github.com/kanaka/websockify)
* [docker-ubuntu-vnc-desktop](https://github.com/fcwu/docker-ubuntu-vnc-desktop)
* [docker-eclipse-novnc](https://github.com/mccahill/docker-eclipse-novnc.git)

It is functional, scalable, minimal but with necessary security enhancement:

* fail2ban for ssh login failure limitation.
* https for noVNC: noVNC/utils/self.pem from `gen_pem.sh`

People can build their own cloud environment with:

    # FROM tinylab/cloud-ubuntu

To customize the key/cert, please rerun `gen_pem.sh`.

## Usage

    $ ./build                 # build it from scratch
    $ ./rm                    # remove the container before run a new one
    $ ./run                   # run a new container

The ssh/noVNC/gateone login password can be set via the according environment
variables in `./run`: `UNIX_PWD`, `VNC_PWD`,  the default users and passwords
are `ubuntu`.

## Services

| Protocol     |  Internal port  | Default External port|
|-------------:|----------------:|---------------------:|
|ssh           | 22              | 2222                 |
|gateone/webssh| 443             | 4433                 |
|noVNC         | 6080            | 6080                 |

## Login

    $ ./login/bash
    $ ./login/ssh
    $ ./login/webssh
    $ ./login/vnc

## Building

To speedup your building, please focus on such files:

* system/base/etc/resolv.conf: customize your own DNS server
* system/base/etc/apt/sources.list: customize your own ubuntu mirror site
* dockerfiles/Dockerfile.base: customize your own pip index mirror
* dockerfiles/Dockerfile.dev: customize your own gem sources
