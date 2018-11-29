# Contributing to codewatch

Thanks for your interest in `codewatch`!

We hope that this doc will help you get started if you'd like to contribute, but feel free to [join our slack workspace](https://opensource.tophat.com/#join-slack) and hop in the `#codewatch` channel if we can be of further assistance.

## Steps to get started:

1. Create the virtual environment in the `./venv` directory:
```
python -m venv venv
```

*NOTE:*
_If you want to use a specific version of python, either specify it here instead of `python` or use a tool like `pyenv` to switch. We currently support Python 2.7, 3.6, or 3.7_

2. Activate your new virtual environment for your current terminal session by running the `activate` script: `
```
. venv/bin/activate
```

*NOTE:*
_You can verify the virtual environment is active by running_
`which pip`
_You should see the full path to that venv directory you specified in step 1._

3. Install the dependencies:
```
pip install -r requirements.txt
pip install -r requirements_test.txt
```

4. Run the tests:
```
pytest
```
