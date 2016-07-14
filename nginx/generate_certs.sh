#!/bin/bash

cat <<EOF
Based on marvambass/nginx-ssl-secure container
EOF

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CERTS_DIR="${DIR}/external"
if [ ! -d "$CERTS_DIR" ]; then
  # Control will enter here if $DIRECTORY exists.
  echo "Creating $CERTS_DIR (using sudo):"
  sudo mkdir -p $CERTS_DIR
  sudo chown -R $USER:staff $CERTS_DIR
fi

if [ -z ${DH_SIZE+x} ]
then
  >&2 echo ">> no \$DH_SIZE specified using default" 
  DH_SIZE="2048"
fi


DH="${CERTS_DIR}/dh.pem"

if [ ! -e "$DH" ]
then
  echo ">> seems like the first start of nginx"
  echo ">> doing some preparations..."
  echo ""

  echo ">> generating $DH with size: $DH_SIZE"
  openssl dhparam -out "$DH" $DH_SIZE
fi

if [ ! -e "/etc/nginx/external/cert.pem" ] || [ ! -e "/etc/nginx/external/key.pem" ]
then
  echo ">> generating self signed cert"
  openssl req -x509 -newkey rsa:4086 \
  -subj "/C=XX/ST=XXXX/L=XXXX/O=XXXX/CN=localhost" \
  -keyout "${CERTS_DIR}/key.pem" \
  -out "${CERTS_DIR}/cert.pem" \
  -days 3650 -nodes -sha256
fi
