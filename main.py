from notion.client import NotionClient
from os import environ
from pprint import pprint

token = environ.get("TOKEN_V2")
client = NotionClient(token_v2=token)

def get_block(block_id):
    collection_block = client.get_block(block_id, force_refresh=True)
    return collection_block

def build_pages(space_id):
    workspace = client.get_space(space_id, force_refresh=True)

    # Get all pages from the workspace
    page_ids = workspace.get(force_refresh=True)['pages']

    for page_id in page_ids:
        page_block = get_block(page_id) 
        pprint(page_block.type)

def main():
    space_id = environ.get("SPACE_ID")
    build_pages(space_id)

if __name__ == '__main__':
    main()
