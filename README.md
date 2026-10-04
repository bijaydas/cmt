<p align="center">
  <img src="https://raw.githubusercontent.com/bijaydas/cmt/refs/heads/main/art/cmt-cli.svg" alt="cmt-cli logo" width="400">
</p>

# cmt-cli

<p>
  <a href="https://pypi.org/project/cmt-cli/"><img src="https://img.shields.io/pypi/v/cmt-cli.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/cmt-cli/"><img src="https://img.shields.io/pypi/pyversions/cmt-cli.svg" alt="Python versions"></a>
  <a href="https://github.com/bijaydas/cmt/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/status-beta-yellow.svg" alt="Beta status">
  <a href="https://github.com/bijaydas/cmt/actions/workflows/test.yml"><img src="https://github.com/bijaydas/cmt/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
</p>

<p>
  AI-powered CLI tool that analyzes your staged Git changes and suggests a professional commit message.
</p>

> **Note:** `cmt-cli` is in **beta**. Expect occasional breaking changes and rough edges until a stable release.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Updating](#updating)
- [Uninstalling](#uninstalling)
- [Privacy & Cost](#privacy--cost)
- [Development](#development)
- [License](#license)

## Features

- Analyzes staged Git changes (added, modified, deleted, and renamed files, plus diffs)
- Generates a commit message and description using OpenAI (via LangChain)
- Review, edit (in `vim`), or reject the suggested message before committing
- Caches suggestions per diff/model to avoid redundant API calls
- Simple configuration for your OpenAI API key and model

## Requirements

- Python 3.12+
- Git
- `vim` installed and available on your `PATH` (used for the `e` / edit option)
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Installation

```bash
uv tool install cmt-cli
```

## Configuration

Before first use, configure your OpenAI API key and model:

```bash
cmt config set
```

If no model is specified, `cmt-cli` defaults to `gpt-4o-mini`. Configuration is stored in `~/.config/cmt/config.ini`.

To view your current configuration:

```bash
cmt config get
```

## Usage

Stage your changes as usual, then run:

```bash
git add .
cmt suggest
```

You'll be shown a suggested commit message and can choose to:

- `y` — commit with the suggested message
- `e` — edit the message in `vim` before committing
- `n` — abort

Other commands:

```bash
cmt --version   # print the installed version
cmt update      # check whether a newer version is available
```

## Updating

```bash
cmt update
```

This checks PyPI for a newer release. If one is available, upgrade it with:

```bash
uv tool upgrade cmt-cli
```

## Uninstalling

```bash
uv tool uninstall cmt-cli
```

## Privacy & Cost

`cmt suggest` sends your staged diff to the OpenAI API to generate a commit message, so avoid staging secrets or sensitive data before running it. Each request uses your own OpenAI API key and is subject to OpenAI's standard usage pricing; `cmt-cli` caches suggestions per diff/model locally (`~/.config/cmt/cache`) to help avoid redundant, repeat API calls.

## Development

Clone the repo and install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/bijaydas/cmt.git
cd cmt
uv sync --all-groups
```

Run the test suite and linter:

```bash
uv run pytest
uv run ruff check .
```

## License

This project is licensed under the terms of the MIT license.
