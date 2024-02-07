

class PDPSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Profile Report
    including French and English versions"""

    def __init__(self):

        # Header dicts additional report specific info appended later
        self.f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Profil de Section de Vote / Polling District Profile ",
            'rep_order': f"Décret de représentation de 2013 / Representation order of 2013",}

        self.e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Polling District Profile / Profil de Section de Vote",
            'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}


        # Headers for main table
        self.f_table_header = ["Nº / NO.", "NOM / NAME", "ÉLECTEURS INSCRITS / ELECTORS LISTED", "NUL / VOID"]
        self.e_table_header = ["NO. / Nº", "NAME / NOM", "ELECTORS LISTED / ÉLECTEURS INSCRITS ", "VOID / NUL"]

class ADPSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Profile Report
    including French and English versions"""

    def __init__(self):

        # Header dicts additional report specific info appended later
        self.f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Districts de vote par anticipation / Advance Polling Districts",
            'rep_order': f"Décret de représentation de 2013 / Representation order of 2013",}

        self.e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Advance Polling Districts / Districts de vote par anticipation",
            'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}


        # Headers for main table
        self.f_table_header = ["Nº / NO.", "NOM / NAME", "ÉLECTEURS INSCRITS / ELECTORS LISTED", "NUL / VOID"]
        self.e_table_header = ["NO. / Nº", "NAME / NOM", "ELECTORS LISTED / ÉLECTEURS INSCRITS ", "VOID / NUL"]
