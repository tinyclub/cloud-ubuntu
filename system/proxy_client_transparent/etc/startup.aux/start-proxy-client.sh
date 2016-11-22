#!/bin/bash
#
# start-proxy-client.sh -- config and start the proxy server with port and password
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../../

[ -z "$PROXY_SERVER" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_SERVER=IP:PORT'" && exit 1
PROXY_SERVER="$(echo $PROXY_SERVER | tr ':' ' ')"

[ -z "$PROXY_PWD" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_PWD=PASSWORD'" && exit 2

[ -z "$PROXY_PORT" ] && PROXY_PORT=1080

# 代理服务客户端，负责将接收到的 socks5 请求封装成 http 协议，转发给服务器端。
${TOP_DIR}/usr/local/bin/hev-socks5-client 0.0.0.0 $PROXY_PORT $PROXY_PWD $PROXY_SERVER &

sleep 1

# DNS 转发器，iptables 重定向 udp 53 端口的报文至此服务，dns-forwarder 转成 tcp 查询请求并重发出来。
${TOP_DIR}/usr/local/bin/hev-dns-forwarder 0.0.0.0 5300 8.8.8.8 &
sleep 1

# 透明代理服务，iptables 的 REDIRECT target 会将命中的 TCP 连接重定向至此服务，socks5-tproxy封装至 socks5 请求转发至 socks5-client。
${TOP_DIR}/usr/local/bin/hev-socks5-tproxy 0.0.0.0 10800 0.0.0.0 $PROXY_PORT &
sleep 1

# 导入 iptables 规则。
sudo iptables-restore ${TOP_DIR}/usr/local/bin/iptables-transparent-bypass.rules

gpasswd -d ubuntu adm
gpasswd -d ubuntu sudo
