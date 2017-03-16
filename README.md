
# Cloud Ubuntu

This project aims to build a basic docker image with Ubuntu + ssh/gateone/noVNC, it should be available easily from all over the world.

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
* https for Gateone
* https/http switch with `LAB_SECURITY`

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

## VNC/ssh Web Proxy

To save the ports and processes resources, the original noVNC and Gateone
support have been removed from `cloud-ubuntu` and a standalone noVNC and
Gateone proxy image is created and named with `cloud-ubuntu-web` and it can be
run with:

    $ ./scripts/web-ubuntu.sh

It provides web proxy function for the vnc and ssh services of the other
images.

## Login

    $ ./login/bash
    $ ./login/ssh
    $ ./login/webssh
    $ ./login/vnc

## Record and playback

### Terminal record/playback

A `showterm` command is added in the `cloud-ubuntu-dev` and its derivers, it
can be used to record the terminal operations.

    $ showterm

### VNC record/playback

noVNC can be used to record the VNC desktop operations and the record data can
be played back, to record it:

    $ VNC_RECORD=1 ./scripts/web-ubuntu.sh

The data is stored in `noVNC/recordings/` and the files are named with
`vnc.record.data.[session number]`, play back it:

    $ VNC_DATA=vnc.record.data.1 ./scripts/vnc-playback.sh

## Building

To speedup your building, please focus on such files:

* system/base/etc/resolv.conf: customize your own DNS server
* system/base/etc/apt/sources.list: customize your own ubuntu mirror site
* dockerfiles/Dockerfile.base: customize your own pip index mirror
* dockerfiles/Dockerfile.dev: customize your own gem sources
