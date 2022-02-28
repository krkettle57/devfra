#!/bin/bash -Ceu
docker_buildup() {
  LOCAL_UID=$(id -u $USER) LOCAL_GID=$(id -g $USER) docker-compose up -d --build
}

docker_up() {
  LOCAL_UID=$(id -u $USER) LOCAL_GID=$(id -g $USER) docker-compose up -d
}

docker_exec() {
  LOCAL_UID=$(id -u $USER) LOCAL_GID=$(id -g $USER) docker-compose exec -u user terraform bash
}

docker_down() {
  LOCAL_UID=$(id -u $USER) LOCAL_GID=$(id -g $USER) docker-compose down
}

get_credentials() {
  TOKEN_CODE=$1

  secrets=$(
    AWS_ACCESS_KEY_ID=$ASSUME_ROLE_AWS_ACCESS_KEY_ID \
      AWS_SECRET_ACCESS_KEY=$ASSUME_ROLE_AWS_SECRET_ACCESS_KEY \
      aws sts assume-role \
      --role-arn $EXEC_TF_ROLE_ARN \
      --role-session-name tf \
      --serial-number $ASSUME_ROLE_MFA_ARN \
      --token-code $TOKEN_CODE \
      --duration-seconds $(expr 3600 \* 8) \
      --region $ASSUME_ROLE_AWS_REGION
  )

  export AWS_ACCESS_KEY_ID=$(echo $secrets | jq -r .Credentials.AccessKeyId)
  export AWS_SECRET_ACCESS_KEY=$(echo $secrets | jq -r .Credentials.SecretAccessKey)
  export AWS_SESSION_TOKEN=$(echo $secrets | jq -r .Credentials.SessionToken)
  export AWS_DEFAULT_REGION=$ASSUME_ROLE_AWS_REGION
}

"$@"
