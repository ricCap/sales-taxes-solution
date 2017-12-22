
import sys  # For command line arguments
import re  # For pattern matching
import math  # For the ceil function

# General constants
BASIC_SALES_TAX = 0.10
IMPORT_DUTY = 0.05
BASIC_EXCEMPTED_GOODS = ['book', 'chocolate', 'chocolates', 'pills']

# Item pattern structure (1[one or more spaces/tabs][one item_name of one or more words][one or more spaces/tabs]at[one or more spaces/tabs][price])
# The heading number indicates the group of the matching ()
# 1. ^[ \t]*            match zero or more blank spaces and tabs at the beginning of the line
# 1. 1                  the number of items (might be modified)
# 1. [ \t]+             match one or more space and/or tabs
# 2. [ì[a-zA-Z_ ]+         match the name of the item (one or more words with uppercase, lowercase and underscores characters)
# 3. at                 match the 'at' before the price
# 3. [ \t]+             match one or more space and/or tabs
# 4. [0-9]+[\.[0-9]+]*  match

INPUT_PATTERN = re.compile(
    "(^[ \t]*1[ \t]+)([a-zA-Z_ ]+)(at[ \t]+)([0-9]+[\.[0-9]+]*)")

# The output pattern is
OUTPUT_PATTERN = '1 {item_name}: {price:.2f}\n'


def update_receipt(files: list):
    """
    Returns:
            True if success, False if failure
    """

    # For each input file
    for file in files:

        # Try to open the file
        try:
            with open(file) as input:
                with open('output_' + file, 'w+') as out:

                    print('Parsing file' + file)

                    total_sales_taxes = 0.
                    total_price = 0.

                    for line in input:
                        item = INPUT_PATTERN.search(line)

                        if item == None:
                            out.print('Unrecognized item; skipping!')
                        else:
                            # Get item name and remove trailing spaces
                            item_name = str(item.group(2)).strip()
                            item_price = float(item.group(4))

                            # Compute new price for item
                            updated_price, sales_taxes_applied = update_price(
                                item_name, item_price)

                            # Update total and total_sales_taxes
                            total_price += updated_price
                            total_sales_taxes += sales_taxes_applied

                            # Format the output line and add it to a the list of
                            # items to print
                            out.write(OUTPUT_PATTERN.format(
                                item_name=item_name, price=updated_price))

                    # Print summary
                    out.write('Sales Taxes: {:.2f}\n'.format(
                        total_sales_taxes))
                    out.write('ToTal: {:.2f}\n'.format(total_price))

        except FileNotFoundError:
            print('File ' + file + ' not found')


def update_price(item_name, item_price):
    """return 'basic' or 'exempt'"""

    import_tax = 0.
    sales_tax = 0.

    # Compute import duty
    if 'imported' in item_name.split():
        import_tax = _round(item_price * IMPORT_DUTY)

    # Comput basic sales tax if applicable
    if not is_basic_exempt(item_name):
        sales_tax = _round(item_price * BASIC_SALES_TAX)

    # Apply taxes
    updated_price = item_price + import_tax + sales_tax

    return updated_price, import_tax + sales_tax


def is_basic_exempt(item_name):
    words = item_name.split()
    for word in words:
        if word in BASIC_EXCEMPTED_GOODS:
            return True
    return False


def _round(value: float):
    """ Round to the nearest 0.05"""
    return math.ceil(value / 0.05) * 0.05

if __name__ == '__main__':
    # Get input files (usage python input1.txt input2.txt ...)
    files = sys.argv[1:]
    # Parse the file and update the receipt according to taxes
    update_receipt(files)
