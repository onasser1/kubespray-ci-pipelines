#!/bin/bash

# Sample inputs (in real script, these come from cat VERSION or github.event.release.tag_name)
RELEASE="v2.30.0"  # Dynamic: could be $(cat VERSION) or ${{ github.event.release.tag_name }}
p_major=2
p_minor=29
p_patch=0  # Assuming prev was v2.29.0

# Strip 'v' prefix if present
current_version="${RELEASE#v}"

# Parse current into components (MAJOR MINOR PATCH)
IFS='.' read -r c_major c_minor c_patch <<< "$current_version"

# Ensure they are integers (fallback to 0 if parsing fails)
c_major=${c_major:-0}
c_minor=${c_minor:-0}
c_patch=${c_patch:-0}
p_major=${p_major:-0}
p_minor=${p_minor:-0}
p_patch=${p_patch:-0}

# Determine bump type
bump_type="patch"  # Default
if [ "$c_major" -gt "$p_major" ]; then
  bump_type="major"
elif [ "$c_minor" -gt "$p_minor" ]; then
  bump_type="minor"
fi

echo "Bump type: $bump_type"
echo "Current: v${c_major}.${c_minor}.${c_patch}"
echo "Previous major/minor/patch: ${p_major}.${p_minor}.${p_patch}"

# Compute next_expected_release based on bump type (increment current, reset lower parts to 0)
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

echo "Next expected release: $next_expected_release"

# In GitHub Actions: Export as step output for use elsewhere
echo "next_expected_release=$next_expected_release" >> "$GITHUB_OUTPUT"
echo "bump_type=$bump_type" >> "$GITHUB_OUTPUT"