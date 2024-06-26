# Changelog

## v0.5.0 (2024-05-01)

#### New Features

* add mixin class for initializing a logger attribute

#### Docs

* update readme

## v0.4.2 (2024-02-18)

#### Refactorings

* improve type annotation coverage

## v0.4.1 (2024-01-18)

#### Docs

* add missing docstrings

## v0.4.0 (2024-01-18)

#### New Features

* subclass `logging.Logger` and add additonal functions

## v0.3.1 (2024-01-09)

#### Fixes

* add close method to imports

## v0.3.0 (2024-01-09)

#### New Features

* add close method

#### Refactorings

* change `return Log(` statements to `return self.__class__(` to appease the type checker

## v0.2.0 (2023-11-07)

#### New Features

* add functions for getting logpaths and loading Log objects from a logging.Logger instance

#### Performance improvements

* don't set handler formatter until after checking if the handler needs to be added

#### Refactorings

* import Log and Event from models

## v0.1.1 (2023-10-31)

#### Refactorings

* make logpath if it doesn't exist

## v0.1.0 (2023-10-29)

#### New Features

* add support for slicing Log objects and getting their event lengths

#### Fixes

* prevent duplicate log messages
