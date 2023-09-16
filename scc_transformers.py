import re

TRANSFORMERS = [
    (re.compile(r"^(President and Vice President)$"), ("Country", "US", 1, None)),
    (
        re.compile(r"^(\d+)(st|nd|rd|th) Congressional$"),
        ("State", "CA", "Representative", 1),
    ),
    (re.compile(r"^(\d+)(st|nd|rd|th) Assembly$"), ("State", "CA", "Lower House", 1)),
    (
        re.compile(r"^(\d+)(st|nd|rd|th) State Senate$"),
        ("State", "CA", "Upper House", 1),
    ),
    (re.compile(r"^(County) (Supervisor), District (\d+)$"), (1, "Santa Clara", 2, 3)),
    (
        re.compile(r"^(Board of Education), Trustee Area #(\d+), Governing Board$"),
        ("County", "Santa Clara", 1, 2),
    ),
    (
        re.compile(r"^(.*) Board of Education, District (\d+), Governing Board$"),
        ("School District", 1, "Board Member", 2),
    ),
    (
        re.compile(r"^(.*) (School District), Governing Board$"),
        (2, 1, "Board Member", None),
    ),
    (
        re.compile(r"^(.*) (School District), Governing Board, Trustee Area (\d+)$"),
        (2, 1, "Board Member", 3),
    ),
    (
        re.compile(r"^(.*) (School District), Trustee Area #?(\d+), Governing Board$"),
        (2, 1, "Board Member", 3),
    ),
    (
        re.compile(r"^(.*) (Community College District), Governing Board$"),
        (2, 1, "Board Member", None),
    ),
    (
        re.compile(
            r"^(.*) (Community College District), Trustee Area #(\d+), Governing Board$"
        ),
        (2, 1, "Board Member", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), Council Member$"),
        (1, 2, "Council Member", None),
    ),
    (
        re.compile(r"^(City|Town) of (.*), Council Member, District (\w+)$"),
        (1, 2, "Council Member", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), Member, City Council, District (\d+)$"),
        (1, 2, "Council Member", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), District Council Member, # ?(\d+)$"),
        (1, 2, "Council Member", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), (Mayor|Chief of Police|City Clerk)$"),
        (1, 2, 3, None),
    ),
    (
        re.compile(r"^(Judge - Superior Court Office) #(\d+)$"),
        ("County", "Santa Clara", 1, 2),
    ),
    (
        re.compile(
            r"^State (Proposition) (\d+) - (Constitutional Amendment|Referendum|Initiative Statute) - .*$"
        ),
        ("State", "CA", 1, 2),
    ),
    (re.compile(r"^(Measure) ([A-Z]+) - (Town|City) of (.*), (.*)$"), (3, 4, 1, 2)),
    (re.compile(r"^(Measure) ([A-Z]+) - (.*) (School District), (.*)$"), (4, 3, 1, 2)),
    (
        re.compile(
            r"^(Measure) ([A-Z]+) - (San Jose - (.*)) (Community College District), (.*)$"
        ),
        (5, 3, 1, 2),
    ),
    (re.compile(r"^(Measure) ([A-Z]+) - ([^,]*), (.*)$"), ("Special", 3, 1, 2)),
    (
        re.compile(r"^([^,]+),( (District|Ward) (\d+),)? (Director)$"),
        ("Special", 1, 5, 4),
    ),
]
