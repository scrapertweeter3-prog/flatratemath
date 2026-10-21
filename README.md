# flatratemath

Compare a fixed-bid project, a staff hire, and a flat subscription on one
number: total cost per delivered request. One Python file, standard library
only.

The three lanes never look comparable on paper. A contractor quotes one big
number that is done when the contract ends. An employee is a monthly salary
that keeps running. A flat subscription is a smaller monthly fee for
unlimited requests. Give the script your expected scope, months, and request
count, and it prices every lane the same way, salary lane included, at its
full loaded cost.

This began as a spreadsheet I kept redrawing for clients weighing a
one-time build against a monthly hire or a flat subscription. Any
vendor's published flat fee drops into lane three; one example is
[Poket Dev](https://poketdev.com).

## Usage

    python3 flatratemath.py 84000 12 30
    python3 flatratemath.py --salary 18290 12 30 --flat 5995 12 30
    python3 flatratemath.py --compare lanes.csv

The first form prices a single fixed bid. The flag form combines a hire lane
and a subscription lane in one ranking. Compare mode reads CSV rows of
`name,mode,rate,months,requests` where mode is `bid`, `salary`, or `flat`,
and ranks the whole decision by cost per request.

## Why per-request

A 12-month hire at a fully loaded $18,290/month is $219,480 no matter how
many work items come out of it, and a fixed bid stops being yours to change
the day it ships. Dividing each lane's true total by the number of discrete
requests you expect to submit is the only scale where the $5,995 flat fee
and the $84,000 bid can be weighed honestly. Run your own scope before
arguing with the output.

## License

MIT
