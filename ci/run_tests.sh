#!/usr/bin/env bash

# Usage:
# ./ci/run_tests.sh

MINIMUM_TEST_COVRAGE=77.8
RET_SUM=0

echo "pytest version"
pytest --version

MSG='Running tests'; echo $MSG
if [[ "$GITHUB_ACTIONS" == "true" ]]
then
	pytest --cov --cov-fail-under=$MINIMUM_TEST_COVRAGE
else
	pytest --cov --cov-fail-under=$MINIMUM_TEST_COVRAGE --cov-report html
fi
RET_SUM=$(($RET_SUM + $?))

exit $RET_SUM
