# PITCH Data Challenge

The goal is a program that reads PITCH data from standard input.

The output of the program should be a table of the top ten symbols by their executed volume.

Example output:

    SPY  24486275
    QQQQ 15996041
    XLF  10947444
    IWM  9362518
    MSFT 8499146
    DUG  8220682
    C    6756932
    F    6679883
    EDS  6673983
    QID  6526201

The executed volume is the amount of shares executed by each symbol.

## Usage

    python exercise.py extract_10
    python exercise.py extract_10 pitch_example_minimal_data

## Implementation

I treat the PITCH data as an interface, even though I'm reading it from a file. So the `pitch_contract` method is worded such to indicate that the PITCH data coming in _is_ in fact a contract. This means contract, property, and consumer-driven contract tests could be applied to any interfaces that are relying on this data.

The `pitch_contract` takes in the messages from the PITCH source. Its operation is to provide a simple mapping of the message and the volume. A dictionary of key-value pairs seems to make sense here. The contract is encapsulated in a TextIOWrapper, which is a buffered text stream over a BufferedIOBase binary stream. This is being done to allow for less initial hurdles with reading large data sets.

The `top_performers` method takes the executed volume data and returns the top performers from it.

I created two different data sets so that I could better explore the problem space and get some diagnostics on my execution.

### Minimal Data Set

Here is how that can be executed:

    python exercise.py extract_data 1 pitch_example_minimal_data

The minimal data set is based on a single order ID (4K27GA00003G). The output of this is:

   DIA 153

The path of execution here would look like this:

    A - order_id:  4K27GA00003G
    A - shares:  000200
    A - stock:  DIA
    E - order_id:  4K27GA00003G
    E - executed_shares:  77
    E - order_data:  {'shares': 200, 'stock_symbol': 'DIA'}
    E - executed_volume:  {}
    E - executed_volume:  {'DIA': 77}

    E - order_id:  4K27GA00003G
    E - executed_shares:  76
    E - order_data:  {'shares': 123, 'stock_symbol': 'DIA'}
    E - executed_volume:  {'DIA': 77}
    E - executed_volume:  {'DIA': 153}


### Reduced Data Set

Here is how that can be executed:

    python exercise.py extract_data 1 pitch_example_reduced_data

The reduced data set is based on two orders: 4K27GA00003G and 5K27GA00000L. The output of this is:

    DIA 153

The same as the minimal data set, if you are checking for just the top performer. To see that there are actually two values and that the top is being chosen, run it like this:

    python exercise.py extract_data 2 pitch_example_reduced_data

The output would be:

    DIA 153
    FXP 20

The path of execution here would look like this:

    A - order_id:  4K27GA00003G
    A - shares:  000200
    A - stock:  DIA
    E - order_id:  4K27GA00003G
    E - Executed Shares:  77
    E - order_data:  {'shares': 200, 'stock_symbol': 'DIA'}
    E - executed_volume:  {}
    E - executed_volume:  {'DIA': 77}

    E - order_id:  4K27GA00003G
    E - Executed Shares:  76
    E - order_data:  {'shares': 123, 'stock_symbol': 'DIA'}
    E - executed_volume:  {'DIA': 77}
    E - executed_volume:  {'DIA': 153}

    A - order_id:  5K27GA00000L
    A - shares:  000100
    A - stock:  FXP
    E - order_id:  5K27GA00000L
    E - executed_shares:  20
    E - order_data:  {'shares': 100, 'stock_symbol': 'FXP'}
    E - executed_volume:  {'DIA': 153}
    E - executed_volume:  {'DIA': 153, 'FXP': 20}

### Full Data Set

Here is how that can be executed:

    python exercise.py extract_data

Here if no other data is passed in then the default values of 10 is used for the number of data points to retrieve and "pitch_example_data" is used as the data source.

The output of this is:

    DRYS 509
    FXP 320
    AAPL 295
    DIA 229
    DIG 200
    UYG 100

This is incomplete at this point. And it's not clear yet if it's accurate.

## Oracle

The oracle for the project is the PITCH specification. It is provided in PITCH_SPECIFICATION.pdf.

## Data

A portion of realistic PITCH data is provided in `pitch_example_data` file.

All data in that test data begins with an 'S' character. That character is not part of the specification because it is not part of the message. Any implementations should be designed such that the 'S' character is ignored.

## Breakdown of Data:

### Adding an Order:

See 4.3 of specification.

Consider this data point:

    28800167A4K27GA00002ZB000100DRYS  0001052600Y

This breaks down as:
    Timestamp:      28800167
    Message Type:   A
    Order ID:       4K27GA00002Z
    Side Indicator: B
    Shares:         000100
    Stock Symbol:   DRYS
    Price:          0001052600
    Display:        Y

### Canceling an Order:

See 4.4.2 of specification.

Consider this data point:

    28800168X1K27GA00000Y000100

This breaks down as:

    Timestamp:       28800168
    Message Type:    X
    Order ID:        1K27GA00000Y
    Canceled Shares: 000100

### Executing an Order:

See 4.4.1 of specification.

Consider this data point:

    28803224E4K27GA00003G00007600004AQ00002

This breaks down as:

    Timestamp:       28803224
    Message Type:    E
    Order ID:        4K27GA00003G
    Executed Shares: 000076
    Execution ID:    00004AQ00002

## Caveat

Note that this exercise does very little to show how a tester should be thinking about these things. This is very much a developer-focused exercise.

From a test and quality assurance perspective, it's important to understand how someone conceptualizes testing, how they would treat data, whether they consider incidentals as part of test data, the amount of tests they would apply to a given situation (too many? too few?), and so on.

There was no expected output provided. As such it was not possible for someone to determine if their implementation worked. This, again, is something that should be provided. When testing applications we generally do have an oracle of what we expect to find in a given situation. If we do not, part of what testers do is ask for one.

I've helped companies learn how to adapt their practices to hiring technical testers. By this I mean "testers who can do some development" (in a test solution context) rather than "developers who can test." Feel free to check out some of these articles:

* http://testerstories.com/2017/10/technical-test-interviews-are-broken/
* http://testerstories.com/2014/12/interview-testers-as-if-you-want-testers/
* http://testerstories.com/2014/06/interview-technical-testers-for-broad-skills/
