<p align="center">
  <img src="art/cmt-cli.svg" alt="cmt-cli logo" width="400">
</p>

# cmt-cli

<p>
  <a href="https://pypi.org/project/cmt-cli/"><img src="https://img.shields.io/pypi/v/cmt-cli.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/cmt-cli/"><img src="https://img.shields.io/pypi/pyversions/cmt-cli.svg" alt="Python versions"></a>
  <a href="https://github.com/bijaydas/cmt/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/status-alpha-orange.svg" alt="Alpha status">
</p>

<p>
  AI-powered CLI tool that analyzes your staged Git changes and suggests a professional commit message.
</p>

> **Note:** `cmt-cli` is in **alpha**. Expect breaking changes, rough edges, and incomplete features until a stable
> release.

## Features

- Analyzes staged Git changes (added, modified, deleted, and renamed files, plus diffs)
- Generates a commit message and description using OpenAI (via LangChain)
- Review, edit (in `vim`), or reject the suggested message before committing
- Caches suggestions per diff/model to avoid redundant API calls
- Simple configuration for your OpenAI API key and model
  ``

## Installation

```bash
uv tool install cmt-cli
```

Requires Python 3.12+.

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

### Configuration

Before first use, configure your OpenAI API key and model:

```bash
cmt config set
```

To view your current configuration:

```bash
cmt config get
```

## License

MIT
