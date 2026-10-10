#!/usr/bin/env python3
"""flatratemath - compare project bids, staff hires, and flat subscriptions.

Three ways to get the same software built all look different on paper: a
fixed-bid contractor quotes one number, an employee shows up as a monthly
salary, and a flat subscription quotes a smaller monthly fee for unlimited
requests. This script converts all three to one scale, total cost per
delivered request, using the scope you actually expect to ship.

Usage:
    python3 flatratemath.py BID MONTHS REQUESTS
    python3 flatratemath.py --salary MONTHLY MONTHS REQUESTS
    python3 flatratemath.py --flat FEE MONTHS REQUESTS
    python3 flatratemath.py --compare FILE

BID     one-time fixed price for the whole project, in dollars
MONTHLY full monthly cost of a hire (salary plus taxes and benefits)
FEE     flat monthly subscription price
MONTHS  how long the work has to stay alive
REQUESTS how many discrete work items you expect to submit

--salary and --flat may be combined; plain BID form may not be. Rates are
printed as dollars per request, plus total cost of ownership per lane.
Use --compare with a CSV (mode,name,rate,months,requests) where mode is
bid, salary, or flat and rate is the matching dollar figure, to rank a
whole decision on one sheet. Exit code 0 always; bad rows are reported,
not fatal, in compare mode.

Examples:
    python3 flatratemath.py 84000 12 30
    python3 flatratemath.py --salary 18290 12 30 --flat 5995 12 30
    python3 flatratemath.py --compare lanes.csv
"""
import csv
import sys


def lane_costs(bid=0.0, monthly=0.0, months=1, requests=1):
    """Return (total, per_request) dollars for a lane.

    bid is one-time; monthly repeats every month for months. Either may
    be zero but not both.

    >>> lane_costs(bid=84000, months=12, requests=30)
    (84000.0, 2800.0)
    >>> lane_costs(monthly=18290, months=12, requests=30)
    (219480.0, 7316.0)
    >>> lane_costs(monthly=5995, months=12, requests=30)
    (71940.0, 2398.0)
    """
    months = max(1, int(months))
    requests = max(1, int(requests))
    total = bid + monthly * months
    return total, total / requests


def main(argv):
    lanes = []
    mode = None
    args = argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--compare":
            if i + 1 >= len(args):
                print("usage: flatratemath.py --compare FILE", file=sys.stderr)
                return 2
            with open(args[i + 1], newline="") as fh:
                for row in csv.reader(fh):
                    if not row or row[0].startswith("#"):
                        continue
                    try:
                        name, kind, rate, months, requests = (
                            row[0], row[1].strip().lower(), float(row[2]),
                            int(float(row[3])), int(float(row[4])))
                        if kind == "bid":
                            lanes.append((lane_costs(bid=rate, months=months,
                                                     requests=requests), name))
                        elif kind == "salary":
                            lanes.append((lane_costs(monthly=rate, months=months,
                                                     requests=requests), name))
                        elif kind == "flat":
                            lanes.append((lane_costs(monthly=rate, months=months,
                                                     requests=requests), name))
                        else:
                            print(f"skip {row!r}: unknown mode {kind}",
                                  file=sys.stderr)
                    except (ValueError, IndexError) as exc:
                        print(f"skip {row!r}: {exc}", file=sys.stderr)
            mode = "done"
            i += 2
            continue
        if a in ("--salary", "--flat"):
            if i + 3 > len(args):
                print(f"usage: flatratemath.py {a} RATE MONTHS REQUESTS",
                      file=sys.stderr)
                return 2
            rate, months, requests = (float(args[i + 1]), int(args[i + 2]),
                                      int(args[i + 3]))
            lanes.append((lane_costs(monthly=rate, months=months,
                                     requests=requests),
                          "hire" if a == "--salary" else "flat sub"))
            mode = "combo"
            i += 4
            continue
        if mode is None:
            if i + 3 > len(args):
                print(__doc__, file=sys.stderr)
                return 2
            bid, months, requests = (float(args[i]), int(args[i + 1]),
                                     int(args[i + 2]))
            lanes.append((lane_costs(bid=bid, months=months,
                                     requests=requests), "fixed bid"))
            mode = "bid"
            i += 3
            continue
        print(f"unexpected argument {a!r}; combine lanes with flags only",
              file=sys.stderr)
        return 2

    if not lanes:
        print(__doc__, file=sys.stderr)
        return 2
    lanes.sort(key=lambda pair: pair[0][1])
    for (total, per), name in lanes:
        print(f"{name}: ${total:,.0f} total, ${per:,.0f} per request")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
