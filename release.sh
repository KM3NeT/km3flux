#!/usr/bin/env zsh
set -e
MODULE=km3flux

if [ $# -eq 0 ]
  then
    echo "No version number supplied"
    exit 1
fi

export VERSION=$1

git checkout master
git pull

vim $MODULE/__version__.py
git add $MODULE/__version__.py

git commit -m "Bump version number"

TITLE="${MODULE} ${VERSION}"
echo "${TITLE}" > docs/version.txt
echo "$(printf '=%.0s' {1..${#TITLE}})" >> docs/version.txt
git add docs/version.txt
git commit -m "update version tag in docs"

vim CHANGELOG.rst
git add CHANGELOG.rst
git commit -m "Bumps changelog"

rm -rf dist/*
python setup.py sdist
twine upload dist/*

git checkout master
git push
git push --tags
