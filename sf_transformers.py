import re

TRANSFORMERS = [
    (
        re.compile(r"^(PRESIDENT AND VICE PRESIDENT)$"),
        ("Country", "US", "President and Vice President", None),
    ),
    (
        re.compile(r"^US House of Rep District (\d+)$"),
        ("State", "CA", "Representative", 1),
    ),
    (
        re.compile(r"^STATE ASSEMBLY MEMBER District (\d+)$"),
        ("State", "CA", "Lower House", 1),
    ),
    (
        re.compile(r"^State Senator District (\d+)$"),
        ("State", "CA", "Upper House", 1),
    ),
    (
        re.compile(r"^BOARD OF EDUCATION$"),
        ("School District", "San Francisco", "Governing Board", None),
    ),
    (
        re.compile(r"^COMMUNITY COLLEGE BOARD$"),
        ("Community College District", "San Francisco", "Governing Board", None),
    ),
    (
        re.compile(r"^BART DIRECTOR DISTRICT (\d+)$"),
        ("Special", "SF Bay Area", "BART Director", 1),
    ),
    (
        re.compile(r"^BOARD OF SUPERVISORS DISTRICT (\d+)$"),
        ("City", "San Francisco", "Board of Supervisors", 1),
    ),
    (
        re.compile(r"^(Proposition) (\d+)$"),
        ("State", "CA", 1, 2),
    ),
    (
        re.compile(r"^(Proposition) ([A-Z]+)$"),
        ("City", "San Francisco", 1, 2),
    ),
]
