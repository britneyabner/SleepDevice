import argparse
import device


def run():
    parser = argparse.ArgumentParser(
        prog='SleepDevice',
        description='Device for tracking sleep',
    )

    parser.add_argument('-i', '--id',
                        type=int)

    parser.add_argument('-r', '--record',
                        action="store_true")

    parser.add_argument('-s', '--score',
                        action="store_true")

    parser.add_argument('-d', '--date',
                        type=str)

    parser.add_argument('-t', '--time',
                        type=int)

    args = parser.parse_args()

    if args.record:
        id = args.id
        time = args.time
        device.record_data(id, time)
    if args.score:
        id = args.id
        date = args.date
        device.get_score(id, date)


if __name__ == "__main__":
    run()
