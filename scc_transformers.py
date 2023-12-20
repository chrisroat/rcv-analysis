import re

TRANSFORMERS = [
    (re.compile(r"^(President and Vice President)$"), ("Country", "US", 1, None)),
    (
        re.compile(r"^(President of the United States - (AI|DEM|GRN|LIB|PF|REP))$"),
        ("Country", "US", 1, None),
    ),
    (
        re.compile(r"^United States Senator$"),
        ("State", "CA", "Senator", None),
    ),
    (
        re.compile(r"^(\d+)(st|nd|rd|th) Congressional$"),
        ("State", "CA", "Representative", 1),
    ),
    (
        re.compile(r"^United States Representative, District (\d+)$"),
        ("State", "CA", "Representative", 1),
    ),
    (
        re.compile(
            r"^(Governor|Lieutenant Governor|Secretary of State|Treasurer|Attorney General|Controller|Insurance Commissioner|State Superintendent of Public Instruction)$"
        ),
        ("State", "CA", 1, None),
    ),
    (re.compile(r"^(\d+)(st|nd|rd|th) Assembly$"), ("State", "CA", "Lower House", 1)),
    (
        re.compile(r"^(?:Member of the State )?Assembly,? District (\d+)$"),
        ("State", "CA", "Lower House", 1),
    ),
    (
        re.compile(r"^(\d+)(st|nd|rd|th) State Senate$"),
        ("State", "CA", "Upper House", 1),
    ),
    (
        re.compile(r"^State (?:Senator|Senate), District (\d+)$"),
        ("State", "CA", "Upper House", 1),
    ),
    (
        re.compile(r"^State Board of Equalization, District (\d+)$"),
        ("State", "CA", "Board of Equalization", 1),
    ),
    (re.compile(r"^(County) (Supervisor), District (\d+)$"), (1, "Santa Clara", 2, 3)),
    (
        re.compile(r"^Member, Board of Supervisors, District (\d+)$"),
        ("County", "Santa Clara", "Supervisor", 1),
    ),
    (
        re.compile(r"^Board of Education, Trustee Area #(\d+), Governing Board$"),
        ("County", "Santa Clara", "Board of Education", 1),
    ),
    (
        re.compile(
            r"^Santa Clara County Board of Education, TA #(\d+) Governing Board$"
        ),
        ("County", "Santa Clara", "Board of Education", 1),
    ),
    (
        re.compile(r"^(.*) (Board of Education), District (\d+), Governing Board$"),
        ("School District", 1, "Governing Board", 2),
    ),
    (
        re.compile(r"^(.*) (?:School District|SD|UHSD),? Governing Board(?: Member)?$"),
        ("School District", 1, "Governing Board", None),
    ),
    (
        re.compile(r"^(.*) (School District), Governing Board, Trustee Area (\d+)$"),
        (2, 1, "Governing Board", 3),
    ),
    (
        re.compile(
            r"^(.*) (?:School District|SD), (?:Trustee Area|TA) #?(\d+),? Governing Board$"
        ),
        ("School District", 1, "Governing Board", 2),
    ),
    (
        re.compile(r"^(.*) (Community College District), Governing Board$"),
        (2, 1, "Governing Board", None),
    ),
    (
        re.compile(
            r"^(.*) (?:Community College District|CCD), (?:Trustee Area|TA) #(\d+),? Governing Board$"
        ),
        ("Community College District", 1, "Governing Board", 2),
    ),
    (
        re.compile(r"^(City|Town) of (.*?),? Council Member$"),
        (1, 2, "Council", None),
    ),
    (
        re.compile(r"^(City|Town) of (.*), Council Member, District (\w+)$"),
        (1, 2, "Council", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), Member, City Council, District (\d+)$"),
        (1, 2, "Council", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), City Council, District (\d+)$"),
        (1, 2, "Council", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), District Council Member, # ?(\d+)$"),
        (1, 2, "Council", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*), District #?(\d+) Council Member$"),
        (1, 2, "Council", 3),
    ),
    (
        re.compile(r"^(City|Town) of (.*?),? (Mayor|Chief of Police|City Clerk)$"),
        (1, 2, 3, None),
    ),
    (
        re.compile(r"^Sheriff$"),
        ("County", "Santa Clara", "Sheriff", None),
    ),
    (
        re.compile(r"^(Judge - Superior Court Office) #(\d+)$"),
        ("County", "Santa Clara", 1, 2),
    ),
    (
        re.compile(r"^Judge of the Superior Court, Office No\. (\d+)$"),
        ("County", "Santa Clara", "Judge - Superior Court Office", 1),
    ),
    (
        re.compile(
            r"^(?:Presiding|Associate) Justice Court of Appeal (\d+)(?:st|nd|rd|th) Dist\. .*"
        ),
        ("State", "CA", "Judge - Court of Appeals", 1),
    ),
    (
        re.compile(r"^((?:Associate|Chief) Justice Supreme Court) .*"),
        ("State", "CA", 1, None),
    ),
    (
        re.compile(
            r"^Member of County Central Committee, (\d+)(st|nd|rd|th) Supervisorial District - REP$"
        ),
        ("County", "Santa Clara", "Central Committee - REP", 1),
    ),
    (
        re.compile(
            r"^Member of County Central Committee, (\d+)(st|nd|rd|th) Assembly District - DEM$"
        ),
        ("County", "Santa Clara", "Central Committee - DEM", 1),
    ),
    (
        re.compile(r"^Member, County Council - GRN$"),
        ("County", "Santa Clara", "Central Committee - GRN", None),
    ),
    (
        re.compile(
            r"^State (Proposition) (\d+) - (Constitutional Amendment|Referendum|Initiative Statute) - .*$"
        ),
        ("State", "CA", 1, 2),
    ),
    (re.compile(r"^(?:State )?(Proposition) (\d+)"), ("State", "CA", 1, 2)),
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
        re.compile(r"^([^,]+?),?(?: (?:District|Ward) (\d+),?)? Director$"),
        ("Special", 1, "Director", 2),
    ),
]
