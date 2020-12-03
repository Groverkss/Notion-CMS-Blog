# Notion-CMS-Blog
A blog with Notion as content management system. Imports content from notion and publishes it.

## Installation

> :warning: Versions of Python older than 3.6 may not work

1. Create a virtual environment using `venv`. For systems using `apt`:

```
sudo apt install python3-venv
python3 -m venv .env
```

2. Source the virtual environment and install 
dependencies from `requirements.txt`

```
source .env/bin/activate
pip3 install -r requirements.txt
```

3. You need to create a `.secrets` file with the following contents:

```
#!/bin/bash

export TOKEN_V2="<YOUR TOKEN_V2>"
export SPACE_ID="<WORKSPACE ID>"
```

- Token can be obtained from cookies as `token_v2` after logging in Notion.

- To obtain workspace id, login to Notion, use developer tools in browser.
Go to Networks tab and press `Ctrl+R` to reload the page. 
Look for `getSpaces` object. Click on the object and go to 
**Preview** tab. Expand and look for id in `spaces` value 
corresponding to the required workspace.

Give execute permissions to this file:

```
chmod +700 .secrets
```

4. Remove lines 5-7 in `.gitignore`

## Runnning

After creating the `.secrets` file, run the program as follows:

```
bash run.sh
```

## Customizing

To customize the homepage or collection page, edit the corresponding `html`
templates in `templates` directory.

## Features

- Pages/Collections are only downloaded if they have been changed. Deleted
objects are removed.
- Currently it only supports pages and collections of pages. I do not know how to
export pages inside pages without sending an email to the members.

## TODO

- Remove redundant zips and check availability straight from HTML pages

## Contributing

Feel free to open issues/pull requests. Format code with `black` formatter before
submitting please.
