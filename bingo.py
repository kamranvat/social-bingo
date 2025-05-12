### python script that pulls header, title, entries form a .json file.
# it then makes bingo sheets: a dict of header: header, title: title, entries: 2d grid of entries
# it then generates pdf bingo sheets from the dict (N tables per a4 page)
import json
import random
import numpy as np
from fpdf import FPDF
import pandas as pd


def load_json(json_file):
    """Load a json file and return the data as a dict."""
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def create_sheet(data, size=4):
    """Create a bingo sheet from the data.
    The data should be a dict with the following keys:
    - title: the title of the bingo sheet
    - header: the header of the bingo sheet
    - entries: a list of entries to fill the bingo sheet with

    Args:
        data (dict): dict for the bingo sheet
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
    if len(entries) < amount:
        raise ValueError(
            f"Not enough entries to fill the bingo sheet. Need {amount} but only have {len(entries)}"
        )
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


def create_sheets(data, size=4, amount=1):
    """Create multiple bingo sheets from the data.

    Args:
        data (dict): dict generated from the json file
        size (int, optional): Side length of bingo square. Defaults to 4.
        amount (int, optional): Number of bingo sheets to create. Defaults to 1.

    Returns:
        list: A list of dicts with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - entries: a 2d list of entries to fill the bingo sheet with
    """
    sheets = []
    for i in range(amount):
        sheets.append(create_sheet(data, size))
    return sheets


def check_uniqueness(sheets):
    """Check if the bingo sheets are unique.

    Args:
        sheets (list): list of dicts with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - entries: a 2d list of entries to fill the bingo sheet with

    Returns:
        bool: True if all sheets are unique, False otherwise
    """
    entries = []
    for sheet in sheets:
        entries += [entry for row in sheet["entries"] for entry in row]
    return len(entries) == len(set(entries))


def create_pdf(sheets, filename="bingo.pdf"):
    """Create a pdf from the bingo sheets.

    Args:
        sheets (list): list of dicts with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - entries: a 2d list of entries to fill the bingo sheet with
        filename (str, optional): name of the pdf file. Defaults to "bingo.pdf".
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # set font
    pdf.set_font("Arial", size=12)

    # loop through sheets
    for i, sheet in enumerate(sheets):
        # add title
        pdf.cell(200, 10, txt=sheet["title"], ln=True, align="C")
        # add header
        pdf.cell(200, 10, txt=sheet["header"], ln=True, align="C")
        # add entries
        for row in sheet["entries"]:
            pdf.cell(200, 10, txt=" | ".join(row), ln=True, align="C")
        # add page break
        if (i + 1) % 2 == 0:
            pdf.add_page()

    pdf.output(filename)


def main():
    # load json file
    data = load_json("bingo.json")
    max_tries = 10  # max tries to generate unique sheets.

    while True:
        # get size and amount from user
        try:
            size = int(input("Enter the size of the bingo sheet (default 4): ") or 4)
            amount = int(
                input("Enter the number of bingo sheets to create (default 1): ") or 1
            )
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # create bingo sheets until the generated sheets are unique
    for _ in range(max_tries):
        sheets = create_sheets(data, size, amount)
        if check_uniqueness(sheets):
            break
        else:
            print("Bingo sheets are not unique. Generating again...")

        if _ == max_tries - 1:
            print(
                "Failed to generate",
                amount,
                "unique bingo sheets after",
                max_tries,
                "attempts. Saving last attempt.",
            )
            return

    # create pdf
    create_pdf(sheets, filename="bingo.pdf")


if __name__ == "__main__":
    main()
