# https://github.com/kanaka/websockify/wiki/Encrypted-Connections

TOP_DIR=$(cd $(dirname $0) && pwd)

PEM=${TOP_DIR}/noVNC/utils/self.pem

[ -n "$AUTO" -a "$AUTO" == "1"  ] && BATCH=-batch

openssl req $BATCH -new -x509 -days 365 -nodes -out $PEM -keyout $PEM
