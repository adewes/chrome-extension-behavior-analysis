# Chrome Extension Behavior Analysis

This code analyzes the behavior of Chrome extensions. It makes use of Selenium Webdriver
to get a list of extensions from the Chrome Web Store, download their source code,
install them in a browser and then open a series of websites.

It uses a modified version of [a Python proxy](https://github.com/abhinavsingh/proxy.py) to log all connections that the browser makes when opening the websites, and stores this in a report. If an extension sends data to a remote host every time a URL is openend (or batch-wise after a few opens), you will see it in the logs.

## Usage

There are three scripts to get a list of the extensions, download their source code and test them.

### Getting a list of extensions

To get a list of extensions from the Google Web Store, run *get_extension_list.py*:

    python get_extension_list.py data/extensions.json

This will scroll down the page until you hit a button on the keyboard, then it will parse all extensions that it has seen and store them in a JSON object.

### Downloading extension source code

After getting the extension list, you can download the extensions:

    python download_extensions data/extensions.json data/extensions

### Analyzing extensions

Finally, to analyze the downloaded extensions:

    python test_extensions data/extensions.json data/extensions data/reports

This will test all extensions in `data/extension.json` for which there exists a downloaded version in `data/extensions`, and store the result in `data/reports`. If an extension already has been analyzed, it will skip it.

The script contains an additional parameter `baseline`, which is set to `False` by default. If you set it to `True`, in addition to checking the browser behavior with the given extension installed, the script will check behavior without it as well, in order to provide a baseline for the connections made by opening the list of websites you provided. This is useful to distinguish "normal" tracking from extension-based tracking.

### Example Data

The `data` directory contains example data for extension source code, lists and reports.

### Questions?

Feel free to contact me.

### License

This code is public domain, use it in whichever way you like (please note the different license for the Proxy server).
