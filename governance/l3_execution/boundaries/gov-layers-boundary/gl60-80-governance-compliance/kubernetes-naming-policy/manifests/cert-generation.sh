#!/bin/bash
# TLS Certificate Generation Script for Naming Policy Webhook
# GL Layer: GL60-80 Governance Compliance

set -e

NAMESPACE="platform"
SERVICE_NAME="naming-policy-webhook"
SECRET_NAME="naming-policy-webhook-certs"

echo "Generating TLS certificates for naming policy webhook..."

# Create temporary directory
TMPDIR=$(mktemp -d)
trap "rm -rf ${TMPDIR}" EXIT

cd ${TMPDIR}

# Generate private key
openssl genrsa -out tls.key 2048

# Generate certificate signing request
cat <<EOF > csr.conf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[req_distinguished_name]

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = ${SERVICE_NAME}
DNS.2 = ${SERVICE_NAME}.${NAMESPACE}
DNS.3 = ${SERVICE_NAME}.${NAMESPACE}.svc
DNS.4 = ${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local
EOF

# Generate CSR
openssl req -new -key tls.key -subj "/CN=${SERVICE_NAME}.${NAMESPACE}.svc" \
  -out tls.csr -config csr.conf

# Generate self-signed certificate (valid for 1 year)
openssl x509 -req -in tls.csr -signkey tls.key -out tls.crt \
  -days 365 -extensions v3_req -extfile csr.conf

echo "Certificates generated successfully"

# Create namespace if it doesn't exist
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Create or update secret
kubectl create secret generic ${SECRET_NAME} \
  --from-file=tls.crt=tls.crt \
  --from-file=tls.key=tls.key \
  --namespace=${NAMESPACE} \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret ${SECRET_NAME} created/updated in namespace ${NAMESPACE}"

# Get CA bundle for webhook configuration
CA_BUNDLE=$(cat tls.crt | base64 | tr -d '\n')

echo ""
echo "=== CA Bundle for webhook-config.yaml ==="
echo ""
echo "Replace the caBundle field in webhook-config.yaml with:"
echo "${CA_BUNDLE}"
echo ""
echo "Or apply it automatically:"
echo "kubectl patch validatingwebhookconfiguration naming-policy-webhook \\"
echo "  --type='json' -p='[{\"op\": \"replace\", \"path\": \"/webhooks/0/clientConfig/caBundle\", \"value\":\"${CA_BUNDLE}\"}]'"
echo ""

echo "Certificate generation complete!"
