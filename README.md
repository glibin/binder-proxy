# Binder proxy for faster frontend development

This proxy helps to work faster and more productive with binder frontend development.

You will get higher productivity because:

 * PHP loads static files synchronously (or with some instances at aws sandbox)
 * It takes some time to upload your code to aws sandbox
 * Files served faster from local then from remote in America :-)

All you have to do is use this proxy which makes all project's css/js files serve locally and all other requests will be passed to sandbox/dev instance.
Also, you can configure or add any other logic for paths you need (for e.g. mocks).

# Installation

## Mac OS X/Ubuntu

This systems comes with bundled Python 2.7 so you can use it (but I highly recommend to use Python 3 :-)).

 * clone this repo and run the following commands in terminal at this repo directory
 * make sure you have `pip` installed: Ubuntu: `sudo apt-get install python-pip`, Mac: `sudo easy_install pip`
 * run `sudo pip install -r requirements.txt` (if you know what `virtualenv` is and using it, run this command without `sudo`)
 * that's all ;-)

## Windows

 * go at https://www.python.org/downloads/windows/ and download/install 3.4.x version (there should be an installer)
 * don't forget to check `Add python.exe to Path` checkbox
 * clone this repo and run the following commands in terminal (`cmd.exe`) at this repo directory
 * run `pip install -r requirements.txt`
 * done :-)

## Usage

Run:

```
python proxy.py --static_path=<your_binder_path>/web --proxy_url=<url_to_your_binder>
```

For example:

```
python proxy.py --static_path=../profile-search-ui/web --proxy_url=http://sandbox1.agate.upwork.com:32819
```

Proxy url could be any url (local, sandbox, dev) to your instance.

After that you can go [http://127.0.0.1:9999](http://127.0.0.1:9999) and you are done :) For e.g. `profile-search` path would be `http://127.0.0.1:9999/o/profiles/browse/`

Also you can put all this command line arguments to `config/local.cfg` file. All available arguments are available with `python proxy.py --help`.


So, now you need to just run `grunt watch` to monitor and rebuild your js/css changes and they would be automatically served.

This proxy uses [tortik](https://github.com/glibin/tortik) and if you want to see some magic just add `debug` parameter to the url, for e.g. `http://127.0.0.1:9999/o/profiles/browse/?debug`.
