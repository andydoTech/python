#!/bin/sh
if [ $# -lt 2 ]
then
   echo "$0 from_branch to_branch"
   exit 1
fi

from_branch=$1
to_branch=$2
git checkout $from_branch
git checkout $to_branch
git merge $from_branch
git push origin $to_branch
