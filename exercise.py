def pitch_contract(messages):
    add_orders = {}
    executed_volume = {}

    for message in messages:
        # The S is not part of the specification.
        if message[0] == 'S':
            message = message[1:]

        # First 8 should be the timestamp across message types.
        message_type = message[8]

        # 'A' indicates Add Order
        if message_type == 'A':
            order_id = message[9:21]
            shares = message[22:28]
            stock_symbol = message[28:34].replace(' ', '')

            add_orders[order_id] = {'shares': int(shares), 'stock_symbol': stock_symbol}

        # 'E' indicates Execute Order
        if message_type == 'E':
            order_id = message[9:21]
            executed_shares = int(message[21:27])

            order_data = add_orders[order_id]

            shares = order_data['shares']
            stock_symbol = order_data['stock_symbol']

            if stock_symbol not in executed_volume:
                if executed_shares <= shares:
                    executed_volume[stock_symbol] = executed_shares
                    order_data['shares'] -= executed_shares
            else:
                if executed_shares <= shares:
                    executed_volume[stock_symbol] += executed_shares
                    order_data['shares'] -= executed_shares

    return executed_volume


def top_performers(executed_volume, data_size):
    import operator
    data_size = int(data_size)

    volume = sorted(executed_volume.items(),
                key=operator.itemgetter(1),
                reverse=True)

    return tuple(volume[:data_size])


def extract_data(count=10, file_to_read="pitch_example_data"):
    with open(file_to_read, 'r') as line:
        executed_volume = pitch_contract(line)

    top_symbols = top_performers(executed_volume, count)

    for symbol, value in top_symbols:
        print(symbol, value)


def main(arguments):
    options = {
        "extract_data": extract_data,
    }

    try:
        if len(arguments) == 4:
            options[arguments[1]](arguments[2], arguments[3])
        else:
            print("Using default values.")
            options[arguments[1]]()
    except IndexError:
        print("Provide a valid exercise function name.")
        print("Current choices: extract_data")
    except KeyError as key_name:
        print("Unable to execute exercise function:", key_name)


if __name__ == '__main__':
    import sys

    if sys.version_info < (3, 0):
        print("This exercise requires Python 3.")
        sys.exit(1)

    main(sys.argv)
