#!/usr/bin/env bash
# Securely copy a file to given servers one by one using SCP with specified user.
scp "$1" "ubuntu@3.85.136.194:~/"
scp "$1" "ubuntu@54.90.0.18:~/"

