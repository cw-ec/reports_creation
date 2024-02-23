

class PDPSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Profile Report
    including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
            'report_type': "Profil de Section de Vote / Polling District Profile ",
            'rep_order': f"Décret de représentation de 2013 / Representation order of 2013",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Polling District Profile / Profil de Section de Vote",
            'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}

        # Headers for main table
        f_table_header = ["<b>Nº / NO.</b>", "<b>NOM / NAME</b>", "<b>ÉLECTEURS INSCRITS / ELECTORS LISTED</b>", "<b>NUL / VOID</b>"]
        e_table_header = ["<b>NO. / Nº</b>", "<b>NAME / NOM</b>", "<b>ELECTORS LISTED / ÉLECTEURS INSCRITS</b>", "<b>VOID / NUL</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "Summary Statistics / Statistiques récapitulatives"
        f_ss_table_header = "Statistiques récapitulatives / Summary Statistics"

        # Summary Stats Row Descriptions
        f_total_apd = "Total de sections de votes actives / Total of Active Polling Divisions"
        e_total_apd = "Total Active Polling Divisions / Total de sections de votes actives"

        f_total_noe = "Nombre total d’électeurs / Total Number of Electors"
        e_total_noe = "Total Number of Electors / Nombre total d’électeurs"

        f_avg_noe_per_apd = "Nombre moyen d'électeurs par section de vote ordinaire / Average Number of Electors per Ordinary Polling Division"
        e_avg_noe_per_apd = "Average Number of Electors per Ordinary Polling Division / Nombre moyen d'électeurs par section de vote ordinaire"

        f_total_vpd = "Nombre total de sections de vote nulles / Total Void Polling Divisions"
        e_total_vpd = "Total Void Polling Divisions / Nombre total de sections de vote nulles"

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
            'rep_order': f"Décret de représentation de 2013 / Representation order of 2013",}

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
            'report_type': "Advance Polling Districts / Districts de vote par anticipation",
            'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}

        # Headers for main table
        f_table_header = ["<b>Nº / NO.</b>", "<b>NOM / NAME</b>", "<b>SECTIONS DE VOTE / LISTED POLLING DIVISIONS</b>", "<b>TOTAL</b>"]
        e_table_header = ["<b>NO. / Nº</b>", "<b>NAME / NOM</b>", "<b>POLLING DIVISIONS / SECTIONS DE VOTE</b>", "<b>TOTAL</b>"]

        # Summary Statistics Table Header
        e_ss_table_header = "Summary Statistics / Statistiques récapitulatives"
        f_ss_table_header = "Statistiques récapitulatives / Summary Statistics"

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
                    'rep_order': f"Décret de représentation de 2013 / Representation order of 2013", }

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
                    'report_type': "Descriptions",
                    'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}

        # Headers for main table
        e_table_header_range = ["STREET NAME / NOM DE RUE", "FROM / DE", "TO / À", "FROM / DE", "TO / À", "SIDE / CÔTÉ"]
        f_table_header_range = ["NOM DE RUE / STREET NAME", "DE / FROM", "À / TO", "DE / FROM", "À / TO", "CÔTÉ / SIDE"]

        e_table_header_mp = ["INSTITUTION / ÉTABLISSEMENT", "ADDRESS / ADRESSE", "ELECTORS_LISTED / ÉLECTEURS INSCRITS"]
        f_table_header_mp = ["ÉTABLISSEMENT / INSTITUTION", "ADRESSE / ADDRESS", "ÉLECTEURS INSCRITS / ELECTORS_LISTED"]

        e_table_header_strm = ["TOWNSHIP / CANTON", "RANGE / RANG", "MERIDIAN / MÉRIDIEN", "SECTION NUMBER / NUMÉRO DE SECTION", "SPECIFICATIONS / SPÉCIFICATION"]
        f_table_header_strm = ["CANTON / TOWNSHIP", "RANG / RANGE", "MÉRIDIEN / MERIDIAN", "NUMÉRO DE SECTION / SECTION NUMBER", "SPÉCIFICATION / SPECIFICATIONS"]

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

        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict

class DPKSettings:
    """Contains all page setup components colours, margins page locations for the Polling District Descriptions Report
        including French and English versions"""

    def __init__(self, in_ed):

        # Header dicts additional report specific info appended later
        f_header = {'dept_nme': "ÉLECTIONS CANADA / ELECTIONS CANADA",
                    'report_type': "Electoral District Poll Key / Indicateur des sections de vote de la circonscription",
                    'rep_order': f"Décret de représentation de 2013 / Representation order of 2013", }

        e_header = {'dept_nme': "ELECTIONS CANADA / ÉLECTIONS CANADA",
                    'report_type': "Indicateur des sections de vote de la circonscription / Electoral District Poll Key",
                    'rep_order': f"Representation order of 2013 / Décret de représentation de 2013"}

        # Headers for main table
        e_table_header = ["STREET NAME / NOM DE RUE", "FROM / DE", "TO / À", "FROM / DE", "TO / À", "SIDE / CÔTÉ", "PD / SV", "APD / DVA"]
        f_table_header = ["NOM DE RUE / STREET NAME", "DE / FROM", "À / TO", "DE / FROM", "À / TO", "CÔTÉ / SIDE", "SV / PD", "DVA / APD"]

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "footer_text": e_footer_text,
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header_range": f_table_header,
                              "footer_text": f_footer_text,
                              }

        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict
