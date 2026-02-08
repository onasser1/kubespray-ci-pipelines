#!/bin/bash

CURRENT_RELEASE=$(cat VERSION)
PREVIOUS_RELEASE=$(git tag --sort=-version:refname | head -1)

current_version_number="${CURRENT_RELEASE#v}"
previous_version_number="${PREVIOUS_RELEASE#v}"

IFS='.' read -r c_major c_minor c_patch <<< "$current_version_number"
IFS='.' read -r p_major p_minor p_patch <<< "$previous_version_number"

c_major=${c_major:-0}
c_minor=${c_minor:-0}
c_patch=${c_patch:-0}
p_major=${p_major:-0}
p_minor=${p_minor:-0}
p_patch=${p_patch:-0}

bump_type="patch"  # Default
if [ "$c_major" -gt "$p_major" ]; then
  bump_type="major"
elif [ "$c_minor" -gt "$p_minor" ]; then
  bump_type="minor"
fi


case $bump_type in
  "major")
    next_major=$(($c_major + 1))
    next_minor=0
    next_patch=0
    ;;
  "minor")
    next_major=$c_major
    next_minor=$(($c_minor + 1))
    next_patch=0
    ;;
  "patch")
    next_major=$c_major
    next_minor=$c_minor
    next_patch=$(($c_patch + 1))
    ;;
esac

next_expected_release="v${next_major}.${next_minor}.${next_patch}"
echo "current release: $CURRENT_RELEASE"
echo "NEXT EXPECTED RELEASE: $next_expected_release"
# echo "next_expected_release=$next_expected_release" >> "$GITHUB_OUTPUT"
echo "bump_type=$bump_type" # >> "$GITHUB_OUTPUT"