--This query shows the PDADS (Polling Division Address Descriptions System) street segment information for every polling division belonging to a given ELCTRL_EVENT_ID.
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
-- If the French and English province names are the same, PRVNC_NAMEE gets listed.
-- If the French and English province names are different, PRVNC_NAMEE / PRVNC_NAMEF gets listed for the EDs outside of Quebec, and PRVNC_NAMEF / PRVNC_NAMEE gets listed for the EDs inside of Quebec.
  EDistrict.PRVNC_ID,
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
  PLL.PD_NBR, PLL.PD_NBR_SFX,

-- More ORD PD Information.
 --PLL.PD_ID,

--ORD PD Name
--PLL.POLL_NAME_ID,
-- PNAME.POLL_NAME,
PNAME.POLL_NAME AS POLL_NAME_FIXED, PLL.VOID_IND,


 --More ORD PD Information
PLL.SINGLE_BLDG_IND, PLL.MOBILE_POLL_IND,
--PLL.STATION_IND, PLL.DIVISION_IND,
PLL.URBAN_RURAL_IND,



 --ADV PD INFORMATION
  --ADV Number
  PLL.ADVANCE_POLL_IND,
  CONCAT (CONCAT (PLL2.PD_NBR, '-'), PLL2.PD_NBR_SFX ) FULL_ADV_PD_NBR,
   PLL2.PD_NBR ADV_PD_NBR, PLL2.PD_NBR_SFX ADV_PD_NBR_SFX,


--Related Poll Table: This is used to establish the ADV PD Nname.
--Related Poll Table
--PARENT_PD_ID ADV_PD_ID, CHILD_PD_ID CHILD_ORD_PD_ID,


--ADV PD Name
--ADV Name
  PNAME2.POLL_NAME ADV_POLL_NAME_FIXED,
  --REPLACE (PNAME2.POLL_NAME, '--', '—') AS ADV_POLL_NAME_FIXED,
 --Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.



--SITE INFORMATION
--None for right now
 --



--PDSS CSD INFORMATION
 --PDSS.PD_SEGMENT_ID,
 --ECSTR.PLACE_ID,
  ECPL.PLACE_NAME, CSDTP1.CSD_TYP_DESCE, CSDTP1.CSD_TYP_DESCF,

--Accounts for CSD type description differences between English and French.
  CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      CASE
        WHEN CSDTP1.CSD_TYP_DESCE <> CSDTP1.CSD_TYP_DESCF THEN CSDTP1.CSD_TYP_DESCF ||' / '|| CSDTP1.CSD_TYP_DESCE
        ELSE CSDTP1.CSD_TYP_DESCF
      END
    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) then
      CASE
        WHEN CSDTP1.CSD_TYP_DESCE <> CSDTP1.CSD_TYP_DESCF THEN CSDTP1.CSD_TYP_DESCE ||' / '|| CSDTP1.CSD_TYP_DESCF
        ELSE CSDTP1.CSD_TYP_DESCE
      END
  END AS CSD_TYP_DESC_BIL, CSDTP1.CSD_TYP_ABBRE CSD_TYP_ABBR_BI,

--FULL PLACE NAME
--Accounts for differences between English and French.
 ECPL.PLACE_NAME ||''||  CASE
    WHEN ECPL.PLACE_NAME is not null and EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      CASE
       WHEN  CSDTP1.CSD_TYP_DESCE is null and CSDTP1.CSD_TYP_DESCF is not null THEN ', '|| CSDTP1.CSD_TYP_DESCF
       WHEN  CSDTP1.CSD_TYP_DESCF is null and CSDTP1.CSD_TYP_DESCE is not null THEN ', '|| CSDTP1.CSD_TYP_DESCE
       WHEN  CSDTP1.CSD_TYP_DESCE is null and CSDTP1.CSD_TYP_DESCF is null THEN ''
        WHEN CSDTP1.CSD_TYP_DESCE is not null and CSDTP1.CSD_TYP_DESCF is not null  and CSDTP1.CSD_TYP_DESCE <> CSDTP1.CSD_TYP_DESCF   THEN ', '|| CSDTP1.CSD_TYP_DESCF ||' / '|| CSDTP1.CSD_TYP_DESCE
          ELSE ', '||CSDTP1.CSD_TYP_DESCF
      END
    WHEN ECPL.PLACE_NAME is not null and (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) then
      CASE
       WHEN  CSDTP1.CSD_TYP_DESCE is null and CSDTP1.CSD_TYP_DESCF is not null THEN ', '|| CSDTP1.CSD_TYP_DESCF
       WHEN  CSDTP1.CSD_TYP_DESCF is null and CSDTP1.CSD_TYP_DESCE is not null THEN ', '|| CSDTP1.CSD_TYP_DESCE
       WHEN  CSDTP1.CSD_TYP_DESCE is null and CSDTP1.CSD_TYP_DESCF is null THEN ''
        WHEN CSDTP1.CSD_TYP_DESCE is not null and CSDTP1.CSD_TYP_DESCF is not null  and CSDTP1.CSD_TYP_DESCE <> CSDTP1.CSD_TYP_DESCF   THEN ', '|| CSDTP1.CSD_TYP_DESCE ||' / '|| CSDTP1.CSD_TYP_DESCF
          ELSE ', '||CSDTP1.CSD_TYP_DESCE
      END
  END
   AS FULL_PLACE_NAME,


  --DEACTIVATED CSD_TYP_ABBRF,
  --CODE for isolating CSD_TYP_ABBR
  -- CASE
  -- WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
  -- CASE
  --WHEN CSDTP1.CSD_TYP_ABBRE <> CSDTP1.CSD_TYP_ABBRF THEN CSDTP1.CSD_TYP_ABBRF ||' / '|| CSDTP1.CSD_TYP_ABBRE
  --ELSE CSDTP1.CSD_TYP_ABBRF
  --END
  --WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) then
  --CASE
  --WHEN CSDTP1.CSD_TYP_ABBRE <> CSDTP1.CSD_TYP_ABBRF THEN CSDTP1.CSD_TYP_ABBRE ||' / '|| CSDTP1.CSD_TYP_ABBRF
  --ELSE CSDTP1.CSD_TYP_ABBRE
  --END
  --END AS CSD_TYP_ABBR_BIL,
  --



--PDSS STREET INFORMATION
--DEACTIVATED PDSS.STREET_ID,
  ECSTR.ST_NME, ECSTR.ST_TYP_CDE,

--These street types must be corrected for EDs inside Quebec to create English street types, so that RUE, AV and BOUL get converted to ST, AVE and BLVD.
    CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
     REPLACE ( REPLACE (REPLACE (ECSTR.ST_TYP_CDE,'RUE', 'ST'), 'AV', 'AVE'),'BOUL', 'BLVD')
     else ECSTR.ST_TYP_CDE
    END ST_TYP_CDE_ENG,

--These street types must be corrected for EDs outside Quebec to create French street types, so that ST, AVE and BLVD get converted to RUE, AV and BOUL.
     CASE
    WHEN EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999 then
      REPLACE ( REPLACE (REPLACE (ECSTR.ST_TYP_CDE,'ST', 'RUE'),'AVE', 'AV'),'BLVD', 'BOUL')
     else ECSTR.ST_TYP_CDE
    END ST_TYP_CDE_FRE,


ECSTR.ST_DRCTN_CDE,

--These street direction codes must be corrected for EDs inside Quebec to create English street direction codes, so that O, NO and SO get converted to W, NW and SW.
  RTRIM(CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      REPLACE ( REPLACE (REPLACE (ECSTR.ST_DRCTN_CDE,'O', 'W'),'NO', 'NW'),'SO', 'SW')
     else ECSTR.ST_DRCTN_CDE
    END) ST_DRCTN_CDE_ENG,

--These street direction codes must be corrected for EDs outside Quebec to create French street direction codes, so that W, NW and SW get converted to O, NO and SO.
    RTRIM (CASE
    WHEN EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999 then
     REPLACE ( REPLACE (REPLACE (ECSTR.ST_DRCTN_CDE,'W', 'O'),'NW', 'NO'),'SW', 'SO')
     else ECSTR.ST_DRCTN_CDE
    END) ST_DRCTN_CDE_FRE,


(ECSTR.ST_NME||' '|| RTRIM(ECSTR.ST_TYP_CDE)||' '|| ECSTR.ST_DRCTN_CDE) as STREET_NME_FULL,

--A FULL, CONVERTED ENGLISH STREET NAME WITH STREET TYPE AND STREET DIRECTION CODE.
--These street types must be corrected for EDs inside Quebec to create English street types, so that RUE, AV and BOUL get converted to ST, AVE and BLVD.
--These street direction codes must be corrected for EDs inside Quebec to create English street direction codes, so that O, NO and SO get converted to W, NW and SW.
(ECSTR.ST_NME||' '|| RTRIM( CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
     REPLACE ( REPLACE (REPLACE (ECSTR.ST_TYP_CDE,'RUE', 'ST'), 'AV', 'AVE'),'BOUL', 'BLVD')
     else ECSTR.ST_TYP_CDE
    END)||' '|| (RTRIM(CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      REPLACE ( REPLACE (REPLACE (ECSTR.ST_DRCTN_CDE,'O', 'W'),'NO', 'NW'),'SO', 'SW')
     else ECSTR.ST_DRCTN_CDE
    END))) as STREET_NME_FULL_ENG,


--A FULL, CONVERTED FRENCH STREET NAME WITH STREET TYPE AND STREET DIRECTION CODE.
--These street types must be corrected for EDs outside Quebec to create French street types, so that ST, AVE and BLVD get converted to RUE, AV and BOUL.
--These street direction codes must be corrected for EDs outside Quebec to create French street direction codes, so that W, NW and SW get converted to O, NO and SO.
  (ECSTR.ST_NME||' '|| RTRIM(  CASE
    WHEN EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999 then
      REPLACE ( REPLACE (REPLACE (ECSTR.ST_TYP_CDE,'ST', 'RUE'),'AVE', 'AV'),'BLVD', 'BOUL')
     else ECSTR.ST_TYP_CDE
    END)||' '|| (RTRIM(CASE
    WHEN EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999 then
     REPLACE ( REPLACE (REPLACE (ECSTR.ST_DRCTN_CDE,'W', 'O'),'NW', 'NO'),'SW', 'SO')
     else ECSTR.ST_DRCTN_CDE
    END))) as STREET_NME_FULL_FRE,


--Used for sorting street names.
ECSTR.ST_PARSED_NAME,



--DEACTIVATED PDSS.FEATURE_ID,



--FROM-TO CIVIC NUMBERS

--FROM Civic numbers.
--NOTE: SBPDs and MOBs use a different logic than ORD PDs.
CASE WHEN (PLL.SINGLE_BLDG_IND = 'Y' or PLL.MOBILE_POLL_IND = 'Y') and PDSS.FROM_ST_ADR_NBR is null THEN PDSS.TO_ST_ADR_NBR
  --WHEN (PLL.SINGLE_BLDG_IND = 'N' AND PLL.MOBILE_POLL_IND = 'N') and PDSS.FROM_ST_ADR_NBR is null THEN "------"
ELSE  PDSS.FROM_ST_ADR_NBR
END AS FROM_CIV_NUM,

--TO Civic numbers.
--NOTE: SBPDs and MOBs use a different logic than ORD PDs.
CASE WHEN (PLL.SINGLE_BLDG_IND = 'Y'  or PLL.MOBILE_POLL_IND = 'Y') and PDSS.TO_ST_ADR_NBR is NOT NULL THEN PDSS.FROM_ST_ADR_NBR
ELSE  PDSS.TO_ST_ADR_NBR
END AS TO_CIV_NUM,


--FROM CROSS FEATURES
--PDSS.FROM_CROSS_FEATURE_ID,
--PDSS.FROM_CROSS_FEATURE,
--ECSTR2.ST_NME ||' '|| RTRIM(ECSTR2.ST_TYP_CDE) ||' '|| ECSTR2.ST_DRCTN_CDE  as FROM_STREET,

--If the street side description is 'ALL', don't show a FROM CROSS value.
CASE
    WHEN (SS.ST_SIDE_DESCE = 'All') THEN NULL
    WHEN (SS.ST_SIDE_DESCE <> 'All') THEN
      CASE
        WHEN PDSS.FROM_CROSS_FEATURE is not NULL THEN PDSS.FROM_CROSS_FEATURE
        ELSE ECSTR2.ST_NME ||' '|| RTRIM(ECSTR2.ST_TYP_CDE) ||' '|| ECSTR2.ST_DRCTN_CDE
      END
  END AS FROM_CROSS_FEAT,


--TO CROSS FEATURES
--PDSS.TO_CROSS_FEATURE_ID,
--PDSS.TO_CROSS_FEATURE,
--ECSTR3.ST_NME ||' '|| RTRIM(ECSTR3.ST_TYP_CDE) ||' '|| ECSTR3.ST_DRCTN_CDE  as TO_STREET,

--If the street side description is 'ALL', don't show a TO CROSS value.
CASE
    WHEN (SS.ST_SIDE_DESCE = 'All') THEN NULL
    WHEN (SS.ST_SIDE_DESCE <> 'All') THEN
      CASE
        WHEN PDSS.TO_CROSS_FEATURE is not NULL THEN PDSS.TO_CROSS_FEATURE
        ELSE ECSTR3.ST_NME ||' '|| RTRIM(ECSTR3.ST_TYP_CDE) ||' '|| ECSTR3.ST_DRCTN_CDE
      END
  END AS TO_CROSS_FEAT,


 --STREET SIDE
  --SS.ST_SIDE_DESCE, SS.ST_SIDE_DESCF

-- If the French and STREET SIDE DESCRIPTIONS are the same, ST_SIDE_DESCE gets listed.
-- If the French and English STREET SIDE DESCRIPTIONS are different, ST_SIDE_DESCE / ST_SIDE_DESCF gets listed for the EDs outside of Quebec, and ST_SIDE_DESCF / ST_SIDE_DESCE gets listed for the EDs inside of Quebec.
CASE
    WHEN (SS.ST_SIDE_DESCF is not null or SS.ST_SIDE_DESCE is not null) and EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 THEN SS.ST_SIDE_DESCF ||' / '|| SS.ST_SIDE_DESCE
    WHEN (SS.ST_SIDE_DESCF is not null or SS.ST_SIDE_DESCE is not null) and (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) THEN SS.ST_SIDE_DESCE ||' / '|| SS.ST_SIDE_DESCF
    ELSE NULL

 END AS ST_SIDE_DESC_BIL,



--PD_PLACE TABLE, FOR TOP-RIGHT PD DESCRIPTIONS
  ECPL2.PLACE_NAME DESC_PLACE_NAME,
  CSDTP2.CSD_TYP_DESCE PD_PLACE_CSD_TYP_DESCE , CSDTP2.CSD_TYP_DESCF PD_PLACE_CSD_TYP_DESCF,


-- If the French and CSD TYPE DESCRIPTIONS are the same, CSD_TYP_DESCE gets listed.
-- If the French and English CSD TYPE DESCRIPTIONS are different, CSD_TYP_DESCE / CSD_TYP_DESCF gets listed for the EDs outside of Quebec, and CSD_TYP_DESCF / CSD_TYP_DESCE gets listed for the EDs inside of Quebec.
 CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      CASE
        WHEN CSDTP2.CSD_TYP_DESCE <> CSDTP2.CSD_TYP_DESCF THEN CSDTP2.CSD_TYP_DESCF ||' / '|| CSDTP2.CSD_TYP_DESCE
        ELSE CSDTP2.CSD_TYP_DESCF
      END
    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) then
      CASE
        WHEN CSDTP2.CSD_TYP_DESCE <> CSDTP2.CSD_TYP_DESCF THEN CSDTP2.CSD_TYP_DESCE ||' / '|| CSDTP2.CSD_TYP_DESCF
        ELSE CSDTP2.CSD_TYP_DESCE
      END
  END AS DESC_CSD_TYP_DESC_BIL,


 CSDTP2.CSD_TYP_ABBRE DESC_CSD_TYP_ABBR_BI,


--FULL PD_PLACE_PLACE NAME
-- If the French and CSD TYPE DESCRIPTIONS are the same, CSD_TYP_DESCE gets listed.
-- If the French and English CSD TYPE DESCRIPTIONS are different, CSD_TYP_DESCE / CSD_TYP_DESCF gets listed for the EDs outside of Quebec, and CSD_TYP_DESCF / CSD_TYP_DESCE gets listed for the EDs inside of Quebec.
 ECPL2.PLACE_NAME ||''||  CASE
    WHEN ECPL2.PLACE_NAME is not null and EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 then
      CASE
       WHEN  CSDTP2.CSD_TYP_DESCE is null and CSDTP2.CSD_TYP_DESCF is not null THEN ', '|| CSDTP2.CSD_TYP_DESCF
       WHEN  CSDTP2.CSD_TYP_DESCF is null and CSDTP2.CSD_TYP_DESCE is not null THEN ', '|| CSDTP2.CSD_TYP_DESCE
       WHEN  CSDTP2.CSD_TYP_DESCE is null and CSDTP2.CSD_TYP_DESCF is null THEN ''
        WHEN CSDTP2.CSD_TYP_DESCE is not null and CSDTP2.CSD_TYP_DESCF is not null  and CSDTP2.CSD_TYP_DESCE <> CSDTP2.CSD_TYP_DESCF   THEN ', '|| CSDTP2.CSD_TYP_DESCF ||' / '|| CSDTP2.CSD_TYP_DESCE
          ELSE ', '||CSDTP2.CSD_TYP_DESCF
      END
    WHEN ECPL2.PLACE_NAME is not null and (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) then
      CASE
       WHEN  CSDTP2.CSD_TYP_DESCE is null and CSDTP2.CSD_TYP_DESCF is not null THEN ', '|| CSDTP2.CSD_TYP_DESCF
       WHEN  CSDTP2.CSD_TYP_DESCF is null and CSDTP2.CSD_TYP_DESCE is not null THEN ', '|| CSDTP2.CSD_TYP_DESCE
       WHEN  CSDTP2.CSD_TYP_DESCE is null and CSDTP2.CSD_TYP_DESCF is null THEN ''
        WHEN CSDTP2.CSD_TYP_DESCE is not null and CSDTP2.CSD_TYP_DESCF is not null  and CSDTP2.CSD_TYP_DESCE <> CSDTP2.CSD_TYP_DESCF   THEN ', '|| CSDTP2.CSD_TYP_DESCE ||' / '|| CSDTP2.CSD_TYP_DESCF
          ELSE ', '||CSDTP2.CSD_TYP_DESCE
      END
  END
   AS DESC_FULL_PLACE_NAME



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
  LEFT JOIN ECDBA.PD_STREET_SEGMENT PDSS on
    PLL.PD_ID = PDSS.PD_ID
  LEFT JOIN ECDBA.POLL_NAME PNAME on
    PLL.POLL_NAME_ID = PNAME.POLL_NAME_ID
  LEFT JOIN ECDBA.STREET_SIDE SS on
    PDSS.ST_SIDE_ID = SS.ST_SIDE_ID
  LEFT JOIN ECDBA.EC_STREET ECSTR on
    PDSS.STREET_ID = ECSTR.STREET_ID
  LEFT JOIN EC_PLACE ECPL on
    ECSTR.PLACE_ID = ECPL.PLACE_ID
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD on
    ECPL.PLACE_ID = CSD.PLACE_ID
  LEFT JOIN ECDBA.CSD_TYPE CSDTP1 on
    CSD.CSD_TYP_ID = CSDTP1.CSD_TYP_ID
  LEFT JOIN ECDBA.EC_STREET ECSTR2 on
    PDSS.FROM_CROSS_FEATURE_ID = ECSTR2.STREET_ID
  LEFT JOIN ECDBA.EC_STREET ECSTR3 on
    PDSS.TO_CROSS_FEATURE_ID = ECSTR3.STREET_ID
  LEFT JOIN ECDBA.RELATED_POLL RP on
    PLL.PD_ID = RP.CHILD_PD_ID
  LEFT JOIN ECDBA.POLL PLL2 on
    RP.PARENT_PD_ID = PLL2.PD_ID
  LEFT JOIN ECDBA.POLL_NAME PNAME2 on
    PLL2.POLL_NAME_ID = PNAME2.POLL_NAME_ID

--LEFT JOIN PD_PLACE
  LEFT JOIN EC_PLACE ECPL2 on
 PLL.PLACE_ID = ECPL2.PLACE_ID
 LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD2 on
ECPL2.PLACE_ID = CSD2.PLACE_ID
LEFT JOIN ECDBA.CSD_TYPE CSDTP2 on
CSD2.CSD_TYP_ID = CSDTP2.CSD_TYP_ID



--WHERE CLAUSES
--For 2023 Redistribution, we used ELCTRL_EVENT_ID  = '88'.
-- This will change to REDIST.RDSTRBTN_CRNT_IND = 'Y' in RLS once the data is finalized.
-- This will change to EDEE.ELCTRL_EVENT_ID  = '99' in RLS once the data is finalized.
-- This will change to EDEE.CRNT_IND ='Y' in RLS once the data is finalized.

where
--Reactivate these two rows if you want to refer to the most recent data.
--REDIST.RDSTRBTN_CRNT_IND = 'Y'
--and EDEE.CRNT_IND ='Y'

--There is a query to determine different  ELCTRL_EVENT_ID values.
--Switch to '99' and add "AND" before the next line to refer to the RELEASE data.
EDEE.ELCTRL_EVENT_ID = '88'

  and PLL.ADVANCE_POLL_IND = 'N'
  and PLL.VOID_IND = 'N'
  and PLL.PD_NBR <> 999
  --and PLL.PD_NBR > 499
  --and PLL.PD_NBR < 600
  and EDistrict.ED_CODE in ED_LIST_HERE

--Use this code to select ranges of EDs.
-- and EDistrict.ED_CODE > 13000
-- and EDistrict.ED_CODE < 24021

order by
  EDEE.EVENT_ED_CODE, ECPL.PLACE_NAME, ECSTR.ST_PARSED_NAME,
  ECSTR.ST_DRCTN_CDE, ECSTR.ST_TYP_CDE, FROM_CIV_NUM + 0 NULLS FIRST
--PLL.PD_NBR, PLL.PD_NBR_SFX,
