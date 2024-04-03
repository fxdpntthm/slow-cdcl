# slow-cdcl
Yet another inefficient and slow CDCL solver

### Dev Env Setup

- Install cvc5
`brew install cvc5` on MacOS or build your own using [installation instructions](https://cvc5.github.io/docs/cvc5-1.0.2/installation/installation.html)

- Python 3.12 (assumes virtualenv pyenv etc. is install)

```
$ virtualenv -p python cdcl-env
$ source cdcl-env/bin/activate
$ pip install -r requirements.txt
```

- check installation

```
$ python -i example.py
```
