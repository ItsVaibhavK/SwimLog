# Import functions to be tested from swimlog.py
from swimlog import valid, total_distance, total_time, average_distance, average_time


# Testing valid(n)
def test_valid():
    assert valid(1) == True
    assert valid(0) == False
    assert valid("a") == False
    assert valid(-1) == False
    assert valid(0.7) == False


# Testing total_distance(distance)
def test_total_distance():
    assert total_distance(500) == "\nTotal distance swam: 500 meters"
    assert total_distance(999) == "\nTotal distance swam: 999 meters"
    assert total_distance(1687) == "\nTotal distance swam: 1.687 kilometers"
    assert total_distance(3500) == "\nTotal distance swam: 3.5 kilometers"


# Testing total_time(duration)
def test_total_time():
    assert total_time(60) == "\nTotal time spent swimming: 1 hour(s), 0 minute(s)"
    assert total_time(44) == "\nTotal time spent swimming: 44 minutes"
    assert total_time(122) == "\nTotal time spent swimming: 2 hour(s), 2 minute(s)"
    assert total_time(12) == "\nTotal time spent swimming: 12 minutes"


# Testing average_distance(distance, sessions)
def test_average_distance():
    assert (
        average_distance(500, 1) == "\nAverage distance swam per session: 500.0 meters"
    )
    assert (
        average_distance(3600, 4) == "\nAverage distance swam per session: 900.0 meters"
    )
    assert (
        average_distance(6347, 8)
        == "\nAverage distance swam per session: 793.38 meters"
    )
    assert (
        average_distance(9521, 14)
        == "\nAverage distance swam per session: 680.07 meters"
    )


# Testing average_time(duration, sessions)
def test_average_time():
    assert (
        average_time(222, 3)
        == "\nAverage time spent swimming per session: 1 hour(s), 14 minute(s)"
    )
    assert (
        average_time(657, 6)
        == "\nAverage time spent swimming per session: 1 hour(s), 50 minute(s)"
    )
    assert (
        average_time(117, 2) == "\nAverage time spent swimming per session: 58 minutes"
    )
    assert (
        average_time(45, 1) == "\nAverage time spent swimming per session: 45 minutes"
    )


if __name__ == "__main__":
    main()
