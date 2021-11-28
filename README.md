# MERchain

### What is it?

MERchain is an auction website written in Django which implements blockchain notarization at the end of every auction.

### Set up

Once you have downloaded the source code from Github, you should create a virtual environment to launch the website locally. 

Be sure you have Python installed in your machine, this project is built with Python 3.9.5.

In your workspace run this command to create a new venv:

```
python -m venv venv
```

Be sure to activate your venv to install there all the requirements, on Windows using PowerShell:

```
path\to\venv\Scripts\Activate.ps1
```

Once you're working in the venv, install there all the requirements:

```
pip install -r path/to/requirements.txt
```

Once you are in the MERchain folder run these commands:

```
python manage.py makemigrations
python manage.py migrate
```

Now you can launch the website locally running:

```
python manage.py runserver
```

### Start your auctions

Using the platform is really intuitive: create some accounts, open some auctions and start to bid on some products.
Every auction has a deadline set by the seller, if the auction is successful a JSON containing all the details related to the operation is hashed and broadcasted to the Ethereum blockchain (Ropsten testnet).

### License

GPL-3.0-or-later
