import os


def convert(file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    the_file = os.path.join(dir_path, file)

    tickers = []

    with open(the_file) as f:

        for line in f:
            # import code
            # code.interact(local=dict(globals(), **locals()))
            line = line.split(",")
            ticker = line[0].rstrip()
            tickers.append(ticker)
        # lines = [line.rstrip() for line in f]
    print(tickers)


convert("tockers.csv")
