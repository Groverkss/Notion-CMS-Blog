import notion
from zipfile import ZipFile
from notion.client import NotionClient
from os import environ
from pathlib import Path
from cms.exporter import Exporter
from jinja2 import Template

token = environ.get("TOKEN_V2")
client = NotionClient(token_v2=token)

exporter = Exporter(client)
new_exports = []


def get_block(block_id):
    """Gets a notion block"""
    block = client.get_block(block_id, force_refresh=True)
    return block


def build_page(page_block):
    """Exports a page from notion. Does not export the page if
    the page is already available in exports. Returns a Path class
    for the corresponding htmk file"""

    title = page_block.title
    page_id = page_block.id

    page_info = page_block.get(force_refresh=True)
    last_edited_time = page_info["last_edited_time"]

    output_dir_path = Path("exports/")
    export_file_name = f"{page_id}|{last_edited_time}.zip"
    output_dir_path /= export_file_name

    if output_dir_path.is_file():
        print(f"No changes in {title}")
    else:
        print(f"Downloading {title}")
        output_dir_path = exporter.download_page(page_id, title, output_dir_path)

    if output_dir_path is None:
        return None
    new_exports.append(output_dir_path)

    outpath = Path("pages/")
    with ZipFile(output_dir_path, "r") as zip_ref:
        print(f"Unziping {title}")
        zip_ref.extractall(outpath)
        zip_files = zip_ref.infolist()

    # Get HTML file name from zip
    zip_files = [
        zip_file.filename
        for zip_file in zip_files
        if zip_file.filename.endswith(".html")
    ]
    return outpath / zip_files[0], title


def build_collection(collection_block):
    """Traverses through a collection and builds its pages."""
    collection = collection_block.collection
    collection_info = collection.get(force_refresh=True)

    try:
        description = collection_info["description"][0][0]
    except:
        description = None

    title = collection_info["name"][0][0]
    collection_id = collection_info["id"]

    pages = []
    for row in collection.get_rows():
        pages.append(build_page(row))
    pages = [page for page in pages if page is not None]

    # Build collection page
    with open("./templates/collection.html") as home_template:
        home_contents = home_template.read()

    collect_t = Template(home_contents)
    collect_t = collect_t.render(title=title, description=description, pages=pages)

    outpath = Path(f"pages/{title} {collection_id}.html")
    outpath.write_text(collect_t)

    # Return collection page path,title
    return outpath, title


def build_solopage(page_block):
    """Builds a single page"""
    page = build_page(page_block)

    # Return solopage path, title
    return page


def build_space(space_id):
    """Traverses through a space and builds all collections and pages"""
    workspace = client.get_space(space_id, force_refresh=True)
    page_ids = workspace.get(force_refresh=True)["pages"]

    pages = []
    for page_id in page_ids:
        page_block = get_block(page_id)
        if page_block is None:
            continue
        if page_block.type == "page":
            pages.append(build_solopage(page_block))
        else:
            pages.append(build_collection(page_block))

    # Build main page
    with open("./templates/homepage.html") as home_template:
        home_contents = home_template.read()

    collect_t = Template(home_contents)
    collect_t = collect_t.render(pages=pages)

    outpath = Path(f"index.html")
    outpath.write_text(collect_t)


def main():
    # Clean old pages
    print("Cleaning old pages")
    pages_path = Path("pages/")
    exporter.clean_pages(pages_path)

    # Build new pages
    print("Building Space")
    space_id = environ.get("SPACE_ID")
    build_space(space_id)

    # Clean redundent zips
    print("Removing Redundent Zips")
    export_path = Path("exports/")
    exporter.clean_exports(export_path, new_exports)


if __name__ == "__main__":
    main()
