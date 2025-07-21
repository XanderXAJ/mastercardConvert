# MasterCard Currency Converter

Command line interface to MasterCard currency conversions.

It uses the currencies as can be found in the [MasterCard Currency Conversion Tool](https://www.mastercard.com/global/currencyconversion/index.html).

## Requirements

This project uses [Python 3][python] & [uv][uv].

[python]: https://www.python.org/
[uv]: https://docs.astral.sh/uv/

## Quick installation

1. Use your favourite tool manager to install directly from source:

    ```shell
    # uv
    uv tool install git+https://github.com/XanderXAJ/mastercardConvert.git
    # pipx
    pipx install git+https://github.com/XanderXAJ/mastercardConvert.git
    ```

2. Run the project via `mc`:

    ```shell
    mc 10 usd gbp
    ```

## Source Installation

1. Clone the repository.
2. Use your favourite tool manager to install from source:

    ```shell
    # uv
    uv tool install .
    # pipx
    pipx install .
    ```

3. Run the project via `mc`:

    ```shell
    mc 10 usd gbp
    ```

## Usage

To use it, simply call `mc` with the amount you're converting, and the currency before and after.

For example, if I had paid 10 US Dollars and wanted to know how much that was in British Pound Sterling (you can use lower or upper case for currencies):

```shell
mc 10 usd gbp
```

## Update

Run the appropriate command for your tool manager:

`uv`:

```shell
# Direct source install
uv tool install --reinstall git+https://github.com/XanderXAJ/mastercardConvert.git
# Local clone install
uv tool install --reinstall .
```

`pipx`:

```shell
# Reinstall/refresh using original installation method
pipx reinstall mastercardconvert
# Override installation method to local code
pipx install . --force
```

## Development

For development, this project uses [uv][uv] to isolate its environment.
[Follow its installation instructions.](https://docs.astral.sh/uv/getting-started/installation/)

Run the in-progress version of the code:

```bash
uv run python -m mc 10 usd gbp
```

`uv` will automatically create the virtualenv and install dependencies when the environment doesn't exist or is out of date.
(Use `uv sync` if you want to be sure.)

Note: `-m` is used to ensure imports work in the same way as they do when installing via tool managers.

To test installations, follow the **Update** instructions above.

This project uses `unittest` for testing.
To run the tests:

```bash
uv run python -m unittest discover -s mc
```

Use `uv run` to run commands inside the virtualenv from outside the virtualenv.

### Default branch rename

On 2025-06-11, I renamed the default branch to `main`.
If you were one of the ~4 or so forks at the time of that happening:

1. Apologies for the inconvenience 😇
2. Here are instructions to update your repo to the new branch name.

    This does **move and delete branches**, so double-check before running anything, I believe the instructions are correct but I'm not responsible if anything goes wrong, etc. 🙂
    It also assumes the clone uses an `origin` upstream -- change that if you've used a different name:

    ```shell
    # Rename branch
    git branch -m master main
    # Push the new branch, simultaneously updating the upstream tracking
    git push -u origin main
    # Delete the old remote branch
    git push -d origin master
    ```

## Known issues

MasterCard don't tend to publish today's exchange rates until part way through the day; this is also affected by your time zone.
This means that sometimes the exchange rates for today might not be available.
The script automatically uses the latest rates by default.
While it means that the exchange rates my not accurately reflect what is used in your transaction, the differences tend to be small.

MasterCard don't publish new exchange rates on Saturdays or Sundays.  Not much that can be done there!
