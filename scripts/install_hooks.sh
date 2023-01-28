#!/usr/bin/env bash

GIT_PRE_COMMIT='#!/bin/bash
cd $(git rev-parse --show-toplevel)
poetry run make lint
'

echo "$GIT_PRE_COMMIT" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-*