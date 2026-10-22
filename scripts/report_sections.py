"""
report_sections.py
Implements builder functions for each chapter of the BCSE355L Final Project Report.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_data import (
    PROJECT_METADATA,
    PAPERS_DATA,
    NOVELTY_DATA,
    DATASET_ATTRIBUTES,
    AWS_SERVICES_DATA,
    TOOLS_DATA,
    MODULES_DATA,
    TEST_CASES_DATA,
    RISKS_DATA,
    TEAM_CONTRIBUTION_DATA,
    TIMELINE_DATA,
    CHECKLIST_ITEMS
)

print("report_sections.py loading...")
