# Pin_Analysis
Scientific computing tools relevant to evaluating the definition of a failure
Scientific computing tools for identifying a failure once cartridge is loaded with oil

## Versioning
Versions are tagged in git using the "Semantic Versioning 2.0" standard beginning with 0.1.0.
For details, please refer to: [http://semver.org/spec/v2.0.0.html](http://semver.org/spec/v2.0.0.html)

Version is manually updated using a text source file

## Summary
A version is of the form MAJOR.MINOR.PATCH, where each gets incremented for the following:

 * MAJOR, for incompatible API changes
 * MINOR, for functionality added in a backwards-compatible manner
 * PATCH, for backwards-compatible bug fixes

 The MAJOR patch will be zero for initial dev.

## Branching Model
Development is intended to follow the Git Flow branching model.

For details, please refer to: [http://nvie.com/posts/a-successful-git-branching-model/](http://nvie.com/posts/a-successful-git-branching-model/)

In summary, development takes place in feature branches (named anything except master, develop, release-\*, or hotfix-\*), then moved into release branches (release-\*), then tagged when released, and merged back into development and master branches.  For our purposes, build artifacts (elf, bin, hex, map files) are included in the release branches so that the build output is available once tagged.

## Install Anaconda 5.0.1 (64 bit), python 2.7.14
https://www.anaconda.com/download/
Anaconda>=5.0.1
python>=2.7.14
## Ensure relevant modules
relevant modules
numpy>=1.13.3

## Installing the tools for a Check Pins ADE (LAUNCH SUBPROCESS BLOCK)
Move Pin_Analysis lower directory folder into the users C:/src/python
Load the InstrumentSpecificDatabase folder with the local machine overall set average (may change with new cartridges)
