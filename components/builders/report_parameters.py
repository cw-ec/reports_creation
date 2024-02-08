

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
        f_table_header = ["Nº / NO.", "NOM / NAME", "ÉLECTEURS INSCRITS / ELECTORS LISTED", "NUL / VOID"]
        e_table_header = ["NO. / Nº", "NAME / NOM", "ELECTORS LISTED / ÉLECTEURS INSCRITS ", "VOID / NUL"]

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

        # Page number text
        e_num_txt = "of / de"
        f_num_txt = "de / of"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              "num_txt": e_num_txt,
                              "ss_total_noe": e_total_noe,
                              "ss_total_apd": e_total_apd,
                              "ss_avg_noe_per_apd": e_avg_noe_per_apd,
                              "ss_total_vpd": e_total_vpd
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              "num_txt": f_num_txt,
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
    """Contains all page setup components colours, margins page locations for the Polling District Profile Report
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
        f_table_header = ["Nº / NO.", "NOM / NAME", "SECTIONS DE VOTE / LISTED POLLING", "NUL / VOID"]
        e_table_header = ["NO. / Nº", "NAME / NOM", "POLLING DIVISIONS / SECTIONS DE VOTE", "VOID / NUL"]

        # Summary Statistics Table Header
        e_ss_table_header = "Summary Statistics / Statistiques récapitulatives"
        f_ss_table_header = "Statistiques récapitulatives / Summary Statistics"

        # Summary Stats Row Descriptions
        f_total_apd = "Nombre total de districts de vote par anticipation / Total number of advanced polling districts"
        e_total_apd = "Total number of advanced polling districts / Nombre total de districts de vote par anticipation"

        # Footer Text
        e_footer_text = "Printed on / Imprimé le"
        f_footer_text = "Imprimé le / Printed on"

        # Page number text
        e_num_txt = "of / de"
        f_num_txt = "de / of"

        # Create a dictionary of english first parameters to allow for easy access
        self.e_params_dict = {"header": e_header,
                              "table_header": e_table_header,
                              "ss_table_header": e_ss_table_header,
                              "footer_text": e_footer_text,
                              "num_txt": e_num_txt,
                              "ss_total_apd": e_total_apd
                              }
        self.f_params_dict = {"header": f_header,
                              "table_header": f_table_header,
                              "ss_table_header": f_ss_table_header,
                              "footer_text": f_footer_text,
                              "num_txt": f_num_txt,
                              "ss_total_apd": f_total_apd
                              }
        if (in_ed > 24000) and (in_ed < 24999):
            self.settings_dict = self.f_params_dict
        else:
            self.settings_dict = self.e_params_dict
