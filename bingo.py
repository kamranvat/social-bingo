import json
import random
import numpy as np
from fpdf import FPDF, XPos, YPos


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
    - statements: a list of statements to fill the bingo sheet with

    Args:
        data (dict): dict for the bingo sheet
        size (int, optional): Side length of bingo square. Defaults to 4.

    Returns:
        dict: A dict with the following keys:
        - title: the title of the bingo sheet
        - header: the header of the bingo sheet
        - statements: a 2d list of statements to fill the bingo sheet with
    """
    title = data["title"]
    header = data["header"]
    statements = data["statements"]

    # pull statements
    amount = size * size
    if len(statements) < amount:
        raise ValueError(
            f"Not enough statements to fill the bingo sheet. Need {amount} but only have {len(statements)}"
        )
    random.shuffle(statements)
    statements = statements[:amount]

    # create bingo sheet
    sheet = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(statements[i * size + j])
        sheet.append(row)

    return {"header": header, "title": title, "statements": sheet}


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
            - statements: a 2d list of statements to fill the bingo sheet with
    """
    sheets = []
    for i in range(amount):
        sheets.append(create_sheet(data, size))
    return sheets


def check_uniqueness(sheets):
    """Check if the bingo sheets are unique. Warning: expensive.

    Args:
        sheets (list): list of dicts with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - statements: a 2d list of statements to fill the bingo sheet with

    Returns:
        bool: True if all sheets are unique, False otherwise
    """
    if len(sheets) < 2:
        return True

    statements = []
    for sheet in sheets:
        # flatten the statements, keeping the order
        flat_statements = [
            statement for row in sheet["statements"] for statement in row
        ]
        statements.append(flat_statements)
    # check if all statements are unique
    for i in range(len(statements)):
        for j in range(i + 1, len(statements)):
            if statements[i] == statements[j]:
                print(f"Duplicate sheets found: {i} and {j}")
                return False

    return True


def create_pdf(sheets, filename="bingo.pdf"):
    """Create a pdf from the bingo sheets.

    Args:
        sheets (list): list of dicts with the following keys:
            - title: the title of the bingo sheet
            - header: the header of the bingo sheet
            - statements: a 2d list of statements to fill the bingo sheet with
        filename (str, optional): name of the pdf file. Defaults to "bingo.pdf".
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # title, header, and statements size
    title_font_size = 10
    header_font_size = 8
    statement_font_size = 6

    # set font
    font = "Helvetica"

    # set grid and cell sizes
    grid_size = np.sqrt(len(sheets[0]["statements"]))
    grid_size = int(grid_size)
    cell_width = 95 / grid_size
    cell_height = 40 / grid_size

    title_height = 0
    header_height = 0
    grid_height = grid_size * cell_height + 10
    print(grid_height)
    # set margins
    pdf.set_margins(10, 10, 10)

    # loop through sheets
    for i, sheet in enumerate(sheets):
        pdf.set_font(font, "B", title_font_size)
        pdf.cell(
            200, 10, text=sheet["title"], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C"
        )
        if i == 0:
            title_height = pdf.get_y()

        # add header
        pdf.set_font(font, "I", header_font_size)
        pdf.multi_cell(
            200,
            10,
            text=sheet["header"],
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align="C",
            max_line_height=pdf.font_size,
        )
        if i == 0:
            header_height = pdf.get_y()

        # create grid
        pdf.set_font(font, size=statement_font_size)
        for row in sheet["statements"]:
            for statement in row:
                # place text in cell, ensure that if the text is too long, the line breaks
                pdf.multi_cell(
                    cell_width,
                    cell_height,
                    text=statement,
                    border=1,
                    align="C",
                    max_line_height=pdf.font_size,
                    # new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                )

            pdf.ln()

        if i == 0:
            grid_height = pdf.get_y()
            print(grid_height)

        # print(title_height, header_height)
        # pdf.ln(title_height + header_height)

        pdf.set_y(title_height + header_height + grid_height + 5)

        # add page break
        if (i + 1) % 2 == 0:
            pdf.add_page()

    pdf.output(filename)


def main():
    data = load_json("entries.json")
    max_tries = 10  # max tries to generate unique sheets.
    size = 4  # default size of bingo sheet
    filename = "sheets.pdf"  # default filename

    while True:
        # get amount from user
        try:
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
    create_pdf(sheets, filename=filename)
    print(f"Bingo sheets saved to {filename}")


if __name__ == "__main__":
    main()
