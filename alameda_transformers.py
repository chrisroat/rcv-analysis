import re

TRANSFORMERS = [
    (
        re.compile(r"^President and Vice President$"),
        ("Country", "US", "President and Vice President", None),
    ),
    (
        re.compile(
            r"^U.S. Representative, (\d+)(?:st|nd|rd|th) Congressional District$"
        ),
        ("State", "CA", "Representative", 1),
    ),
    (
        re.compile(r"^State Assembly, (\d+)(?:st|nd|rd|th) District$"),
        ("State", "CA", "Lower House", 1),
    ),
    (
        re.compile(r"^State Senator, (\d+)(?:st|nd|rd|th) District$"),
        ("State", "CA", "Upper House", 1),
    ),
    (
        re.compile(r"^Superior Court Judge, Office #(\d+)$"),
        ("County", "Alameda", "Judge - Superior Court", 1),
    ),
    (
        re.compile(r"^(.*) CCD Trustees?, Area (\d+)$"),
        ("Community College District", 1, "Governing Board", 2),
    ),
    (
        re.compile(
            r"^(.*) USD Governing Board Members?(?:, Area (\d+))?(?:, (?:Full|Short) Term)?$"
        ),
        ("School District", 1, "Governing Board", 2),
    ),
    (
        re.compile(r"^Members, Board of Education - (.*)$"),
        ("School District", 1, "Governing Board", None),
    ),
    (
        re.compile(r"^Supervisor, (\d+)(?:st|nd|rd|th) District$"),
        ("County", "Alameda", "Supervisor", 1),
    ),
    (
        re.compile(r"^(Auditor|Treasurer|Mayor|City Attorney) - (.*?)(?: \(RCV\))?$"),
        ("City", 2, 1, None),
    ),
    (
        re.compile(
            r"^Members?, City Council(?:, (?:At-Large|Dist\. (\d+)))? - (.*?)(?: \(RCV\))?$"
        ),
        ("City", 2, "Council", 1),
    ),
    (
        re.compile(r"^Rent Stabilization Board Commissioners - Berkeley$"),
        ("City", "Berkeley", "Rent Stabilization Board", None),
    ),
    (
        re.compile(r"^School Directors?(?:, Dist\. (\d+))? - (.*)(?: \(RCV\))?$"),
        ("School District", 2, "Governing Board", 1),
    ),
    (
        re.compile(r"^(.*) District Directors?(?:, (?:At-Large|Ward (\d+)))?$"),
        ("Special", 1, "Director", 2),
    ),
    (
        re.compile(r"^Members, Board of Directors, (.*) District$"),
        ("Special", 1, "Director", None),
    ),
    (
        re.compile(r"^BART Director, District (\d+)$"),
        ("Special", "SF Bay Area", "BART Director", 1),
    ),
    (re.compile(r"^(?:State )?(Proposition) (\d+)"), ("State", "CA", 1, 2)),
    (re.compile(r"^(Measure) ([A-Z]+) - Alameda County$"), ("County", "Alameda", 1, 2)),
    (
        re.compile(r"^(Bond Measure) ([A-Z]+) - Alameda County Fire Dept.$"),
        ("County", "Alameda", 1, 2),
    ),
    (
        re.compile(r"^(Bond Measure) ([A-Z]+) - Oakland USD$"),
        ("City", "Oakland", 1, 2),
    ),
    (
        re.compile(r"^((Bond )?Measure) ([A-Z0-9]+) - City of (.*)$"),
        ("City", 3, 1, 2),
    ),
    (
        re.compile(r"^((?:Bond )?Measure) ([A-Z]+) - (.*) Dist\.$"),
        ("Special", 3, 1, 2),
    ),
]
