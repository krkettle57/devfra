#!/bin/bash -Ceu

USER_ID=${LOCAL_UID:-9001}
GROUP_ID=${LOCAL_GID:-9001}
USER="user"

echo "Starting with UID: $USER_ID"
usermod -u $USER_ID -g $GROUP_ID $USER
export HOME="/home/${USER}"
chmod 777 -R $HOME
exec /usr/sbin/gosu $USER "$@"
