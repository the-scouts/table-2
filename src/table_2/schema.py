from typing import Literal

import pydantic

TYPES_CATEGORY = Literal["Programme Delivery", "Line Manager", "Governance", "Support"]
TYPES_SUBCATEGORY = Literal[
    "Beaver Colony",
    "Cub Pack",
    "Scout Troop",
    "Explorer Unit",
    "UK Contingent",
    None,
    "Deputy Managers",
    "Activities",
    "Administrators",
    "Supporters",
    "Adult Training",
    "Advisers",
    "Assistant Commissioners",
    "Site Volunteers",
    "Chaplains",
    "Communications",
    "Contingents",
    "Leaders",
    "Presidents",
    "Safe Scouting",
    "SASUs",
    "Youth Commissioners",
]
TYPES_HIERARCHY = Literal["Group", "District", "Headquarters", "County", "Region (England, Wales)", "Country", "Region (England)"]
TYPES_COMPASS_CLASS = Literal[
    "Leader",
    "Commissioner",
    "Committee",
    "Secretary",
    "Manager",
    "Supporter",
    "Trainer",
    "Assessor",
    "Administrator",
    "Co-ordinator",
    "Advisor",
    "Adviser",
    " Commissioner",
    "Honorary",
]
TYPES_MEMBERSHIP = Literal["Member", "Associate Member", "None"]
TYPES_TRUSTEE = Literal[
    "Opt-in",
    "No",
    "Yes",
    "See Scottish Variations from POR",
    "As defined in Branch’s constitution",
    "No (unless a member of an Executive or Trustee Board)",
    "Yes\n(in Scotland, only if Group is OSCR registered)",
    "Yes\n(for 1 role holder)",
    None,
]
TYPES_DISCLOSURE = Literal["Yes", "No", "Yes (SV)", None]
TYPES_REVIEW = Literal["Yes", "No", "N/A", None]
TYPES_TRAINING = Literal["GS", "NA", "TO"]
TYPES_MODULE_TRUSTEE_INTRODUCTION = Literal["OP", "NA"]  # TODO ????? this doesn't seem right
TYPES_GETTING_STARTED = Literal["GS", "NA"]
TYPES_TRAINING_OBLIGATION = Literal["TO", "NA"]
TYPES_TRAINING_DEADLINE = Literal["3Y", "5M", None]


class Table2Roles(pydantic.BaseModel):
    category: list[TYPES_CATEGORY] = []
    subcategory: list[TYPES_SUBCATEGORY] = []
    hierarchy: list[TYPES_HIERARCHY] = []
    title: list[str] = []
    variants: list[str] = []
    compass_class: list[TYPES_COMPASS_CLASS] = []
    line_manager: list[str] = []
    approval_process: list[str] = []
    approver: list[str] = []
    relevant: list[str] = []
    induction: list[str] = []
    membership: list[TYPES_MEMBERSHIP] = []
    trustee: list[TYPES_TRUSTEE] = []
    disclosure: list[TYPES_DISCLOSURE] = []
    review: list[TYPES_REVIEW] = []
    location_england: list[bool] = []
    location_scotland: list[bool] = []
    location_northern_ireland: list[bool] = []
    location_wales: list[bool] = []
    location_bso: list[bool] = []
    location_branches: list[bool] = []
    location_guernsey: list[bool] = []
    location_jersey: list[bool] = []
    location_headquarters: list[bool] = []
    location_uk_contingent: list[bool] = []
    module_1: list[TYPES_TRAINING] = []
    module_trustee_introduction: list[str] = []
    module_2: list[TYPES_TRAINING] = []
    module_3: list[TYPES_GETTING_STARTED] = []
    module_4: list[TYPES_TRAINING] = []
    module_safety: list[TYPES_TRAINING] = []
    module_safeguarding: list[TYPES_TRAINING] = []
    module_gdpr: list[TYPES_TRAINING] = []
    module_section_wood_badge: list[TYPES_TRAINING_OBLIGATION] = []
    training_deadline: list[TYPES_TRAINING_DEADLINE] = []
    module_ms_wood_badge: list[TYPES_TRAINING_OBLIGATION] = []
    module_first_aid_certificate: list[TYPES_TRAINING_OBLIGATION] = []
    module_7: list[TYPES_TRAINING_OBLIGATION] = []
    module_24: list[TYPES_TRAINING_OBLIGATION] = []
    module_25: list[TYPES_TRAINING_OBLIGATION] = []
    module_30: list[TYPES_TRAINING_OBLIGATION] = []
    module_37: list[TYPES_TRAINING_OBLIGATION] = []
