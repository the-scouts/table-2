import pandas as pd

from table_2.utility import LATEST_DATA_ROOT


def load_table_2() -> pd.DataFrame:
    roles_path = LATEST_DATA_ROOT / "table-2-roles.csv"
    return pd.read_csv(roles_path, encoding="utf-8")


def preprocess_roles(roles: pd.DataFrame) -> pd.DataFrame:
    columns_map = {
        "Role Category": "category",
        "Role Subcategory": "subcategory",
        "Role Hierarchy": "hierarchy",
        "Role title": "title",
        "Variants": "variants",
        "Role class on Compass": "compass_class",
        "Hierarchy or Location": "location",
        "Line manager to help make the application": "line_manager",
        "Approval process \n(see 4.5)": "approval_process",
        "Approver": "approver",
        "Relevant Commissioner or body": "relevant",
        "Responsible for induction": "induction",
        "Getting Started requirement for full appointment \n(within 5 months)": "getting_started",
        "Training Obligations": "training",
        "Minimum Membership": "membership",
        "Ex Officio Charity Trustee role?sv": "trustee",
        "Criminal Records Disclosure Check Required?++": "disclosure",
        "Appointment Review Required?": "review",
    }
    roles.columns = [columns_map[col] for col in roles.columns]

    category_map = {
        "PROGRAMME DELIVERY ROLES": "Programme Delivery",
        "LINE MANAGER ROLES": "Line Manager",
        "GOVERNANCE ROLES": "Governance",
        "SUPPORT ROLES": "Support",
    }
    roles["category"] = [category_map[i] for i in roles["category"]]

    subcategory_map = {
        "Beaver Colony Leadership Team roles": "Beaver Colony",
        "Cub Pack Leadership Team roles": "Cub Pack",
        "Scout Troop Leadership Team roles": "Scout Troop",
        "Explorer Unit Leadership Team roles (may be linked with Group(s) via Partnership Agreements)": "Explorer Unit",
        "UK Headquarters - Delivery roles for major events": "UK Contingent",
        "SUPPORT ROLES - Deputy Managers": "Deputy Managers",
        "SUPPORT ROLES - Activities": "Activities",
        "SUPPORT ROLES - Administration roles - Administrators": "Administrators",
        "SUPPORT ROLES - Administration roles - Supporters": "Supporters",
        "SUPPORT ROLES - Adult Training": "Adult Training",
        "SUPPORT ROLES - Advisers": "Advisers",
        "SUPPORT ROLES - Assistant District, County and Regional Commissioners": "Assistant Commissioners",
        "SUPPORT ROLES - Camp site and Centre volunteers": "Site Volunteers",
        "SUPPORT ROLES - Chaplains": "Chaplains",
        "SUPPORT ROLES - Communication": "Communications",
        "SUPPORT ROLES - Contingent roles for major events": "Contingents",
        "SUPPORT ROLES - Leader roles on District, County & Country Teams": "Leaders",
        "SUPPORT ROLES - Presidents and Vice Presidents": "Presidents",
        "SUPPORT ROLES - Safety and Safeguarding": "Safe Scouting",
        "SUPPORT ROLES - Scout Active Support Units": "SASUs",
        "SUPPORT ROLES - Youth Commissioners": "Youth Commissioners",
    }
    roles["subcategory"] = [subcategory_map.get(i, i) for i in roles["subcategory"]]

    hierarchy_map = {
        # Group
        "Scout Group Roles": "Group",
        "Scout Group": "Group",
        "Group": "Group",
        # District
        "Scout District Roles": "District",
        "Scout District": "District",
        "District": "District",
        "Scout District or equivalent": "District",
        # County
        "Scout County or equivalent": "County",
        "Scout County": "County",
        # Region (X)
        "England and Wales Regions": "Region (England, Wales)",
        "Scout Region (England, Wales)": "Region (England, Wales)",
        "Region (England)": "Region (England)",
        "Scout Region - England": "Region (England)",
        "England Region": "Region (England)",
        # Country
        "Country Manager roles": "Country",
        "Countries": "Country",
        "Country": "Country",
        "Scout Countries": "Country",
        # HQ
        "UK Headquarters": "Headquarters",
        "Headquarters Manager roles": "Headquarters",
        "Headquarters": "Headquarters",
        "UK Headquarters - Roles for major events": "Headquarters",
    }
    roles["hierarchy"] = [hierarchy_map[i] for i in roles["hierarchy"]]

    # Remap locations to a series of country dummy (boolean) variables
    scotland_exclusion = "not Scot"  # must not contain the word "Scotland" as we do a contains check
    location_map = {
        "UK": "Headquarters",
        "National SASUs": "Headquarters",
        "World Jamboree, Moots and similar events": "UK Contingent",
        "World Jamborees, Moots and similar events": "UK Contingent",
        "District\n(not Scotland)": scotland_exclusion,
        "Scotalnd": "Scotland",
        "Group\n(not Scotland)": scotland_exclusion,
        "District\n (not Scotland)": scotland_exclusion,
        "Group (note: not a role in Scotland)": scotland_exclusion,
        "District (note: not a role in Scotland)": scotland_exclusion,
        "District - BSO, England, Northern Ireland, Wales": "BSO, England, Northern Ireland, Wales",
        "Group": "All",
        "District": "All",
        "County": "All",
    }
    roles["location"] = [location_map.get(i, i) for i in roles["location"]]
    # TODO can we remove e.g. Guernsey/Jersey - are these just role name variants, or do other things change?
    countries = (
        "England",
        "Scotland",
        "Northern Ireland",
        "Wales",
        "BSO",
        "Branches",
        "Guernsey",
        "Jersey",
        "Headquarters",
        "UK Contingent",
    )
    all_countries = roles["location"] == "All"
    not_scotland = roles["location"] == scotland_exclusion
    for country in countries:
        safe_country = country.lower().replace(" ", "_")
        current_country = roles["location"].str.contains(country, regex=False, case=False)
        if country in {"Headquarters", "UK Contingent"}:
            roles[f"location_{safe_country}"] = current_country
        elif country == "Scotland":
            roles[f"location_{safe_country}"] = current_country | all_countries
        else:
            roles[f"location_{safe_country}"] = current_country | all_countries | not_scotland
    del roles["location"]

    roles["membership"] = roles["membership"].fillna("None")

    # Acting roles
    roles.loc[roles["review"].str.contains("N/a", regex=False, case=False).astype("boolean"), "review"] = "N/A"
    roles.loc[roles["review"].str.contains("yes", regex=False, case=False).astype("boolean"), "review"] = "Yes"

    trustee_map = {
        "Yes \n(if opts-in)": "Opt-in",
        "No unless opts-in to a Group Executive role under the terms of a Partnership Agreement with a Group.": "Opt-in",
        " No": "No",
    }
    roles["trustee"] = [trustee_map.get(i, i) for i in roles["trustee"]]

    disclosure_map = {"Yes++": "Yes (SV)", "Yes ": "Yes", "No ": "No"}
    roles["disclosure"] = [disclosure_map.get(i, i) for i in roles["disclosure"]]

    getting_started_map = {
        "No requirement": "No Requirement",
        # Contingent Leader / DCL / CMT / CST (new from R2R)
        "Modules 1, GDPR, Safety, Safeguarding and 4 if not completed within 3 years prior to the role start date.": "Modules 1, GDPR, Safety, Safeguarding, 2 and 4",
        # Deputy Chief Commissioner (Country)
        "Modules 1, GDPR, Safety, Safeguarding, 2  and 4\n(Trustee Introduction for 1 role holder)": "Modules 1, GDPR, Safety, Safeguarding, 2, 4 and Trustee Introduction",
        # Chief Commissioner (Branch) (new from R2R)
        "As agreed": "Module 1, Safety, Safeguarding",
    }
    roles["getting_started"] = [getting_started_map.get(i, i) for i in roles["getting_started"]]
    roles["getting_started"] = roles["getting_started"].fillna("N/A")

    sc_wb_fa = "[Section] Wood Badge and First Aid certificate (within 3 years)"
    ms_wb_fa = "[M&S] Wood Badge and First Aid certificate (within 3 years)"
    training_map = {
        "None ": "None",
        "No requirement": "None",
        "No requirement as completed through Trustee role requirements. ": "None",
        # Unit Leader / Asst Unit Leader (new from R2R)
        "It is recommended that role holders have the relevant Wood Badge and First Aid Certificate prior to appointment, or are close to completing both.": sc_wb_fa,
        # Contingent Leader / DCL / CMT (new from R2R)
        "It is strongly recommended that role holders have the relevant Wood Badge and First Aid Certificate prior to appointment, or are close to completing both.": ms_wb_fa,
        # Assistant District Commissioner (Adult Training) (new from R2R)
        "[M&S] Wood Badge and First Aid certificate ": ms_wb_fa,
        # Chief Commissioner (Branch) (new from R2R)
        "Module 1, Safety, Safeguarding, Wood Badge and First Aid certificate (within 3 years)": sc_wb_fa,
        # Project Lead / POW Member / Programme Sponsor
        "Modules 1, GDPR, Safety and Safeguarding": "Modules 1, GDPR, Safety and Safeguarding (within 5 months)",
        # Regional Adviser - Activities
        "Modules 1, GDPR, Safety, Safeguarding, 2 and 4": "Modules 1, GDPR, Safety, Safeguarding, 2 and 4 (within 5 months)",
    }
    roles["training"] = [training_map.get(i, i) for i in roles["training"]]
    roles["training"] = roles["training"].str.replace(r"\s+", " ", regex=True).str.lower().str.strip().fillna("N/A")
    roles["training"] = roles["training"].str.split(r", | and | & | \(|\) *")

    for module in ("1", "Trustee Introduction", "2", "3", "4", "Safety", "Safeguarding", "GDPR"):
        safe_module = f"module_{module.lower().replace(' ', '_')}"
        potential_training_modules = {module.lower(), f"module {module}", f"modules {module}"}
        training_mask = [any(m in i for m in potential_training_modules) for i in roles["training"]]
        # Getting started is second so that it overwrites training obligations if duplicates
        roles[safe_module] = "NA"
        roles.loc[training_mask, safe_module] = "TO"  # Training Obligation
        roles.loc[roles["getting_started"].str.contains(module, regex=False, case=False), safe_module] = "GS"  # Getting Started
    del roles["getting_started"]

    three_years = {"within 3 years"}.issubset
    five_months = {"within 5 months"}.issubset
    for module in (
        "[section] wood badge",
        "[m&s] wood badge",
        "first aid certificate",
        "7",
        "24",
        "25",
        "30",
        "37",
        "opts-in to trustee",
    ):
        if module != "opts-in to trustee":
            safe_module = f"module_{module.lower().replace(' ', '_').replace('&', '').replace('[', '').replace(']', '')}"
            mark = "TO"  # Training Obligation
        else:
            safe_module = "module_trustee_introduction"
            mark = "OP"  # OPt in
        roles[safe_module] = "NA"
        training_mask = [any(module in training_mod for training_mod in training_lst) for training_lst in roles["training"]]
        roles.loc[training_mask, safe_module] = mark
        roles.loc[[three_years(training_lst) for training_lst in roles["training"].tolist()], "training_deadline"] = "3Y"
        roles.loc[[five_months(training_lst) for training_lst in roles["training"].tolist()], "training_deadline"] = "5M"
    del roles["training"]

    return roles


def setup_roles():
    roles = load_table_2()
    roles = preprocess_roles(roles)
    roles.to_feather(LATEST_DATA_ROOT / "table-2-roles.feather")


if __name__ == "__main__":
    setup_roles()
