#!/usr/bin/env bash

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
# this command creates symlink to our pre-commit script
ln -s ../../script/pre-commit.bash $GIT_DIR/hooks/pre-commit
echo "Done"!

# https://www.andrewcbancroft.com/blog/musings/make-bash-script-executable/
# https://medium.com/@yagizcemberci/automate-unit-tests-with-git-hooks-e25e8b564c92