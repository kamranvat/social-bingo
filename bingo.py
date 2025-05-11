### python script that pulls header, title, entries form a .json file.
# it then makes bingo sheets: a dict of header: header, title: title, entries: 2d grid of entries
# it then generates pdf bingo sheets from the dict (N tables per a4 page)

import json
import random


# pull the json file
def load_json(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


# create bingo sheet
def create_sheet(data, size=4):
    """Create a bingo sheet from the data.
        The data should be a dict with the following keys:
        - title: the title of the bingo sheet
        - header: the header of the bingo sheet
    - entries: a list of entries to fill the bingo sheet with

        Args:
            data (dict): dict generated from the json file
            bingo sheet
            size (int, optional): Side length of bingo square. Defaults to 4.

        Returns:
            dict: A dict with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - entries: a 2d list of entries to fill the bingo sheet with
    """
    title = data["title"]
    header = data["header"]
    entries = data["entries"]

    # pull entries
    amount = size * size
    random.shuffle(entries)
    entries = entries[:amount]

    # create bingo sheet
    sheet = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(entries[i * size + j])
        sheet.append(row)

    return {"header": header, "title": title, "entries": sheet}
