--This query shows the information for every polling division belonging to a given ELCTRL_EVENT_ID. It also shows the STRM information that is attached to said polling divisions. This query will be joined with the PD_Numbers - SIMPLIFIED.sql query in the PYTHON scripts.
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
  UPPER (CASE
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
  PLL.PD_NBR, PLL.PD_NBR_SFX, PLL.PD_ID, MPP.MOBILE_POLL_STN_ID,



--STRM INFORMATION
--It is uncertain if IT-GIS has a mechanism in place from DMT to replace the STRM values in the CDB once the geographic dataset gets updated.
  STRM.TWNSHIP, STRM.RNGE, STRM.MRDN, STRM.SECTION, STRM.TRM_DESCE, STRM.TRM_DESCF, STRM.LAST_UPD_DT



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

--JOIN MOBILE_POLL_PLACE for MOB
  LEFT JOIN SITES_ADMIN.MOBILE_POLL_PLACE MPP on
    PLL.PD_ID = MPP.PD_ID

--JOIN STRMs
     LEFT JOIN ECDBA.TWNSHP_RNGE_MRDN STRM  on
     PLL.PD_ID = STRM.PD_ID



--WHERE CLAUSES
--For 2023 Redistribution, we used ELCTRL_EVENT_ID  = '88'.
-- This will change to REDIST.RDSTRBTN_CRNT_IND = 'Y' in RLS once the data is finalized.
-- This will change to EDEE.ELCTRL_EVENT_ID  = '99' in RLS once the data is finalized.
-- This will change to EDEE.CRNT_IND ='Y' in RLS once the data is finalized.

where
--  REDIST.RDSTRBTN_CRNT_IND = 'Y'
--  and EDEE.CRNT_IND ='Y'
EDEE.ELCTRL_EVENT_ID = '88'
  and PLL.ADVANCE_POLL_IND = 'N'
  and PLL.VOID_IND = 'N'
  and PLL.PD_NBR <> 999
  and EDistrict.ED_CODE in ED_LIST_HERE

order by
  EDEE.EVENT_ED_CODE, PLL.PD_NBR, PLL.PD_NBR_SFX
