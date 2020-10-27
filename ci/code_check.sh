#!/usr/bin/env bash

# Took pretty much all of this from:
# https://github.com/pandas-dev/pandas/blob/fbd13a95c65571677632d177a35577baacd5d2ba/ci/code_checks.sh

# Usage:
# ./ci/code_check.sh			# Run all the checks
# ./ci/code_checks.sh doctest	# Run doctest checks
# ./ci/code_check.sh lint		# Run lint checks
# ./ci/code_checks.sh type		# Run typing checks

RET_SUM=0
CHECK_TYPE=$1


if [[ "$GITHUB_ACTIONS" == "true" ]]
then
	FLAKE8_FORMAT="##[error]%(path)s:%(row)s:%(col)s:%(code)s:%(text)s"
else
	FLAKE8_FORMAT="default"
fi

# doctest
if [[ -z "$CHECK_TYPE" || "$CHECK_TYPE" == "doctest" ]]
then
	echo "pytest version"
	pytest --version

	MSG='Doctests src/' ; echo $MSG
	pytest -q --doctest-modules src/
	RET_SUM=$(($RET_SUM + $?))

	echo ""
	MSG='DONE' ; echo $MSG
	echo ""
fi

# lint
if [[ -z "$CHECK_TYPE" || "$CHECK_TYPE" == "lint" ]]
then
	# Black
	echo "Black version"
	black --version

	MSG='Checking black formatting on src/' ; echo $MSG
	black --check src/
	RET_SUM=$(($RET_SUM + $?))

	MSG='Checking black formatting on tests/' ; echo $MSG
	black --check tests/
	RET_SUM=$(($RET_SUM + $?))
	echo ""
	MSG='DONE' ; echo $MSG
	echo ""

	echo "flake8 --version"
	flake8 --version

	MSG='Check linting on src/' ; echo $MSG
	flake8 --format="$FLAKE8_FORMAT" src/
	RET_SUM=$(($RET_SUM + $?))

	MSG='Check linting on tests/' ; echo $MSG
	flake8 --format="$FLAKE8_FORMAT" tests/
	RET_SUM=$(($RET_SUM + $?))
	echo ""
	MSG='DONE' ; echo $MSG
	echo ""

	# Isort
	echo "Isort version"
	isort --version-number

	MSG='Check import formatting on src/' ; echo $MSG
	ISORT_CMD="isort --quiet --check-only src/"
	if [[ "$GITHUB_ACTIONS" == "true" ]]
	then
		eval $ISORT_CMD | awk '{print "##[error]" $0}'
		RET_SUM=$(($RET_SUM + ${PIPESTATUS[0]}))
    else
		eval $ISORT_CMD
	fi
	RET_SUM=$(($RET_SUM + $?))

	MSG='Check import formatting on tests/' ; echo $MSG
	ISORT_CMD="isort --quiet --check-only tests/"
	if [[ "$GITHUB_ACTIONS" == "true" ]]
	then
		eval $ISORT_CMD | awk '{print "##[error]" $0}'
		RET_SUM=$(($RET_SUM + ${PIPESTATUS[0]}))
	else
		eval $ISORT_CMD
	fi
	RET_SUM=$(($RET_SUM + $?))

	echo ""
	MSG='DONE' ; echo $MSG
	echo ""
fi

# typing
if [[ -z "$CHECK_TYPE" || "$CHECK_TYPE" == "type" ]]
then
	echo "Mypy version"
	mypy --version

	MSG='Performing static type checking on src/ and tests/' ; echo $MSG
	mypy src/ tests/
	RET_SUM=$(($RET_SUM + $?))

	echo ""
	MSG='DONE' ; echo $MSG
	echo ""
fi

exit $RET_SUM

