#!/bin/bash -Ceu

WORKDIR=$(
  cd $(dirname $0)
  pwd -P
)

init() {
  DEVFRA_FILEPATH=$1
  if [ ! -f "${WORKDIR}/.terraform.lock.hcl" ]; then
    terraform init
  fi

  if [ ! -f "${WORKDIR}/config/tfvar.json" ]; then
    python ../devfrapy/src/main.py $DEVFRA_FILEPATH $WORKDIR
  fi
}

plan() {
  DEVFRA_FILEPATH=$1
  init $DEVFRA_FILEPATH
  terraform plan -var-file "${WORKDIR}/config/tfvar.json"
}

apply() {
  DEVFRA_FILEPATH=$1
  init $DEVFRA_FILEPATH
  terraform apply -var-file "${WORKDIR}/config/tfvar.json"
}

destroy() {
  if [ ! -f "${WORKDIR}/config/tfvar.json" ]; then
    echo "tfvar.json does not exit."
    exit 1
  fi

  terraform destroy -var-file "${WORKDIR}/config/tfvar.json"
}

"$@"
