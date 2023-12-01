# Experiments

A collection of fun things I tried.
A few ground rules for myself:
- Each experiment should have it's own module under `experiments`
- Each experiment should be well-documented on the `blog`
- If possible, each experiment should be deployed so you can interact with it in the real world
- Have fun 🙂

## Setup

This setup assumes you have conda installed.
Find more info [here](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html) about installing and setting up conda.

Replace `{env name}` below with your desired conda environment name.

1. Create a conda environment for the app
    ```shell
    conda create -n {env name} python=3.12
    ```

2. Activate the conda environment
    ```shell
    conda activate {env name}
    ```

3. Install app dependencies
    ```shell
    pip install .
    ```

4. Add your conda environment to your IDE

5. Install pre-commit and commit-msg hooks for all projects
    ```shell
    make pre-commit-install
    ```

## Contributing

### Commit Messages

Commit messages must be in the format `{emoji} {message}`.
Silly requirement? Maybe.
But does it make GitHub look good? Definitely.

Standard emoji to start the commit message with are:

```
🐞: Bug fix
🎉: Enhancement/feature
📝: Documentation
🧪: Added or modified tests
🧹: Maintenance (refactoring, fix typo, etc.)
💾: Development update
```
