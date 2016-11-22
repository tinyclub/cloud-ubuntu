# https://github.com/kanaka/websockify/wiki/Encrypted-Connections

TOP_DIR=$(cd $(dirname $0) && pwd)

KEY=${TOP_DIR}/system/base/etc/nginx/cert.key
CERT=${TOP_DIR}/system/base/etc/nginx/cert.crt
PEM=${TOP_DIR}/noVNC/utils/self.pem

[ -n "$AUTO" -a "$AUTO" == "1"  ] && BATCH=-batch

openssl req $BATCH -x509 -nodes -days 365 -newkey rsa:2048 -out $CERT -keyout $KEY

cat $CERT $KEY > $PEM
