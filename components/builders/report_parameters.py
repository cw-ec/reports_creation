

class PDPSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Profile Report
    including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Profil de Section de Vote / Polling District Profile ",
            'rep_order': f"Décret de représentation de YR / Representation order of YR",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Polling District Profile / Profil de Section de Vote",
            'rep_order': f"Representation order of YR / Décret de représentation de YR"}

        # Headers for main table
        f_table_header = ["<b>Nº /<br/>NO.</b>", "<b>NOM /<br/>NAME</b>", "<b>ÉLECTEURS INSCRITS /<br/>ELECTORS LISTED</b>", "<b>NUL /<br/>VOID</b>"]
        e_table_header = ["<b>NO. /<br/>Nº</b>", "<b>NAME /<br/>NOM</b>", "<b>ELECTORS LISTED /<br/>ÉLECTEURS INSCRITS</b>", "<b>VOID /<br/>NUL</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "<b>Summary Statistics /<br/>Statistiques récapitulatives</b>"
        f_ss_table_header = "<b>Statistiques récapitulatives /<br/>Summary Statistics</b>"

        # Summary Stats Row Descriptions
        f_total_apd = "Total de sections de votes actives /<br/>Total of Active Polling Divisions"
        e_total_apd = "Total Active Polling Divisions /<br/>Total de sections de votes actives"

        f_total_noe = "Nombre total d’électeurs /<br/>Total Number of Electors"
        e_total_noe = "Total Number of Electors /<br/>Nombre total d’électeurs"

        f_avg_noe_per_apd = "Nombre moyen d'électeurs par section de vote ordinaire /<br/>Average Number of Electors per Ordinary Polling Division"
        e_avg_noe_per_apd = "Average Number of Electors per Ordinary Polling Division /<br/>Nombre moyen d'électeurs par section de vote ordinaire"

        f_total_vpd = "Nombre total de sections de vote nulles /<br/>Total Void Polling Divisions"
        e_total_vpd = "Total Void Polling Divisions / <br/> Nombre total de sections de vote nulles"

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              "ss_total_noe": e_total_noe,
                              "ss_total_apd": e_total_apd,
                              "ss_avg_noe_per_apd": e_avg_noe_per_apd,
                              "ss_total_vpd": e_total_vpd
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              "ss_total_noe": f_total_noe,
                              "ss_total_apd": f_total_apd,
                              "ss_avg_noe_per_apd": f_avg_noe_per_apd,
                              "ss_total_vpd": f_total_vpd
                              }
        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class APDSettings:
    """Contains all page setup components colours, margins page locations for the  Advanced Polling Districts Report
    including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Districts de vote par anticipation / Advance Polling Districts",
            'rep_order': f"Décret de représentation de YR / Representation order of YR",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Advance Polling Districts / Districts de vote par anticipation",
            'rep_order': f"Representation order of YR / Décret de représentation de YR"}

        # Headers for main table
        f_table_header = ["<b>Nº /<br/>NO.</b>", "<b>NOM /<br/>NAME</b>", "<b>SECTIONS DE VOTE /<br/>LISTED POLLING DIVISIONS</b>", "<b>TOTAL</b>"]
        e_table_header = ["<b>NO. /<br/>Nº</b>", "<b>NAME /<br/>NOM</b>", "<b>POLLING DIVISIONS /<br/>SECTIONS DE VOTE</b>", "<b>TOTAL</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "<b>Summary Statistics /<br/>Statistiques récapitulatives</b>"
        f_ss_table_header = "<b>Statistiques récapitulatives /<br/>Summary Statistics</b>"

        # Summary Stats Row Descriptions
        f_total_apd = "Nombre total de districts de vote par anticipation / Total number of advanced polling districts"
        e_total_apd = "Total number of advanced polling districts / Nombre total de districts de vote par anticipation"

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              "ss_total_apd": e_total_apd
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              "ss_total_apd": f_total_apd
                              }
        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class PDDSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Descriptions Report
        including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
                    'report_type': "Descriptions",
                    'rep_order': f"Décret de représentation de YR / Representation order of YR", }

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
                    'report_type': "Descriptions",
                    'rep_order': f"Representation order of YR / Décret de représentation de YR"}

        # Headers for main table
        e_table_header_range = ["STREET NAME /<br/>NOM DE RUE", "FROM /<br/>DE", "TO /<br/>À", "FROM /<br/>DE", "TO /<br/>À", "SIDE /<br/>CÔTÉ"]
        f_table_header_range = ["NOM DE RUE /<br/>STREET NAME", "DE /<br/>FROM", "À /<br/>TO", "DE /<br/>FROM", "À /<br/>TO", "CÔTÉ /<br/>SIDE"]

        e_table_header_mp = ["INSTITUTION /<br/>ÉTABLISSEMENT", "ADDRESS /<br/>ADRESSE", "ELECTORS LISTED /<br/>ÉLECTEURS INSCRITS"]
        f_table_header_mp = ["ÉTABLISSEMENT /<br/>INSTITUTION", "ADRESSE /<br/>ADDRESS", "ÉLECTEURS INSCRITS /<br/>ELECTORS_LISTED"]

        e_table_header_strm = ["TOWNSHIP /<br/>CANTON", "RANGE /<br/>RANG", "MERIDIAN /<br/>MÉRIDIEN", "SECTION NUMBER /<br/>NUMÉRO DE SECTION"]
        f_table_header_strm = ["CANTON /<br/>TOWNSHIP", "RANG /<br/>RANGE", "MÉRIDIEN /<br/>MERIDIAN", "NUMÉRO DE SECTION /<br/>SECTION NUMBER"]

        e_table_title = "Polling Division / Section de Vote"
        f_table_title = "Section de Vote / Polling Division"

        e_table_note = "NOTE: COMPRISES THE ENTIRE TERRITORY DELINEATED ON THE MAP. / COMPREND TOUT LE TERRITOIRE TEL QUE DÉLIMITÉ SUR LA CARTE."
        f_table_note = "NOTE: COMPREND TOUT LE TERRITOIRE TEL QUE DÉLIMITÉ SUR LA CARTE. / COMPRISES THE ENTIRE TERRITORY DELINEATED ON THE MAP."

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"



        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_title": e_table_title,
                              "table_header_range": e_table_header_range,
                              "table_header_mp": e_table_header_mp,
                              "table_header_strm": e_table_header_strm,
                              "table_note": e_table_note,
                              "footer_text": e_footer_text,
                              }
        self.f_params_dict = {"header": f_header,
                              "table_title": f_table_title,
                              "table_header_range": f_table_header_range,
                              "table_header_mp": f_table_header_mp,
                              "table_header_strm": f_table_header_strm,
                              "table_note": f_table_note,
                              "footer_text": f_footer_text,
                              }

        if (in_ed >= 24000) and (in_ed < 25000):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class DPKSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Descriptions Report
        including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
                    'report_type': "Indicateur des sections de vote de la circonscription / Electoral District Poll Key",
                    'rep_order': f"Décret de représentation de YR / Representation order of YR", }

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
                    'report_type': "Electoral District Poll Key / Indicateur des sections de vote de la circonscription",
                    'rep_order': f"Representation order of YR / Décret de représentation de YR"}

        # Headers for main table
        e_table_header = ["STREET NAME /<br/>NOM DE RUE", "FROM /<br/>DE", "TO /<br/>À", "FROM /<br/>DE", "TO /<br/>À", "SIDE /<br/>CÔTÉ", "PD /<br/>SV", "APD /<br/>DVA"]
        f_table_header = ["NOM DE RUE /<br/>STREET NAME", "DE /<br/>FROM", "À /<br/>TO", "DE /<br/>FROM", "À /<br/>TO", "CÔTÉ /<br/>SIDE", "SV /<br/>PD", "DVA /<br/>APD"]

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "footer_text": e_footer_text,
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "footer_text": f_footer_text,
                              }

        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class MPSSettings:
    """Contains all page setup components colours, margins page locations for the  Mobile Polls Summary (MPS) Report
    including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Sommaire de bureaux itinérants / Mobile Polls Summary",
            'rep_order': f"Décret de représentation de YR / Representation order of YR",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Mobile Polls Summary / Sommaire de bureaux itinérants",
            'rep_order': f"Representation order of YR / Décret de représentation de YR"}

        # Headers for main table
        f_table_header = ["<b>NUMÉRO DE LA SECTION DE VOTE /<br/>POLLING DIVISION NUMBER</b>", "<b> TOTAL DES ÉTABLISSEMENTS /<br/>TOTAL INSTITUTIONS</b>", "<b>ÉLECTEURS INSCRITS /<br/>ELECTORS LISTED</b>", "<b>BUREAUX DE VOTE PAR ANTICIPATION /<br/>ADVANCED POLLS</b>"]
        e_table_header = ["<b>POLLING DIVISION NUMBER /<br/>NUMÉRO DE LA SECTION DE VOTE</b>", "<b>TOTAL INSTITUTIONS /<br/>TOTAL DES ÉTABLISSEMENTS</b>", "<b>ELECTORS LISTED /<br/>ÉLECTEURS INSCRITS</b>", "<b>ADVANCED POLLS /<br/>BUREAUX DE VOTE PAR ANTICIPATION</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "<b>Summary Statistics /<br/>Statistiques récapitulatives</b>"
        f_ss_table_header = "<b>Statistiques récapitulatives /<br/>Summary Statistics</b>"

        # Summary Stats Row Descriptions
        f_total_pd = "Total de sections de votes /<br/>Total Polling Divisions"
        e_total_pd = "Total Polling Divisions /<br/>Total de sections de votes"

        f_total_noe = "Nombre total d’électeurs /<br/>Total Number of Electors"
        e_total_noe = "Total Number of Electors /<br/>Nombre total d’électeurs"

        f_total_inst = "Total Nombre d'établissements /<br/>Total Number of Institutions"
        e_total_inst = "Total Number of Institutions /<br/>Total Nombre d'établissements"

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              "ss_total_pd": e_total_pd,
                              "ss_total_noe": e_total_noe,
                              "ss_total_inst": e_total_inst
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              "ss_total_pd": f_total_pd,
                              "ss_total_noe": f_total_noe,
                              "ss_total_inst": f_total_inst
                              }
        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class IDRSettings:
    """Contains all page setup components colours, margins page locations for the  Mobile Polls Summary (MPS) Report
    including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Communautés avec des peuples autochtones / Communities with Indigenous Peoples",
            'rep_order': f"Décret de représentation de 2013 / Representation order of 2013",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Communities with Indigenous Peoples / Communautés avec des peuples autochtones",
            'rep_order': f"Representation order of 2023 / Décret de représentation de 2023"}

        # Headers for main table
        f_table_header = ["<b>NOM DE COMMUNAUTÉ /<br/>COMMUNITY NAME</b>", "<b>DESCRIPTION</b>", "<b>NUMÉRO DE SV /<br/>PD NO.</b>"]
        e_table_header = ["<b>COMMUNITY NAME /<br/>NOM DE COMMUNAUTÉ</b>", "<b>DESCRIPTION</b>", "<b>PD NO. /<br/>NUMÉRO DE SV</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "Summary Statistics /<br/>Statistiques récapitulatives"
        f_ss_table_header = "Statistiques récapitulatives /<br/>Summary Statistics"

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              }
        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict
