import logging
import sys
import os
import shutil
import pandas as pd
from datetime import datetime
from pathlib import Path

def logging_setup(log_dir=".\\logs") -> logging.getLogger():
    """Sets up logging takes one parameter to set a directory for the output log file"""

    create_dir(log_dir)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{datetime.today().strftime('%Y-%m-%d')}.log")),
            logging.StreamHandler(sys.stdout)
        ],
        datefmt="[%Y-%m-%d %H:%M:%S]"  # Tidy's up datetime format
    )
    return logging.getLogger()

def create_dir(path: str) -> None:
    """Check if directory exists and if it doesn't create it."""
    if not os.path.exists(path):
        os.makedirs(path)

def delete_dir(in_path: str) -> None:
    """Checks to see if the given directory exists if it does then delete it and all its contents"""

    in_path = Path(in_path)
    if in_path.exists() and in_path.is_dir():
        shutil.rmtree(in_path)

def to_dataframe(to_import: str, sheet_name=0, encoding='UTF-8') -> pd.DataFrame:
    """Import the given path into a pandas dataframe. Returns that pandas dataframe

    to_import = the path to the data to import into the dataframe. Required

    sheet = Name of the sheet to import into a dataframe. Can be integer or text of name (str)

    """

    path_list = os.path.split(to_import)
    f_type = path_list[-1].split('.')[-1]

    if f_type == 'csv':
        return pd.read_csv(to_import, encoding=encoding, low_memory=False)
    elif f_type in ["xlsx", "xls"]:
        return pd.read_excel(to_import, sheet_name=sheet_name)
    else:
        raise Exception(f"File Extension: {f_type} not yet handled by this function")

def add_en_dash(text:str) -> str:
    """Adds en dashes to text"""
    for c in [u'\u0097', "â€”", "â■■", "--"] :
        if c in text:
            # Replace hyphens with em dashes
            return text.replace(c, u"\u2014")
        else:
            return text

def get_prov_from_code(prov_code: int, type='full') -> str:
    """Input an ed_code and get the province name in return"""

    # Corrected translations eng/ fre or fre / eng where needed with prov code associations
    prov_dict_full = {
        10 : 'NEWFOUNDLAND AND LABRADOR / TERRE-NEUVE-ET-LABRADOR',
        11 : 'PRINCE EDWARD ISLAND / ÎLE-DU-PRINCE-ÉDOUARD',
        12 : 'NOVA SCOTIA / NOUVELLE-ÉCOSSE',
        13 : 'NEW BRUNSWICK / NOUVEAU-BRUNSWICK',
        24 : 'QUÉBEC / QUEBEC',
        35 : 'ONTARIO',
        46 : 'MANITOBA',
        47 : 'SASKATCHEWAN',
        48 : 'ALBERTA',
        59 : 'BRITISH COLUMBIA / COLOMBIE-BRITANNIQUE',
        60 : 'YUKON',
        61 : 'NORTHWEST TERRITORIES / TERRITOIRES DU NORD-OUEST',
        62 : 'NUNAVUT'
    }

    prov_dict_abv = {
        10 : 'NL',
        11 : 'PE',
        12 : 'NS',
        13 : 'NB',
        24 : 'QC',
        35 : 'ON',
        46 : 'MB',
        47 : 'SK',
        48 : 'AB',
        59 : 'BC',
        60 : 'YT',
        61 : 'NT',
        62 : 'NU'

    }

    # Extract the first two numbers of the input ed code to get the prov code
    pr_code = int(str(prov_code)[:2])

    if pr_code in prov_dict_full:

        if type == 'full':  # To return full bilingual names
            return prov_dict_full[pr_code]

        if type == 'abv':  # To return abbreviations
            return prov_dict_abv[pr_code]

    else:
        raise Exception(f"ED_Code {prov_code} not in province when reduced to {pr_code} not in province dict. Check input")

def to_excel(df: pd.DataFrame, out_dir: str, out_nme: str, header: list[str]) -> None:
    """Exports input dataframe to excel"""

    if len(df.columns) != len(header):
        print('header and column count do not match no excel produced')

    else:
        df.to_excel(os.path.join(out_dir, f"{out_nme}.xlsx"),
                    index=False,  # No need for the index column to be included
                    sheet_name=out_nme,  # Give the sheet the same name as the Excel name
                    header=header  # We want to use the column names given not the ones that come with the data
                    )

def get_ed_name_from_code(code: int) -> str:
    """Returns the Fed 343 name for a given ed number"""

    ed_dict = {10001: 'Avalon', 10002: 'Cape Spear', 10003: 'Central Newfoundland', 10004: 'Labrador', 10005: 'Long Range Mountains', 10006: "St. John's East  / St. John's-Est", 10007: 'Terra Nova--The Peninsulas / Terra Nova--Les Péninsules', 11001: 'Cardigan', 11002: 'Charlottetown', 11003: 'Egmont', 11004: 'Malpeque', 12001: 'Acadie--Annapolis', 12002: 'Cape Breton--Canso--Antigonish', 12003: 'Central Nova / Nova-Centre', 12004: 'Cumberland--Colchester', 12005: 'Dartmouth--Cole Harbour', 12006: 'Halifax', 12007: 'Halifax West / Halifax-Ouest', 12008: 'Kings--Hants', 12009: 'Sackville--Bedford--Preston', 12010: 'South Shore--St. Margarets', 12011: 'Sydney--Glace Bay', 13001: 'Acadie--Bathurst', 13002: 'Beauséjour', 13003: 'Fredericton--Oromocto', 13004: 'Fundy Royal', 13005: 'Madawaska--Restigouche', 13006: 'Miramichi--Grand Lake', 13007: 'Moncton--Dieppe', 13008: 'Saint John--Kennebecasis', 13009: 'Saint John--St. Croix', 13010: 'Tobique--Mactaquac', 24001: 'Abitibi--Baie-James--Nunavik--Eeyou', 24002: 'Abitibi--Témiscamingue', 24003: 'Ahuntsic-Cartierville', 24004: 'Alfred-Pellan', 24005: 'Argenteuil--La Petite-Nation', 24006: 'Beauce', 24007: 'Beauharnois--Salaberry--Soulanges--Huntingdon', 24008: 'Beauport--Limoilou', 24009: 'Bécancour--Nicolet--Saurel--Alnôbak', 24010: 'Bellechasse--Les Etchemins--Lévis', 24011: 'Beloeil--Chambly', 24012: 'Berthier--Maskinongé', 24013: 'Bourassa', 24014: 'Brome--Missisquoi', 24015: 'Brossard--Saint-Lambert', 24016: 'Charlesbourg--Haute-Saint-Charles', 24017: 'Châteauguay--Les Jardins-de-Napierville', 24018: 'Chicoutimi--Le Fjord', 24019: 'Compton--Stanstead', 24020: 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 24021: 'Côte-Nord--Kawawachikamach--Nitassinan', 24022: 'Dorval--Lachine--LaSalle', 24023: 'Drummond', 24024: 'Gaspésie--Les Îles-de-la-Madeleine--Listuguj', 24025: 'Gatineau', 24026: 'Hochelaga--Rosemont-Est', 24027: 'Honoré-Mercier', 24028: 'Hull--Aylmer', 24029: 'Joliette--Manawan', 24030: 'Jonquière', 24031: "La Pointe-de-l'Île", 24032: 'La Prairie--Atateken', 24033: 'Lac-Saint-Jean', 24034: 'Lac-Saint-Louis', 24035: 'LaSalle--Émard--Verdun', 24036: 'Laurentides--Labelle', 24037: 'Laurier--Sainte-Marie', 24038: 'Laval--Les Îles', 24039: "Les Pays-d'en-Haut", 24040: 'Lévis--Lotbinière', 24041: 'Longueuil--Charles-LeMoyne', 24042: 'Longueuil--Saint-Hubert', 24043: 'Louis-Hébert', 24044: 'Louis-Saint-Laurent--Akiawenhrahk', 24045: 'Marc-Aurèle-Fortin', 24046: 'Mégantic--L\x92Érable--Lotbinière', 24047: 'Mirabel', 24048: 'Mont-Royal / Mount Royal', 24049: 'Mont-Saint-Bruno--L\x92Acadie', 24050: 'Montcalm', 24051: 'Montmorency--Charlevoix', 24052: 'Notre-Dame-de-Grâce--Westmount', 24053: 'Outremont', 24054: 'Papineau', 24055: 'Pierre-Boucher--Les Patriotes--Verchères', 24056: 'Pierrefonds--Dollard', 24057: 'Pontiac--Kitigan Zibi', 24058: 'Portneuf--Jacques-Cartier', 24059: 'Québec-Centre / Québec Centre', 24060: 'Repentigny', 24061: 'Richmond--Arthabaska', 24062: 'Rimouski--La Matapédia', 24063: 'Rivière-des-Mille-Îles', 24064: 'Rivière-du-Nord', 24065: 'Rosemont--La Petite-Patrie', 24066: 'Saint-Hyacinthe--Bagot--Acton', 24067: 'Saint-Jean', 24068: 'Saint-Laurent', 24069: 'Saint-Léonard--Saint-Michel', 24070: 'Saint-Maurice--Champlain', 24071: 'Shefford', 24072: 'Sherbrooke', 24073: 'Terrebonne', 24074: 'Thérèse-De Blainville', 24075: 'Trois-Rivières', 24076: 'Vaudreuil', 24077: 'Ville-Marie--Le Sud-Ouest--Île-des-Soeurs', 24078: 'Vimy', 35001: 'Ajax', 35002: 'Algonquin--Renfrew--Pembroke', 35003: 'Aurora--Oak Ridges--Richmond Hill', 35004: 'Barrie South--Innisfil / Barrie-Sud--Innisfil', 35005: 'Barrie--Springwater--Oro-Medonte', 35006: 'Bay of Quinte', 35007: 'Beaches--East York', 35008: 'Bowmanville--Oshawa North / Bowmanville--Oshawa-Nord', 35009: 'Brampton Centre / Brampton-Centre', 35010: 'Brampton--Chinguacousy Park', 35011: 'Brampton East / Brampton-Est', 35012: 'Brampton North--Caledon / Brampton-Nord--Caledon', 35013: 'Brampton South / Brampton-Sud', 35014: 'Brampton West / Brampton-Ouest', 35015: 'Brantford--Brant South--Six Nations / Brantford--Brant-Sud--Six Nations', 35016: 'Bruce--Grey--Owen Sound', 35017: 'Burlington', 35018: 'Burlington North--Milton West / Burlington-Nord--Milton-Ouest', 35019: 'Cambridge', 35020: 'Carleton', 35021: 'Chatham-Kent--Leamington', 35022: 'Davenport', 35023: 'Don Valley North / Don Valley-Nord', 35024: 'Don Valley West / Don Valley-Ouest', 35025: 'Dufferin--Caledon', 35026: 'Eglinton--Lawrence', 35027: 'Elgin--St. Thomas--London South / Elgin--St. Thomas--London-Sud', 35028: 'Essex', 35029: 'Etobicoke Centre / Etobicoke-Centre', 35030: 'Etobicoke--Lakeshore', 35031: 'Etobicoke North / Etobicoke-Nord', 35032: 'Flamborough--Glanbrook--Brant North / Flamborough--Glanbrook--Brant-Nord', 35033: 'Guelph', 35034: 'Haldimand--Norfolk', 35035: 'Haliburton--Kawartha Lakes', 35036: 'Hamilton Centre / Hamilton-Centre', 35037: 'Hamilton East--Stoney Creek / Hamilton-Est--Stoney Creek', 35038: 'Hamilton Mountain', 35039: 'Hamilton West--Ancaster--Dundas / Hamilton-Ouest--Ancaster--Dundas', 35040: 'Hastings--Lennox and Addington--Tyendinaga', 35041: 'Humber River--Black Creek', 35042: 'Huron--Bruce', 35043: 'Kanata', 35044: 'Kapuskasing--Timmins--Mushkegowuk', 35045: 'Kenora--Kiiwetinoong', 35046: 'Kingston and the Islands / Kingston et les Îles', 35047: 'King--Vaughan', 35048: 'Kitchener Centre / Kitchener-Centre', 35049: 'Kitchener--Conestoga', 35050: 'Kitchener South--Hespeler / Kitchener-Sud--Hespeler', 35051: 'Lanark--Frontenac', 35052: 'Leeds--Grenville--Thousand Islands--Rideau Lakes', 35053: 'London Centre / London-Centre', 35054: 'London--Fanshawe', 35055: 'London West / London-Ouest', 35056: 'Markham--Stouffville', 35057: 'Markham--Thornhill', 35058: 'Markham--Unionville', 35059: 'Middlesex--London', 35060: 'Milton East--Halton Hills South / Milton-Est--Halton Hills-Sud', 35061: 'Mississauga Centre / Mississauga-Centre', 35062: 'Mississauga East--Cooksville / Mississauga-Est--Cooksville', 35063: 'Mississauga--Erin Mills', 35064: 'Mississauga--Lakeshore', 35065: 'Mississauga--Malton', 35066: 'Mississauga--Streetsville', 35067: 'Nepean', 35068: 'Newmarket--Aurora', 35069: 'New Tecumseth--Gwillimbury', 35070: 'Niagara Falls--Niagara-on-the-Lake', 35071: 'Niagara South / Niagara-Sud', 35072: 'Niagara West / Niagara-Ouest', 35073: 'Nipissing--Timiskaming', 35074: 'Northumberland--Clarke', 35075: 'Oakville East / Oakville-Est', 35076: 'Oakville West / Oakville-Ouest', 35077: 'Orléans', 35078: 'Oshawa', 35079: 'Ottawa Centre / Ottawa-Centre', 35080: 'Ottawa South / Ottawa-Sud', 35081: 'Ottawa--Vanier--Gloucester', 35082: 'Ottawa West--Nepean / Ottawa-Ouest--Nepean', 35083: 'Oxford', 35084: 'Parry Sound--Muskoka', 35085: 'Perth--Wellington', 35086: 'Peterborough', 35087: 'Pickering--Brooklin', 35088: 'Prescott--Russell--Cumberland', 35089: 'Richmond Hill South / Richmond Hill-Sud', 35090: 'Sarnia--Lambton--Bkejwanong', 35091: 'Sault Ste. Marie--Algoma', 35092: 'Scarborough--Agincourt', 35093: 'Scarborough Centre--Don Valley East / Scarborough-Centre--Don Valley-Est', 35094: 'Scarborough--Guildwood--Rouge Park', 35095: 'Scarborough North / Scarborough-Nord', 35096: 'Scarborough Southwest / Scarborough-Sud-Ouest', 35097: 'Scarborough--Woburn', 35098: 'Simcoe--Grey', 35099: 'Simcoe North / Simcoe-Nord', 35100: 'Spadina--Harbourfront', 35101: 'St. Catharines', 35102: 'Stormont--Dundas--Glengarry', 35103: 'Sudbury', 35104: 'Sudbury East--Manitoulin--Nickel Belt / Sudbury-Est--Manitoulin--Nickel Belt', 35105: "Taiaiako'n--Parkdale--High Park", 35106: 'Thornhill', 35107: 'Thunder Bay--Rainy River', 35108: 'Thunder Bay--Superior North / Thunder Bay--Supérieur-Nord', 35109: 'Toronto Centre / Toronto-Centre', 35110: 'Toronto--Danforth', 35111: "Toronto--St. Paul's", 35112: 'University--Rosedale', 35113: 'Vaughan--Woodbridge', 35114: 'Waterloo', 35115: 'Wellington--Halton Hills North / Wellington--Halton Hills-Nord', 35116: 'Whitby', 35117: 'Willowdale', 35118: 'Windsor--Tecumseh--Lakeshore', 35119: 'Windsor West / Windsor-Ouest', 35120: 'York Centre / York-Centre', 35121: 'York--Durham', 35122: 'York South--Weston--Etobicoke / York-Sud--Weston--Etobicoke', 46001: 'Brandon--Souris', 46002: 'Churchill--Keewatinook Aski', 46003: 'Elmwood--Transcona', 46004: 'Kildonan--St. Paul', 46005: 'Portage--Lisgar', 46006: 'Provencher', 46007: 'Riding Mountain / Mont-Riding', 46008: 'St. Boniface--St. Vital / Saint-Boniface--Saint-Vital', 46009: 'Selkirk--Interlake--Eastman', 46010: 'Winnipeg Centre / Winnipeg-Centre', 46011: 'Winnipeg North / Winnipeg-Nord', 46012: 'Winnipeg South / Winnipeg-Sud', 46013: 'Winnipeg South Centre / Winnipeg-Centre-Sud', 46014: 'Winnipeg West / Winnipeg-Ouest', 47001: 'Battlefords--Lloydminster--Meadow Lake', 47002: 'Carlton Trail--Eagle Creek / Sentier Carlton--Eagle Creek', 47003: 'Desnethé--Missinippi--Churchill River / Desnethé--Missinippi--Rivière Churchill', 47004: 'Moose Jaw--Lake Centre--Lanigan', 47005: 'Prince Albert ', 47006: 'Regina--Lewvan', 47007: "Regina--Qu'Appelle ", 47008: 'Regina--Wascana ', 47009: 'Saskatoon South / Saskatoon-Sud', 47010: 'Saskatoon--University', 47011: 'Saskatoon West / Saskatoon-Ouest', 47012: 'Souris--Moose Mountain ', 47013: 'Swift Current--Grasslands--Kindersley', 47014: 'Yorkton--Melville ', 48001: 'Airdrie--Cochrane', 48002: 'Battle River--Crowfoot', 48003: 'Bow River', 48004: 'Calgary Centre / Calgary-Centre', 48005: 'Calgary Confederation', 48006: 'Calgary Crowfoot', 48007: 'Calgary East / Calgary-Est', 48008: 'Calgary Heritage', 48009: 'Calgary McKnight', 48010: 'Calgary Midnapore', 48011: 'Calgary Nose Hill', 48012: 'Calgary Shepard', 48013: 'Calgary Signal Hill', 48014: 'Calgary Skyview', 48015: 'Edmonton Centre / Edmonton-Centre', 48016: 'Edmonton Gateway', 48017: 'Edmonton Griesbach', 48018: 'Edmonton Manning', 48019: 'Edmonton Northwest / Edmonton-Nord-Ouest', 48020: 'Edmonton Riverbend', 48021: 'Edmonton Southeast / Edmonton-Sud-Est', 48022: 'Edmonton Strathcona', 48023: 'Edmonton West / Edmonton-Ouest', 48024: 'Foothills', 48025: 'Fort McMurray--Cold Lake', 48026: 'Grande Prairie', 48027: 'Lakeland', 48028: 'Leduc--Wetaskiwin', 48029: 'Lethbridge', 48030: 'Medicine Hat--Cardston--Warner', 48031: 'Parkland', 48032: 'Peace River--Westlock', 48033: 'Ponoka--Didsbury', 48034: 'Red Deer', 48035: 'Sherwood Park--Fort Saskatchewan', 48036: 'St. Albert--Sturgeon River', 48037: 'Yellowhead', 59001: 'Abbotsford--South Langley / Abbotsford--Langley-Sud', 59002: 'Burnaby Central', 59003: 'Burnaby North--Seymour / Burnaby-Nord--Seymour', 59004: 'Cariboo--Prince George', 59005: 'Chilliwack--Hope', 59006: 'Cloverdale--Langley City', 59007: 'Columbia--Kootenay--Southern Rockies', 59008: 'Coquitlam--Port Coquitlam', 59009: 'Courtenay--Alberni', 59010: 'Cowichan--Malahat--Langford', 59011: 'Delta', 59012: 'Esquimalt--Saanich--Sooke', 59013: 'Fleetwood--Port Kells', 59014: 'Kamloops--Shuswap--Central Rockies', 59015: 'Kamloops--Thompson--Nicola', 59016: 'Kelowna', 59017: 'Langley Township--Fraser Heights', 59018: 'Mission--Matsqui--Abbotsford', 59019: 'Nanaimo--Ladysmith', 59020: 'New Westminster--Burnaby--Maillardville', 59021: 'North Island--Powell River', 59022: 'North Vancouver--Capilano', 59023: 'Okanagan Lake West--South Kelowna / Okanagan Lake-Ouest--Kelowna-Sud', 59024: 'Pitt Meadows--Maple Ridge', 59025: 'Port Moody--Coquitlam', 59026: 'Prince George--Peace River--Northern Rockies', 59027: 'Richmond Centre--Marpole / Richmond-Centre--Marpole', 59028: 'Richmond East--Steveston / Richmond-Est--Steveston', 59029: 'Saanich--Gulf Islands', 59030: 'Similkameen--South Okanagan--West Kootenay / Similkameen--Okanagan-Sud--Kootenay-Ouest', 59031: 'Skeena--Bulkley Valley', 59032: 'South Surrey--White Rock / Surrey-Sud--White Rock', 59033: 'Surrey Centre / Surrey-Centre', 59034: 'Surrey Newton', 59035: 'Vancouver Centre / Vancouver-Centre', 59036: 'Vancouver East / Vancouver-Est', 59037: 'Vancouver Fraserview--South Burnaby / Vancouver Fraserview--Burnaby-Sud', 59038: 'Vancouver Granville', 59039: 'Vancouver Kingsway', 59040: 'Vancouver Quadra', 59041: 'Vernon--Lake Country--Monashee', 59042: 'Victoria', 59043: 'West Vancouver--Sunshine Coast--Sea to Sky Country', 60001: 'Yukon', 61001: 'Northwest Territories / Territoires du Nord-Ouest', 62001: 'Nunavut'}
    if code in ed_dict:
        return ed_dict[code]
    else:
        raise Exception(f"ED Code {code} does not exist in the 343 dictionary.")

def conv_strm_field(value: str) -> str:
    """Takes an input string and attempts to convert it to an integer. If fails returns the original string"""

    try:
         outvalue = str(int(value)).zfill(3)
         return outvalue
    except:
        outvalue = value.zfill(3)
        return outvalue

def get_excel_header(fed_num: int, report_type: str) -> list[str]:
    """Returns the Excel header for the given report type and fed num"""

    if report_type == 'PDP':
        if int(str(fed_num)[:2]) != 24:
            return  ["Electoral District Number / Numéro de circonscription",
                    "English Electoral Distict Name / Nom de circonscription anglais",
                    "French Electoral Distict Name / Nom de circonscription français",
                    "Polling Division Number / Numéro de section de vote",
                    "Prefix / Préfixe",
                    "Suffix / Suffixe",
                    "Polling Division Name / Nom de section de vote",
                    "Electors Listed / Électeurs inscrits",
                     "Void / Nul"]
        else:
            return ["Numéro de circonscription / Electoral District Number",
                    "Nom de circonscription anglais / English Electoral Distict Name",
                    "Nom de circonscription français / French Electoral Distict Name ",
                    "Numéro de section de vote / Polling Division Number",
                    "Préfixe / Prefix",
                    "Suffixe / Suffix",
                    "Nom de section de vote / Polling Division Name",
                    "Électeurs inscrits / Electors Listed",
                    "Nul / Void"]
    if report_type == "APD":
        if int(str(fed_num)[:2]) != 24:
            return [ "Electoral Distict Number / Numéro de circonscription",
                     "English Electoral Distict Name / Nom de circonscription anglais",
                     "French Electoral Distict Name / Nom de circonscription français",
                     "Advance Polling District Number / Numéro de bureau de vote par anticipation",
                     "Prefix / Préfixe",
                     "Suffix / Suffixe",
                     "Advance Polling District Name / Nom de bureau de vote par anticipation",
                     "Polling Division Groupings / Groupements des sections de vote",
                     "Total Polling Divisions / Total de sections de vote"
            ]

        else:
            return ["Numéro de circonscription / Electoral Distict Number",
                   "Nom de circonscription anglais / English Electoral Distict Name",
                   "Nom de circonscription français / French Electoral Distict Name",
                   "Numéro de bureau de vote par anticipation / Advance Polling District Number",
                   "Préfixe/ Prefix",
                   "Suffixe/ Suffix",
                   "Nom de bureau de vote par anticipation / Advance Polling District Name",
                   "Groupements des sections de vote / Polling Division Groupings",
                   "Total de sections de vote / Total Polling Divisions"
                   ]
    if report_type == 'MPS':
        if int(str(fed_num)[:2]) != 24:
            return [
                "Electoral District Number / Numéro de circonscription",
                "English Electoral Distict Name / Nom de circonscription anglais",
                "French Electoral Distict Name / Nom de circonscription français",
                "Polling Division Number / Numéro de section de vote",
                "Prefix / Préfixe",
                "Suffix / Suffixe",
                "Total Institutions / Total d'Établissements",
                "Electors Listed / Électeurs inscrits",
                "Advance Polling District Number / Numéro de bureau de vote par anticipation"
            ]
        else:
            return [
                "Numéro de circonscription / Electoral District Number",
                "Nom de circonscription anglais / English Electoral Distict Name",
                "Nom de circonscription français / French Electoral Distict Name",
                "Numéro de section de vote / Polling Division Number",
                "Préfixe / Prefix",
                "Suffixe / Suffix",
                "Total d'Établissements / Total Institutions",
                "Électeurs inscrits / Electors Listed",
                "Numéro de bureau de vote par anticipation / Advance Polling District Number"
        ]
    if report_type == 'PDD':
        if int(str(fed_num)[:2]) != 24:
            return ["Electoral District Number / Numéro de circonscription",
                    "English Electoral Distict Name / Nom de circonscription anglais",
                    "French Electoral Distict Name / Nom de circonscription français",
                    "Polling Division Number / Numéro de section de vote",
                    "Prefix / Préfixe",
                    "Suffix / Suffixe",
                    "Poll Name / Nom de section de vote",
                    "Municipality Name / Nom de municipalité",
                    "Municipality Type / Type de municipalité",
                    "Street Name / Nom de rue",
                    "Street Type / Type de rue",
                    "Street Direction / Direction de rue",
                    "From Feature / Point de départ",
                    "To Feature / Point de terminaison",
                    "From Civic Number / Numéro civique de départ",
                    "To Civic Number / Numéro civique de terminaison",
                    "Side / Côté",
                    "Advance Polling District Number / Numéro de bureau de vote par anticipation"
                    ]
        else:
            return ["Numéro de circonscription / Electoral District Number",
                    "Nom de circonscription anglais / English Electoral Distict Name",
                    "Nom de circonscription français / French Electoral Distict Name",
                    "Numéro de section de vote / Polling Division Number",
                    "Préfixe / Prefix",
                    "Suffixe / Suffix",
                    "Nom de section de vote / Poll Name",
                    "Nom de municipalité / Municipality Name",
                    "Type de municipalité / Municipality Type",
                    "Nom de rue / Street Name",
                    "Type de rue / Street Type",
                    "Direction de rue / Street Direction",
                    "Point de départ / From Feature",
                    "Point de terminaison / To Feature",
                    "Numéro civique de départ / From Civic Number",
                    "Numéro civique de terminaison / To Civic Number",
                    "Côté / Side",
                    "Numéro de bureau de vote par anticipation / Advance Polling District Number"
                    ]
    if report_type == 'DPK':
        if int(str(fed_num)[:2]) != 24:
            return ["Electoral District Number / Numéro de circonscription",
                    "English Electoral Distict Name / Nom de circonscription anglais",
                    "French Electoral Distict Name / Nom de circonscription français",
                    "Street Name / Nom de rue",
                    "Street Type / Type de rue",
                    "Street Direction / Direction de rue",
                    "Municipality Name / Nom de municipalité",
                    "Municipality Type / Type de municipalité",
                    "From Feature / Point de départ",
                    "To Feature / Point de terminaison",
                    "From Civic Number / Numéro civique de départ",
                    "To Civic Number / Numéro civique de terminaison",
                    "Side / Côté",
                    "Polling Division Number / Numéro de section de vote",
                    "Prefix / Préfixe",
                    "Suffix / Suffixe",
                    "Poll Name / Nom de section de vote",
                    "Advance Polling District Number / Numéro de bureau de vote par anticipation"
                    ]
        else:
            return ["Numéro de circonscription / Electoral District Number",
                    "Nom de circonscription anglais / English Electoral Distict Name",
                    "Nom de circonscription français / French Electoral Distict Name",
                    "Nom de rue / Street Name",
                    "Type de rue / Street Type",
                    "Direction de rue / Street Direction",
                    "Nom de municipalité / Municipality Name",
                    "Type de municipalité / Municipality Type",
                    "Point de départ / From Feature",
                    "Point de terminaison / To Feature",
                    "Numéro civique de départ / From Civic Number",
                    "Numéro civique de terminaison / To Civic Number",
                    "Côté / Side",
                    "Numéro de section de vote / Polling Division Number",
                    "Préfixe / Prefix",
                    "Suffixe / Suffix",
                    "Nom de section de vote / Poll Name",
                    "Numéro de bureau de vote par anticipation / Advance Polling District Number"
                    ]
