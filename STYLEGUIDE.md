# Code Style Guide

## Overview
This document outlines the coding standards and conventions for our project. It's intended to promote code consistency and readability across the entire development team.

## Version Control - Git Flow

We use the Git Flow method for branching and merging in our project. This approach involves several branch types:

- feature/: For new features or enhancements.
- fix/: For bug fixes.
- release/: For release preparation (testing, bug fixing).
- hotfix/: For urgent fixes to be applied to the production version.
- develop: The primary branch where all development happens.
- master/main: The production branch, containing stable and released versions.

Each feature, fix, or improvement should be developed in its own branch and merged back into develop after completion.

## Documentation and Comments

- All documentation, including comments and docstrings, should be written in English.
- Comments should be clear and concise, providing valuable information that isn't immediately obvious from the code itself.
- Docstrings are mandatory for all public classes, methods, and functions, and should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

## Coding Conventions

### Quotation Marks

- Always use double quotes (`" "`) for strings, unless the string contains double quotes, in which case single quotes (`' '`) are acceptable.

### Linters and Formatters

To ensure code quality and style consistency, we use the following tools:

- Ruff: A fast Python linter for catching errors and enforcing a coding standard.
- Mypy: A static type checker to ensure that type annotations are correct.
- Black: An uncompromising code formatter that formats the code in a uniform style.

## Setting Up Linters and Formatters

Instructions on setting up and using these tools will be provided separately. Ensure that your code passes all checks by these tools before submitting a merge request.

## Conclusion

Adhering to these guidelines helps maintain a clean, consistent, and error-free codebase. It's crucial for effective collaboration and the long-term maintainability of the project. If you have any suggestions for improving these guidelines, please submit a pull request with your proposed changes.
