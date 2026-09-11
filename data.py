"""
data.py
Central content store for the portfolio site.
Edit the values below to update the site — no HTML editing required.
"""

PROFILE = {
    "name": "Abanum Emmanuel Ovie",
    "role": "Data Science & Full-Stack Development",
    "email": "emmanuelovieabanum@gmail.com",
    "github": "https://github.com/EmmanuelAbanum",
    "github_handle": "github.com/EmmanuelAbanum",
    "bio": (
        "I'm a reliable and detail-oriented IT professional with experience in "
        "Python, SQL, web development, data handling, and technical support. "
        "I enjoy solving problems, organizing information, and building practical "
        "solutions. I'm committed to delivering accurate, high-quality work, "
        "communicating clearly, and meeting deadlines."
    ),
    "query": "SELECT * FROM specialists WHERE name = 'Emmanuel' AND availability = 'OPEN';",
}

# Rendered as a schema table — field / type / description.
# This mirrors how Emmanuel would actually document a database table,
# which is the point: the skills section IS a small piece of his own work.
SKILLS_SCHEMA = [
    {
        "field": "python_development",
        "type": "core",
        "description": "Scripting, OOP, automation, and application logic.",
    },
    {
        "field": "web_development",
        "type": "core",
        "description": "Flask, HTML, CSS, Bootstrap — building and shipping full sites.",
    },
    {
        "field": "bootstrap_ui",
        "type": "core",
        "description": "Responsive, mobile-ready layouts built quickly with Bootstrap's grid and components.",
    },
    {
        "field": "sql_database_mgmt",
        "type": "core",
        "description": "MySQL schema design, queries, and data integrity.",
    },
    {
        "field": "data_analysis",
        "type": "applied",
        "description": "Cleaning, structuring, and drawing conclusions from raw data.",
    },
    {
        "field": "web_scraping_automation",
        "type": "applied",
        "description": "BeautifulSoup & Selenium for data collection and repetitive tasks.",
    },
    {
        "field": "it_support_networking",
        "type": "foundation",
        "description": "Troubleshooting, systems support, and network fundamentals.",
    },
]

# Rendered as structured "records" rather than generic cards.
PROJECTS = [
    {
        "id": "snake_ladder_oop",
        "title": "Snake & Ladder Game",
        "type": "Python / OOP",
        "status": "Complete",
        "summary": (
            "A fully object-oriented recreation of the classic Snake & Ladder game, "
            "built to demonstrate clean class design — separate objects for the board, "
            "players, dice, and game rules — instead of one long procedural script."
        ),
        "stack": ["Python", "OOP"],
        "github": "https://github.com/EmmanuelAbanum/SNAKE_AND_LADDER_EMMANUEL_VERSION",
    },
    {
        "id": "us_states_game",
        "title": "U.S. States Data & Geography Game",
        "type": "Python / Data",
        "status": "Complete",
        "summary": (
            "An interactive quiz game that tests knowledge of U.S. state geography, "
            "backed by a structured dataset of state positions and names — a small "
            "example of turning raw reference data into something people can interact with."
        ),
        "stack": ["Python", "Pandas", "Turtle/GUI"],
        "github": "https://github.com/EmmanuelAbanum/US_STATES_GAME",
    },
    {
        "id": "business_contact_system",
        "title": "Business Website & Contact Management System",
        "type": "Flask / Full-Stack",
        "status": "Complete",
        "summary": (
            "A professional business website with a working contact management system "
            "behind it — form submissions are validated, stored, and retrievable, "
            "built end-to-end with Flask, HTML, CSS, and Bootstrap."
        ),
        "stack": ["Flask", "HTML", "CSS", "Bootstrap", "SQL"],
    },
]

NAV_LINKS = [
    {"label": "Overview", "href": "#overview"},
    {"label": "Skills", "href": "#skills"},
    {"label": "Projects", "href": "#projects"},
    {"label": "Contact", "href": "#contact"},
]
