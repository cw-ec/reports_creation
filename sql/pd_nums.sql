--This query shows the information for every polling division belonging to a given ELCTRL_EVENT_ID.
--It connects to the CDB.

--Normally, this query would connect to:
--REDIST.RDSTRBTN_CRNT_IND = 'Y'
--and EDEE.CRNT_IND ='Y'
--and EDEE.ELCTRL_EVENT_ID  = '99'
--Which is the normal RLS data.

--Here, the sql pointed to:
--EDEE.ELCTRL_EVENT_ID  = '88'
--This is because the data hadn't been finalized in RLS when the data was queried.



SELECT
--REDISTRIBUTION INFORMATION
-- The 2023 Representation Order RDSTRBTN_ID is 6.
-- The RDSTRBTN_CRNT_IND is "Y" for the most recent, and active data.
  REDIST.RDSTRBTN_ID, REDIST.RDSTRBTN_YEAR, REDIST.RDSTRBTN_CRNT_IND,



 --PROVINCE INFORMATION
   EDistrict.PRVNC_ID,

-- If the French and English province names are the same, PRVNC_NAMEE gets listed.
-- If the French and English province names are different, PRVNC_NAMEE / PRVNC_NAMEF gets listed for the EDs outside of Quebec, and PRVNC_NAMEF / PRVNC_NAMEE gets listed for the EDs inside of Quebec.
 UPPER(CASE
    WHEN PROV.PRVNC_NAMEE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and PROV.PRVNC_NAMEE <> PROV.PRVNC_NAMEF THEN PROV.PRVNC_NAMEF ||' / '|| PROV.PRVNC_NAMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and PROV.PRVNC_NAMEE <> PROV.PRVNC_NAMEF THEN PROV.PRVNC_NAMEE ||' / '|| PROV.PRVNC_NAMEF
        ELSE PROV.PRVNC_NAMEE
      END
    WHEN PROV.PRVNC_NAMEE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and PROV.PRVNC_NAMEE <> PROV.PRVNC_NAMEF THEN PROV.PRVNC_NAMEF ||' / '|| PROV.PRVNC_NAMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and PROV.PRVNC_NAMEE <> PROV.PRVNC_NAMEF THEN PROV.PRVNC_NAMEE ||' / '|| PROV.PRVNC_NAMEF
        ELSE PROV.PRVNC_NAMEE
      END
  END) AS PRVNC_NAME_BIL,



--ED INFORMATION
EDistrict.ED_CODE,
-- ED 24020 needs a text replacement. Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata needs to be changed to Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata.
REPLACE (EDistrict.ED_NAMEE, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata') ED_NAMEE,
REPLACE (EDistrict.ED_NAMEF, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata') ED_NAMEF,
-- If the French and English ED names are the same, ED_NAMEE gets listed.
-- If the French and English ED names are different, ED_NAMEE / ED_NAMEF gets listed for the EDs outside of Quebec, and ED_NAMEF / ED_NAMEE gets listed for the EDs inside of Quebec.
CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN REPLACE (EDistrict.ED_NAMEF, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata') ||' / '|| REPLACE (EDistrict.ED_NAMEE, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata')
    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN REPLACE (EDistrict.ED_NAMEE, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata') ||' / '|| REPLACE (EDistrict.ED_NAMEF, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata')
    ELSE REPLACE (EDistrict.ED_NAMEE, 'Côte-du-Sud-Rivière-du-Loup-Kataskomiq-Témiscouata', 'Côte-du-Sud--Rivière-du-Loup--Kataskomiq--Témiscouata')
  END AS ED_NAME_BIL,


--CASE
--  WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN EDistrict.ED_NAMEF ||' / '|| EDistrict.ED_NAMEE
--  WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN EDistrict.ED_NAMEE ||' / '|| EDistrict.ED_NAMEF
--  ELSE EDistrict.ED_NAMEE
--END AS ED_NAME_BIL,

--This is old code for replacing "--" with an en-dash.
--Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.
-- CASE
--    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN (REPLACE (EDistrict.ED_NAMEF, '--', '—')) ||' / '|| (REPLACE (EDistrict.ED_NAMEE, '--', '—'))
 --   WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN (REPLACE (EDistrict.ED_NAMEE, '--', '—')) ||' / '|| (REPLACE (EDistrict.ED_NAMEF, '--', '—'))
 --   ELSE (REPLACE (EDistrict.ED_NAMEE, '--', '—'))
 -- END AS ED_NAME_BIL,


--Other ED information.
  EDistrict.ED_ID, EDEE.ELCTRL_EVENT_ID,
  EDEE.ED_ELCTRL_EVENT_ID, EDEE.CRNT_IND, EDEE.EVENT_ED_CODE,



--ORD PD INFORMATION
-- This is akin to the full EMRP number that shows both the PD number and the PD suffix.
  CONCAT (CONCAT (PLL.PD_NBR, '-'), PLL.PD_NBR_SFX ) FULL_PD_NBR,
-- More ORD PD Information.
 PLL.PD_NBR, PLL.PD_NBR_SFX, PLL.PD_ID, PLL.VOID_IND, MPP.MOBILE_POLL_STN_ID,

--Now derived from a table derived by Jessica Lachance. ELECTOR_COUNT_BY_PD_ID_20240423.xlsx
 EA_PEC.ELECTOR_COUNT ELECTORS_LISTED,


--ORD PD Name
--PLL.POLL_NAME_ID,
  PNAME.POLL_NAME POLL_NAME_FIXED,

--This is old code for replacing "--" with an en-dash.
--REPLACE (PNAME.POLL_NAME, '--', '—') AS POLL_NAME_FIXED,
--Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.

--More ORD PD Information
 PLL.SINGLE_BLDG_IND,
 PLL.MOBILE_POLL_IND,
--PLL.STATION_IND, PLL.DIVISION_IND,
  PLL.URBAN_RURAL_IND,



 --ADV PD INFORMATION
  PLL.ADVANCE_POLL_IND,

-- This is akin to the full EMRP number that shows both the PD number and the PD suffix.
 CONCAT (CONCAT (PLL2.PD_NBR, '-'), PLL2.PD_NBR_SFX ) FULL_ADV_PD_NBR,

 --More ADV PD Number and Suffix
  PLL2.PD_NBR ADV_PD_NBR, PLL2.PD_NBR_SFX ADV_PD_NBR_SFX,

--Related Poll Table: This is used to establish the ADV PD Nname.
  PARENT_PD_ID ADV_PD_ID,
--CHILD_PD_ID CHILD_ORD_PD_ID,

--ADV PD Name
--ADV Name
--PNAME2.POLL_NAME_ID ADV_POLL_NAME_ID,
  PNAME2.POLL_NAME ADV_POLL_NAME_FIXED,
--REPLACE (PNAME2.POLL_NAME, '--', '—') AS ADV_POLL_NAME_FIXED
--Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.



--ELECTORS LISTED VALUES.
--Now derived from a table derived by Jessica Lachance. ELECTOR_COUNT_BY_PD_ID_20240423.xlsx
 EA_PEC.ELECTOR_COUNT



--TABLE JOINS
 FROM ecdba.REDISTRIBUTION REDIST
  LEFT JOIN ecdba.ELECTORAL_DISTRICT EDistrict on
    REDIST.RDSTRBTN_ID = EDistrict.RDSTRBTN_ID
  LEFT JOIN ecdba.PROVINCE PROV on
    EDistrict.PRVNC_ID= PROV.PROVINCE_ID
  LEFT JOIN ECDBA.ED_ELCTRL_EVENT EDEE on
    EDistrict.ED_ID = EDEE.ED_ID
  LEFT JOIN ECDBA.POLL PLL on
    EDEE.ED_ELCTRL_EVENT_ID = PLL.ED_ELCTRL_EVENT_ID
  LEFT JOIN ECDBA.POLL_NAME PNAME on
    PLL.POLL_NAME_ID = PNAME.POLL_NAME_ID
  LEFT JOIN ECDBA.RELATED_POLL RP on
    PLL.PD_ID = RP.CHILD_PD_ID
  LEFT JOIN ECDBA.POLL PLL2 on
    RP.PARENT_PD_ID = PLL2.PD_ID
  LEFT JOIN ECDBA.POLL_NAME PNAME2 on
    PLL2.POLL_NAME_ID = PNAME2.POLL_NAME_ID

    --JOIN MOBILE_POLL_PLACE for MOB
  LEFT JOIN MOBILE_POLL_PLACE MPP on
    PLL.PD_ID = MPP.PD_ID

    --JOIN PD ELECTOR COUNT
 LEFT JOIN EGD_ADMIN.PD_ELECTOR_COUNT EA_PEC on
PLL.PD_ID = EA_PEC.PD_ID and MPP.MOBILE_POLL_STN_ID  = EA_PEC.MOBILE_POLL_STN_ID
--Now derived from a table derived by Jessica Lachance. ELECTOR_COUNT_BY_PD_ID_20240423.xlsx



--WHERE CLAUSES
--For 2023 Redistribution, we used ELCTRL_EVENT_ID  = '88'.
-- This will change to REDIST.RDSTRBTN_CRNT_IND = 'Y' in RLS once the data is finalized.
-- This will change to EDEE.ELCTRL_EVENT_ID  = '99' in RLS once the data is finalized.
-- This will change to EDEE.CRNT_IND ='Y' in RLS once the data is finalized.

where
-- REDIST.RDSTRBTN_CRNT_IND = 'Y'
-- and EDEE.CRNT_IND ='Y'
EDEE.ELCTRL_EVENT_ID  = '88'
and PLL.ADVANCE_POLL_IND = 'N'
-- and PLL.VOID_IND = 'N'
and PLL.PD_NBR <> 999
-- and PLL.PD_NBR > 500
-- and PLL.PD_NBR < 600
and EDistrict.ED_CODE in ED_LIST_HERE


order by
  EDEE.EVENT_ED_CODE, PLL.PD_NBR, PLL.PD_NBR_SFX
