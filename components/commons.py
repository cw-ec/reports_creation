import logging
import sys
import os
import pandas as pd
from datetime import datetime


def logging_setup(log_dir=".\\") -> logging.getLogger():
    """Sets up logging takes one parameter to set a directory for the output log file"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{datetime.today().strftime('%d-%m-%Y')}_log.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger()


def create_dir(path: str) -> None:
    """Check if directory exists and if it doesn't create it."""
    if not os.path.exists(path):
        os.makedirs(path)


def to_dataframe(to_import: str, sheet_name=0, encoding='UTF-8') -> pd.DataFrame:
    """Import the given path into a pandas dataframe. Returns that pandas dataframe

    to_import = the path to the data to import into the dataframe. Required

    sheet = Name of the sheet to import into a dataframe. Can be integer or text of name (str)

    """

    path_list = os.path.split(to_import)
    f_type = path_list[-1].split('.')[-1]

    if f_type == 'csv':
        return pd.read_csv(to_import, encoding=encoding)
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

def get_prov_from_code(prov_code: int) -> str:
    """Input an ed_code and get the province name in return"""

    # Corrected translations eng/ fre or fre / eng where needed with prov code associations
    prov_dict = {
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

    # Extract the first two numbers of the input ed code to get the prov code
    pr_code = int(str(prov_code)[:2])

    if pr_code in prov_dict:
        return prov_dict[pr_code]
    else:
        raise Exception(f"ED_Code {prov_code} not in province when reduced to {pr_code} not in province dict. Check input")

def get_ed_name_from_code(code: int) -> str:
    """Returns the Fed 343 name for a given ed number"""

    ed_dict = {10001: 'Avalon',
               10002: 'Bonavista—Burin—Trinity',
               10003: 'Coast of Bays—Central—Notre Dame',
               10004: 'Labrador',
               10005: 'Long Range Mountains',
               10006: "St. John's East / St. John's-Est",
               10007: "St. John's South—Mount Pearl / St. John's-Sud—Mount Pearl",
               11001: 'Cardigan',
               11002: 'Charlottetown',
               11003: 'Egmont',
               11004: 'Malpeque',
               12001: 'Cape Breton—Canso',
               12002: 'Central Nova / Nova-Centre',
               12003: 'Cumberland—Colchester',
               12004: 'Dartmouth—Cole Harbour',
               12005: 'Halifax',
               12006: 'Halifax West / Halifax-Ouest',
               12007: 'Kings—Hants',
               12008: 'Sackville—Preston—Chezzetcook',
               12009: 'South Shore—St. Margarets',
               12010: 'Sydney—Victoria',
               12011: 'West Nova / Nova-Ouest',
               13001: 'Acadie—Bathurst',
               13002: 'Beauséjour',
               13003: 'Fredericton',
               13004: 'Fundy Royal',
               13005: 'Madawaska—Restigouche',
               13006: 'Miramichi—Grand Lake',
               13007: 'Moncton—Riverview—Dieppe',
               13008: 'New Brunswick Southwest / Nouveau-Brunswick-Sud-Ouest',
               13009: 'Saint John—Rothesay',
               13010: 'Tobique—Mactaquac',
               24001: 'Abitibi—Baie-James—Nunavik—Eeyou',
               24002: 'Abitibi—Témiscamingue',
               24003: 'Ahuntsic-Cartierville',
               24004: 'Alfred-Pellan',
               24005: 'Argenteuil—La Petite-Nation',
               24006: 'Avignon—La Mitis—Matane—Matapédia',
               24007: 'Beauce',
               24008: 'Beauport—Limoilou',
               24009: 'Bécancour—Nicolet—Saurel',
               24010: 'Bellechasse—Les Etchemins—Lévis',
               24011: 'Beloeil—Chambly',
               24012: 'Berthier—Maskinongé',
               24013: 'Thérèse-De Blainville',
               24014: 'Pierre-Boucher—Les Patriotes—Verchères',
               24015: 'Bourassa',
               24016: 'Brome—Missisquoi',
               24017: 'Brossard—Saint-Lambert',
               24018: 'Rimouski-Neigette—Témiscouata—Les Basques',
               24019: 'Charlesbourg—Haute-Saint-Charles',
               24020: "Beauport-Côte-de-Beaupré-Île d'Orléans-Charlevoix",
               24021: 'Châteauguay—Lacolle',
               24022: 'Chicoutimi—Le Fjord',
               24023: 'Compton—Stanstead',
               24024: 'Dorval—Lachine—LaSalle',
               24025: 'Drummond',
               24026: 'Gaspésie—Les Îles-de-la-Madeleine',
               24027: 'Gatineau',
               24028: 'Hochelaga',
               24029: 'Honoré-Mercier',
               24030: 'Hull—Aylmer',
               24031: 'Joliette',
               24032: 'Jonquière',
               24033: "La Pointe-de-l'Île",
               24034: 'La Prairie',
               24035: 'Lac-Saint-Jean',
               24036: 'Lac-Saint-Louis',
               24037: 'LaSalle—Émard—Verdun',
               24038: 'Laurentides—Labelle',
               24039: 'Laurier—Sainte-Marie',
               24040: 'Laval—Les Îles',
               24041: 'Longueuil—Charles-LeMoyne',
               24042: 'Lévis—Lotbinière',
               24043: 'Longueuil—Saint-Hubert',
               24044: 'Louis-Hébert',
               24045: 'Louis-Saint-Laurent',
               24046: 'Manicouagan',
               24047: "Mégantic—L'Érable",
               24048: 'Mirabel',
               24049: 'Montarville',
               24050: 'Montcalm',
               24051: "Montmagny—L'Islet—Kamouraska—Rivière-du-Loup",
               24052: 'Mont-Royal / Mount Royal',
               24053: 'Notre-Dame-de-Grâce—Westmount',
               24054: 'Outremont',
               24055: 'Papineau',
               24056: 'Pierrefonds—Dollard',
               24057: 'Pontiac',
               24058: 'Portneuf—Jacques-Cartier',
               24059: 'Québec',
               4060: 'Repentigny',
               24061: 'Richmond—Arthabaska',
               24062: 'Rivière-des-Mille-Îles',
               24063: 'Rivière-du-Nord',
               24064: 'Rosemont—La Petite-Patrie',
               24065: 'Marc-Aurèle-Fortin',
               24066: 'Saint-Hyacinthe—Bagot',
               24067: 'Saint-Jean',
               24068: 'Saint-Laurent',
               24069: 'Saint-Léonard—Saint-Michel',
               24070: 'Saint-Maurice—Champlain', 24071: 'Salaberry—Suroît', 24072: 'Shefford', 24073: 'Sherbrooke',
               24074: 'Vaudreuil—Soulanges', 24075: 'Terrebonne', 24076: 'Trois-Rivières',
               24077: 'Ville-Marie—Le Sud-Ouest—Île-des-Soeurs', 24078: 'Vimy', 35001: 'Ajax',
               35002: 'Algoma—Manitoulin—Kapuskasing', 35003: 'Aurora—Oak Ridges—Richmond Hill',
               35004: 'Barrie—Innisfil',
               35005: 'Barrie—Springwater—Oro-Medonte', 35006: 'Bay of Quinte / Baie de Quinte',
               35007: 'Beaches—East York',
               35008: 'Brampton Centre / Brampton-Centre', 35009: 'Brampton East / Brampton-Est',
               35010: 'Brampton North / Brampton-Nord', 35011: 'Brampton South / Brampton-Sud',
               35012: 'Brampton West / Brampton-Ouest', 35013: 'Brantford—Brant', 35014: 'Bruce—Grey—Owen Sound',
               35015: 'Burlington', 35016: 'Cambridge', 35017: 'Chatham-Kent—Leamington', 35018: 'Davenport',
               35019: 'Don Valley East / Don Valley-Est', 35020: 'Don Valley North / Don Valley-Nord',
               35021: 'Don Valley West / Don Valley-Ouest', 35022: 'Dufferin—Caledon', 35023: 'Durham',
               35024: 'Eglinton—Lawrence', 35025: 'Elgin—Middlesex—London', 35026: 'Essex',
               35027: 'Etobicoke Centre / Etobicoke-Centre', 35028: 'Etobicoke—Lakeshore',
               35029: 'Etobicoke North / Etobicoke-Nord', 35030: 'Flamborough—Glanbrook',
               35031: 'Glengarry—Prescott—Russell',
               35032: 'Guelph', 35033: 'Haldimand—Norfolk', 35034: 'Haliburton—Kawartha Lakes—Brock',
               35035: 'Hamilton Centre / Hamilton-Centre',
               35036: 'Hamilton East—Stoney Creek / Hamilton-Est—Stoney Creek',
               35037: 'Hamilton Mountain', 35038: 'Hamilton West—Ancaster—Dundas / Hamilton-Ouest—Ancaster—Dundas',
               35039: 'Hastings—Lennox and Addington', 35040: 'Huron—Bruce', 35041: 'Kanata—Carleton',
               35042: 'Kenora',
               35043: 'King—Vaughan', 35044: 'Kingston and the Islands / Kingston et les Îles',
               35045: 'Kitchener Centre / Kitchener-Centre', 35046: 'Kitchener—Conestoga',
               35047: 'Kitchener South—Hespeler / Kitchener-Sud—Hespeler', 35048: 'Lambton—Kent—Middlesex',
               35049: 'Lanark—Frontenac—Kingston',
               35050: 'Leeds-Grenville-Thousand Islands and Rideau Lakes / Leeds-Grenville-Thousand Islands et Rideau Lakes',
               35051: 'London—Fanshawe', 35052: 'London North Centre / London-Centre-Nord',
               35053: 'London West / London-Ouest',
               35054: 'Markham—Stouffville', 35055: 'Markham—Thornhill', 35056: 'Markham—Unionville',
               35057: 'Milton',
               35058: 'Mississauga Centre / Mississauga-Centre',
               35059: 'Mississauga East—Cooksville / Mississauga-Est—Cooksville', 35060: 'Mississauga—Erin Mills',
               35061: 'Mississauga—Lakeshore', 35062: 'Mississauga—Malton', 35063: 'Mississauga—Streetsville',
               35064: 'Nepean',
               35065: 'Newmarket—Aurora', 35066: 'Niagara Centre / Niagara-Centre', 35067: 'Niagara Falls',
               35068: 'Niagara West / Niagara-Ouest', 35069: 'Nickel Belt', 35070: 'Nipissing—Timiskaming',
               35071: 'Northumberland—Peterborough South / Northumberland—Peterborough-Sud', 35072: 'Oakville',
               35073: 'Oakville North—Burlington / Oakville-Nord—Burlington', 35074: 'Oshawa',
               35075: 'Ottawa Centre / Ottawa-Centre', 35076: 'Orléans', 35077: 'Ottawa South / Ottawa-Sud',
               35078: 'Ottawa—Vanier', 35079: 'Ottawa West—Nepean / Ottawa-Ouest—Nepean', 35080: 'Oxford',
               35081: 'Parkdale—High Park', 35082: 'Parry Sound—Muskoka', 35083: 'Perth—Wellington',
               35084: 'Peterborough—Kawartha', 35085: 'Pickering—Uxbridge', 35086: 'Renfrew—Nipissing—Pembroke',
               35087: 'Richmond Hill', 35088: 'Carleton', 35089: 'St. Catharines', 35090: "Toronto—St. Paul's",
               35091: 'Sarnia—Lambton', 35092: 'Sault Ste. Marie', 35093: 'Scarborough—Agincourt',
               35094: 'Scarborough Centre / Scarborough-Centre', 35095: 'Scarborough—Guildwood',
               35096: 'Scarborough North / Scarborough-Nord', 35097: 'Scarborough—Rouge Park',
               35098: 'Scarborough Southwest / Scarborough-Sud-Ouest', 35099: 'Simcoe—Grey',
               35100: 'Simcoe North / Simcoe-Nord', 35101: 'Spadina—Fort York',
               35102: 'Stormont—Dundas—South Glengarry',
               35103: 'Sudbury', 35104: 'Thornhill', 35105: 'Thunder Bay—Rainy River',
               35106: 'Thunder Bay—Superior North / Thunder Bay—Supérieur-Nord',
               35107: 'Timmins—James Bay / Timmins—Baie James', 35108: 'Toronto Centre / Toronto-Centre',
               35109: 'Toronto—Danforth', 35110: 'University—Rosedale', 35111: 'Vaughan—Woodbridge',
               35112: 'Waterloo',
               35113: 'Wellington—Halton Hills', 35114: 'Whitby', 35115: 'Willowdale', 35116: 'Windsor—Tecumseh',
               35117: 'Windsor West / Windsor-Ouest', 35118: 'York Centre / York-Centre', 35119: 'York—Simcoe',
               35120: 'York South—Weston / York-Sud—Weston', 35121: 'Humber River—Black Creek',
               46001: 'Brandon—Souris',
               46002: 'Charleswood—St. James—Assiniboia—Headingley', 46003: 'Churchill—Keewatinook Aski',
               46004: 'Dauphin—Swan River—Neepawa', 46005: 'Elmwood—Transcona', 46006: 'Kildonan—St. Paul',
               46007: 'Portage—Lisgar', 46008: 'Provencher',
               46009: 'Saint Boniface—Saint Vital / Saint-Boniface—Saint-Vital',
               46010: 'Selkirk—Interlake—Eastman', 46011: 'Winnipeg Centre / Winnipeg-Centre',
               46012: 'Winnipeg North / Winnipeg-Nord', 46013: 'Winnipeg South / Winnipeg-Sud',
               46014: 'Winnipeg South Centre / Winnipeg-Centre-Sud', 47001: 'Battlefords—Lloydminster',
               47002: 'Cypress Hills—Grasslands',
               47003: 'Desnethé—Missinippi—Churchill River / Desnethé—Missinippi—Rivière Churchill',
               47004: 'Carlton Trail—Eagle Creek / Sentier Carlton—Eagle Creek',
               47005: 'Moose Jaw—Lake Centre—Lanigan',
               47006: 'Prince Albert', 47007: 'Regina—Lewvan', 47008: "Regina—Qu'Appelle", 47009: 'Regina—Wascana',
               47010: 'Saskatoon—Grasswood', 47011: 'Saskatoon—University',
               47012: 'Saskatoon West / Saskatoon-Ouest',
               47013: 'Souris—Moose Mountain', 47014: 'Yorkton—Melville', 48001: 'Banff—Airdrie',
               48002: 'Battle River—Crowfoot', 48003: 'Bow River', 48004: 'Calgary Centre / Calgary-Centre',
               48005: 'Calgary Confederation', 48006: 'Calgary Forest Lawn', 48007: 'Calgary Heritage',
               48008: 'Calgary Midnapore', 48009: 'Calgary Nose Hill', 48010: 'Calgary Rocky Ridge',
               48011: 'Calgary Shepard',
               48012: 'Calgary Signal Hill', 48013: 'Calgary Skyview', 48014: 'Edmonton Centre / Edmonton-Centre',
               48015: 'Edmonton Griesbach', 48016: 'Edmonton Manning', 48017: 'Edmonton Mill Woods',
               48018: 'Edmonton Riverbend', 48019: 'Edmonton Strathcona', 48020: 'Edmonton West / Edmonton-Ouest',
               48021: 'Edmonton—Wetaskiwin', 48022: 'Foothills', 48023: 'Fort McMurray—Cold Lake',
               48024: 'Grande Prairie—Mackenzie', 48025: 'Lakeland', 48026: 'Lethbridge',
               48027: 'Medicine Hat—Cardston—Warner',
               48028: 'Peace River—Westlock', 48029: 'Red Deer—Mountain View', 48030: 'Red Deer—Lacombe',
               48031: 'St. Albert—Edmonton', 48032: 'Sherwood Park—Fort Saskatchewan',
               48033: 'Sturgeon River—Parkland',
               48034: 'Yellowhead', 59001: 'Abbotsford', 59002: 'Burnaby North—Seymour / Burnaby-Nord—Seymour',
               59003: 'Burnaby South / Burnaby-Sud', 59004: 'Cariboo—Prince George',
               59005: 'Central Okanagan—Similkameen—Nicola', 59006: 'Chilliwack—Hope',
               59007: 'Cloverdale—Langley City',
               59008: 'Coquitlam—Port Coquitlam', 59009: 'Courtenay—Alberni', 59010: 'Cowichan—Malahat—Langford',
               59011: 'Delta', 59012: 'Fleetwood—Port Kells', 59013: 'Kamloops—Thompson—Cariboo',
               59014: 'Kelowna—Lake Country',
               59015: 'Kootenay—Columbia', 59016: 'Langley—Aldergrove', 59017: 'Mission—Matsqui—Fraser Canyon',
               59018: 'Nanaimo—Ladysmith', 59019: 'New Westminster—Burnaby', 59020: 'North Okanagan—Shuswap',
               59021: 'North Vancouver', 59022: 'Pitt Meadows—Maple Ridge', 59023: 'Port Moody—Coquitlam',
               59024: 'Prince George—Peace River—Northern Rockies', 59025: 'Richmond Centre / Richmond-Centre',
               59026: 'Esquimalt—Saanich—Sooke', 59027: 'Saanich—Gulf Islands', 59028: 'Skeena—Bulkley Valley',
               59029: 'South Okanagan—West Kootenay / Okanagan-Sud—Kootenay-Ouest',
               59030: 'South Surrey—White Rock / Surrey-Sud—White Rock',
               59031: 'Steveston—Richmond East / Steveston—Richmond-Est', 59032: 'Surrey Centre / Surrey-Centre',
               59033: 'Surrey—Newton', 59034: 'Vancouver Centre / Vancouver-Centre',
               59035: 'Vancouver East / Vancouver-Est',
               59036: 'Vancouver Granville', 59037: 'North Island—Powell River', 59038: 'Vancouver Kingsway',
               59039: 'Vancouver Quadra', 59040: 'Vancouver South / Vancouver-Sud', 59041: 'Victoria',
               59042: 'West Vancouver—Sunshine Coast—Sea to Sky Country', 60001: 'Yukon',
               61001: 'Northwest Territories / Territoires du Nord-Ouest', 62001: 'Nunavut'}

    if code in ed_dict:
        return ed_dict[code]
    else:
        raise Exception(f"ED Code {code} does not exist in the 343 dictionary.")
