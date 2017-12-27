import sys  # For command line arguments
import re   # For pattern matching
import math  # For the ceil function


class PriceUpdater():
    """A class that can apply taxes to your stock receipts

    Note:
        Input format: items should be formatted as follows.
            + 1[st+][one item_name of one or more words][st+]at[st+][price]


        Legend:
            + st+: one or more spaces/tabs
            + price: a real number

        Examples of valid items:
            + 1 book   at 15
            + 1 nice book          at 15.15
            + 1 imported thing at 13

        Note: Imported items should include 'imported' in the item_name.


    """

    #####################
    # GENERAL CONSTANTS #
    #####################

    BASIC_SALES_TAX = 0.10
    IMPORT_DUTY = 0.05
    BASIC_EXCEMPTED_GOODS = ['book', 'chocolate', 'chocolates', 'pills']

    # The heading number indicates the group of the matching ()
    # 1. ^[ \t]*            match zero or more blank spaces and tabs *
    # 1. 1                  the number of items (might be modified)
    # 1. [ \t]+             match one or more space and/or tabs
    # 2. [ì[a-zA-Z_ ]+      match the name of the item **
    # 3. at                 match the 'at' before the price
    # 3. [ \t]+             match one or more space and/or tabs
    # 4. [0-9]+[\.[0-9]+]*  match

    # *  at the beginning of the line
    # ** one or more words with uppercase, lowercase and underscore characters

    _INPUT_PATTERN = re.compile(
        "(^[ \t]*1[ \t]+)([a-zA-Z_ ]+)(at[ \t]+)([0-9]+[\.[0-9]+]*)")

    # Define the format of the output items
    _OUTPUT_PATTERN = '1 {item_name}: {price:.2f}\n'

    #################
    # CLASS METHODS #
    #################

    def update_receipts(self, files: list):
        """Update the prices of the items contained in each file (.txt).

        The results are printed into a file called output-[nameOfTheInputFile]

        Args:
            fiels (list): a list of file names or paths with .txt extension

        Note:
            + If the file is not found a message is printed to the console.
            + Not recognized items will be signaled in the output file.

        Raises:
            Exceptions may be raised due to read/write permissions. Make sure
            the script can write and create files in this folder.
        """

        # For each input file
        for file in files:

            # Accept .txt files only
            if not file.endswith('.txt'):
                print('Only .txt files accepted: ' + file)
                continue

            # Try to open the file
            try:
                with open(file) as input_file:
                    with open('output-' + file, 'w+') as out:

                        # TODO we may add a logger for these information
                        print('Parsing file' + file)

                        total_sales_taxes = 0.
                        total_price = 0.

                        # Get the next item
                        for line in input_file:

                            # Parse it
                            item = self._INPUT_PATTERN.search(line)

                            if item is None:
                                out.print('Unrecognized item; skipping!\n')
                            else:
                                # Get item name and price;
                                # remove trailing spaces
                                item_name = str(item.group(2)).strip()
                                item_price = float(item.group(4))

                                # Compute new price for item
                                updated_price, sales_taxes_applied = self._update_price(
                                    item_name, item_price)

                                # Update total_price and total_sales_taxes
                                total_price += updated_price
                                total_sales_taxes += sales_taxes_applied

                                # Print the formatted updated item
                                out.write(
                                    self._OUTPUT_PATTERN.format(
                                        item_name=item_name,
                                        price=updated_price))

                        # Print summary
                        out.write('Sales Taxes: {:.2f}\n'.format(
                            total_sales_taxes))
                        out.write('Total: {:.2f}\n'.format(total_price))

            except FileNotFoundError:
                print('File ' + file + ' not found')

    def _update_price(self, item_name, item_price):
        """Update the item price according to the item category

        Args:
            item_name (str): the name of the item;
            item_price (float): the stock price of the item.

        Returns:
            float, float: the updated price and the taxes charged
        """

        # TODO might change to a single variable (taxes_charged)
        import_tax = 0.
        sales_tax = 0.

        # Compute import duty
        if 'imported' in item_name.split():
            import_tax = self._round(item_price * self.IMPORT_DUTY)

        # Compute basic sales tax if applicable
        if not self._is_basic_exempt(item_name):
            sales_tax = self._round(item_price * self.BASIC_SALES_TAX)

        # Apply taxes
        updated_price = item_price + import_tax + sales_tax

        return updated_price, import_tax + sales_tax

    def _is_basic_exempt(self, item_name: str):
        """Check if the item is exempt from basic sales taxes

        Note:
            This method is very simple: it matches whole words agains a list of
            known items; more robust implementations can be provided using e.g.
            string similarity algorithms along with a database or some
            previously trained supervised machine learning algorithms.

        Returns:
            True if exempt, False if not.
        """
        words = item_name.split()
        for word in words:
            if word in self.BASIC_EXCEMPTED_GOODS:
                return True
        return False

    def _round(self, value: float):
        """ Round up a value to the nearest 0.05"""
        return math.ceil(value / 0.05) * 0.05


if __name__ == '__main__':
    # Get input files (usage python input1.txt input2.txt ...)
    files = sys.argv[1:]
    # Instantiate a PriceUpdater
    price_updater = PriceUpdater()
    # Parse the file and update the receipt according to taxes
    price_updater.update_receipts(files)
