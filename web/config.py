# -*- coding: utf-8 -*-

all_stops = (
    ('mit', "", (
        # tech shuttle tracking is broken: tech|wcamp|mass84
        ("Boston Daytime", "boston|boston|mass84_d", ),
        ("Northwest Shuttle", "northwest|nwcamp|mass77", ),
        ("Boston East", "saferidebostone|boston|mass84_d", ),
        ("Boston West", "saferidebostonw|boston|mass84_d", ),
        ("Boston All\n(→ West)", "saferidebostonall|boston|mass84", ),
        ("Cambridge East", "saferidecambeast|frcamp|mass84_d", ),
        ("Cambridge West", "saferidecambwest|frcamp|mass84_d", ),
        ("Cambridge All\n(→ West)", "saferidecamball|frcamp|mass84_d", ),
    ), ),
    ('mbta', "MBTA ", (
        ("MBTA 1 (→ Cambridge)", "1|1_0_var0|97", ),
        ("MBTA 1 (→ Boston)", "1|1_1_var0|75", ),
    ), ),
)

hubway_stations = (
    (67, "MIT (Bexley)", ), #MIT at Mass Ave / Amherst St
)

