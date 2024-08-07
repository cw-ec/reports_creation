--This query shows the information for every polling division belonging to a given ELCTRL_EVENT_ID. It also shows the polling sites that are attached to said polling divisions. This query is necessary to find MOB information for the PD Descriptions.  It will be joined with the PD_Numbers - SIMPLIFIED.sql query in the PYTHON scripts.
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

--SITE_IDs of different types to validate data.
--SIT1.SITE_ID ORD_SITE_ID,  SIT2.SITE_ID MOB_SITE_ID, SIT3.SITE_ID ORD_ADV_SITE_ID, SIT4.SITE_ID MOB_ADV_SITE_ID,



 --PROVINCE INFORMATION
-- If the French and English province names are the same, PRVNC_NAMEE gets listed.
-- If the French and English province names are different, PRVNC_NAMEE / PRVNC_NAMEF gets listed for the EDs outside of Quebec, and PRVNC_NAMEF / PRVNC_NAMEE gets listed for the EDs inside of Quebec.
  EDistrict.PRVNC_ID, PROV.CPC_PRVNC_NAME,
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
  EDEE.ELCTRL_EVENT_ID, EDEE.ED_ELCTRL_EVENT_ID,
  EDEE.CRNT_IND,



--ORD PD INFORMATION (for ORD/SBPD/MOB)
-- This is akin to the full EMRP number that shows both the PD number and the PD suffix.
    CONCAT (CONCAT (PLL.PD_NBR, '-'), PLL.PD_NBR_SFX ) FULL_PD_NBR,
  PLL.PD_NBR, PLL.PD_NBR_SFX, PLL.PD_ID, PLL.VOID_IND, MPP.MOBILE_POLL_STN_ID, EA_PEC.ELECTOR_COUNT ELECTORS_LISTED,
--SEEE1.SITE_ID ORD_PD_SITE_ID,  SEEE3.SITE_ID MOB_PD_SITE_ID,

--Combining Site_ID columns for both ORD/SBPDs with MOBs.
  CASE
        WHEN SEEE1.SITE_ID is not null then SEEE1.SITE_ID
        ELSE SEEE3.SITE_ID
      END AS PD_SITE_ID,

--ORD PD Name
PNAME.POLL_NAME POLL_NAME_FIXED,
--REPLACE (PNAME.POLL_NAME, '--', '—') AS POLL_NAME_FIXED,
--Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.

--More ORD PD Information
PLL.URBAN_RURAL_IND,



--SBPD INFORMATION
--SBPD Building Address
        EC_ADD5.ADDRESS_ID SBPD_ADDRESS_ID,

--DEACTIVATED FROM_STE_NBR SBPD_FROM_STE_NBR, TO_STE_NBR SBPD_TO_STE_NBR, FROM_FLOOR SBPD_FROM_FLOOR, TO_FLOOR SBPD_TO_FLOOR,

--SBPD Building Name
-- If the French and English building names are the same, BLDG_NAMEE gets listed.
-- If the French and English building names are different, BLDG_NAMEE / BLDG_NAMEF gets listed for the EDs outside of Quebec, and BLDG_NAMEF / BLDG_NAMEE gets listed for the EDs inside of Quebec.
    CASE
    WHEN BLDG_NAMEE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and BLDG_NAMEE <> BLDG_NAMEF THEN BLDG_NAMEF ||' / '|| BLDG_NAMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and BLDG_NAMEE <> BLDG_NAMEF THEN BLDG_NAMEE ||' / '|| BLDG_NAMEF
        ELSE BLDG_NAMEE
      END
    WHEN BLDG_NAMEE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and BLDG_NAMEE <> BLDG_NAMEF THEN BLDG_NAMEF ||' / '|| BLDG_NAMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and BLDG_NAMEE <> BLDG_NAMEF THEN BLDG_NAMEE ||' / '|| BLDG_NAMEF
        ELSE BLDG_NAMEE
      END
  END AS SBPD_BLDG_NAME_BIL,

 --FINAL SBPD ADDRESS (involves many concatenations and English/French cardinal directions)
      case
    when

      CASE
        WHEN EC_ADD5.ST_ADR_NBR is not null then EC_ADD5.ST_ADR_NBR
        ELSE NULL
      END ||''||

           CASE
        WHEN EC_ST5.ST_NME is not null then CONCAT (' ', EC_ST5.ST_NME)
              ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST5.ST_TYP_CDE is not null then CONCAT (' ', EC_ST5.ST_TYP_CDE)
                ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD5.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD5.ST_DRCTN_DESCE <> SD5.ST_DRCTN_DESCF THEN CONCAT (' ', SD5.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD5.ST_DRCTN_DESCE <> SD5.ST_DRCTN_DESCF THEN CONCAT (' ', SD5.ST_DRCTN_DESCE)
            ELSE ''
          END
        ELSE SD5.ST_DRCTN_DESCE
       END) is not null then

      CASE

        WHEN EC_ADD5.ST_ADR_NBR is not null then EC_ADD5.ST_ADR_NBR
              ELSE NULL
      END ||''||


      CASE
        WHEN EC_ST5.ST_NME is not null then CONCAT (' ', EC_ST5.ST_NME)

        ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST5.ST_TYP_CDE is not null then CONCAT (' ', EC_ST5.ST_TYP_CDE)

        ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD5.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD5.ST_DRCTN_DESCE <> SD5.ST_DRCTN_DESCF THEN CONCAT (' ', SD5.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD5.ST_DRCTN_DESCE <> SD5.ST_DRCTN_DESCF THEN CONCAT (' ', SD5.ST_DRCTN_DESCE)
            ELSE ''
          END
             END)
    ELSE (
      CASE
        WHEN EC_ADD5.MERIDIAN_NBR is not null then EC_ADD5.SECTION_NBR ||' T'|| EC_ADD5.TWNSHP_NBR ||' R'|| EC_ADD5.RANGE_NBR ||' '|| EC_ADD5.MERIDIAN_NBR
               ELSE NULL
      END)
  END as FINAL_SBPD_ADDRESS,


--SBPD PLACE_NAME
  EP5.PLACE_NAME SBPD_PLACE_NAME,


--SBPD CSD_TYP_DESC
  CASE
    WHEN CSDT5.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT5.CSD_TYP_DESCE <> CSDT5.CSD_TYP_DESCF THEN CSDT5.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT5.CSD_TYP_DESCE <> CSDT5.CSD_TYP_DESCF THEN CSDT5.CSD_TYP_DESCE
        ELSE CSDT5.CSD_TYP_DESCE
      END
     END AS SBPD_CSD_TYP_DESC_BIL,


--SBPD FULL_PLACE (involves a concatenation and English/French CSD type descriptions)
  EP5.PLACE_NAME ||', '||   CASE
    WHEN CSDT5.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT5.CSD_TYP_DESCE <> CSDT5.CSD_TYP_DESCF THEN CSDT5.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT5.CSD_TYP_DESCE <> CSDT5.CSD_TYP_DESCF THEN CSDT5.CSD_TYP_DESCE
        ELSE CSDT5.CSD_TYP_DESCE
      END
     END AS FULL_SBPD_PLACE,



--SITE INFORMATION (for ORD/SBPD/MOB)
--
--SITE NAME
-- If the French and English site names are the same, SITE_NMEE gets listed.
-- If the French and English site names are different, SITE_NMEE / SITE_NMEF gets listed for the EDs outside of Quebec, and SITE_NMEF / SITE_NMEE gets listed for the EDs inside of Quebec.
CASE
    WHEN SIT1.SITE_NMEE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SIT1.SITE_NMEE <> SIT1.SITE_NMEF THEN SIT1.SITE_NMEF ||' / '|| SIT1.SITE_NMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SIT1.SITE_NMEE <> SIT1.SITE_NMEF THEN SIT1.SITE_NMEE ||' / '|| SIT1.SITE_NMEF
        ELSE SIT1.SITE_NMEE
      END
    WHEN SIT1.SITE_NMEE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SIT3.SITE_NMEE <> SIT3.SITE_NMEF THEN SIT3.SITE_NMEF ||' / '|| SIT3.SITE_NMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SIT3.SITE_NMEE <> SIT3.SITE_NMEF THEN SIT3.SITE_NMEE ||' / '|| SIT3.SITE_NMEF
        ELSE SIT3.SITE_NMEE
      END
  END AS SITE_NAME_BIL,


--SITE ADDRESS_ID
  CASE
    WHEN EC_ADD1.ADDRESS_ID is not null then EC_ADD1.ADDRESS_ID
    ELSE EC_ADD3.ADDRESS_ID
  END AS SITE_ADDRESS_ID,


 --DEACTIVATED CODE
  --SITE STE_NBR (for ORD/SBPD/MOB)
 -- CASE
 --   WHEN EC_ADD1.STE_NBR is not null then EC_ADD1.STE_NBR
 --   ELSE EC_ADD3.STE_NBR
 -- END AS SITE_STE_NBR,

  --SITE ST_ADR_NBR (for ORD/SBPD/MOB)
--  CASE
  --  WHEN EC_ADD1.ST_ADR_NBR is not null then EC_ADD1.ST_ADR_NBR
  --  ELSE EC_ADD3.ST_ADR_NBR
 -- END AS SITE_ST_ADR_NBR,

  --SITE ST_ADR_NBR_SFX_CDE (for ORD/SBPD/MOB)
--  CASE
 --   WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is not null then EC_ADD1.ST_ADR_NBR_SFX_CDE
  --  ELSE EC_ADD3.ST_ADR_NBR_SFX_CDE
 -- END AS SITE_ST_ADR_NBR_SFX_CDE,

  --SITE ST_NME (for ORD/SBPD/MOB)
 -- CASE
  --  WHEN EC_ST1.ST_NME is not null then EC_ST1.ST_NME
  --  ELSE EC_ST3.ST_NME
 -- END AS SITE_ST_NME,

   --SITE ST_TYP_CDE (for ORD/SBPD/MOB)
 -- CASE
 --   WHEN EC_ST1.ST_TYP_CDE is not null then EC_ST1.ST_TYP_CDE
  --  ELSE EC_ST3.ST_TYP_CDE
 -- END AS SITE_ST_TYP_CDE,

  --SITE ST_DRCTN_DESC (for ORD/SBPD/MOB)
 -- CASE
  --  WHEN SD1.ST_DRCTN_DESCE is not null then
   --   CASE
   --     WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN SD1.ST_DRCTN_DESCF
    --    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN SD1.ST_DRCTN_DESCE
   --     ELSE SD1.ST_DRCTN_DESCE
   --   END
  --  WHEN SD1.ST_DRCTN_DESCE is null then
   --   CASE
   --     WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN SD3.ST_DRCTN_DESCF
    --    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN SD3.ST_DRCTN_DESCE
    --    ELSE SD3.ST_DRCTN_DESCE
   --   END
 -- END AS SITE_ST_DRCTN_DESC,


    --SITE Full Street Address (for ORD/SBPD/MOB)
  --CASE
  --  WHEN EC_ADD1.STE_NBR is not null then CONCAT (EC_ADD1.STE_NBR, ', ')
 --   WHEN EC_ADD1.STE_NBR is null and EC_ADD3.STE_NBR is not null then CONCAT (EC_ADD3.STE_NBR, ', ')
   -- ELSE NULL
 -- END ||''||CASE
  --  WHEN EC_ADD1.ST_ADR_NBR is not null then EC_ADD1.ST_ADR_NBR
   -- WHEN EC_ADD1.ST_ADR_NBR is null and EC_ADD3.ST_ADR_NBR is not null then EC_ADD3.ST_ADR_NBR
   -- ELSE NULL
  --END ||''||CASE
    --WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD1.ST_ADR_NBR_SFX_CDE)
    --WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is null and EC_ADD3.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD3.ST_ADR_NBR_SFX_CDE)
    --ELSE NULL
  --END ||''||CASE
    --WHEN EC_ST1.ST_NME is not null then CONCAT (' ', EC_ST1.ST_NME)
    --WHEN EC_ST1.ST_NME is null and EC_ST3.ST_NME is not null then CONCAT (' ', EC_ST3.ST_NME)
    --ELSE NULL
  --END ||''|| RTRIM(CASE
    --WHEN EC_ST1.ST_TYP_CDE is not null then CONCAT (' ', EC_ST1.ST_TYP_CDE)
    --WHEN EC_ST1.ST_TYP_CDE is null and EC_ST3.ST_TYP_CDE is not null then CONCAT (' ', EC_ST3.ST_TYP_CDE)
    --ELSE NULL
  --END) ||''|| (CASE
    --WHEN SD1.ST_DRCTN_DESCE is not null then
      --CASE
        --WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCF)
        --WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCE)
        --ELSE ''
      --END
    --WHEN SD1.ST_DRCTN_DESCE is null then
     -- CASE
    --    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCF)
    --    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCE)
   --     ELSE ''
    --  END
 -- END) as SITE_ADDRESS,

  --SITE STRM (for ORD/SBPD/MOB)
  --CASE
   -- WHEN EC_ADD1.MERIDIAN_NBR is not null then EC_ADD1.SECTION_NBR ||' T'|| EC_ADD1.TWNSHP_NBR ||' R'|| EC_ADD1.RANGE_NBR ||' '|| EC_ADD1.MERIDIAN_NBR
   -- WHEN EC_ADD3.MERIDIAN_NBR is not null THEN EC_ADD3.SECTION_NBR ||' T'|| EC_ADD3.TWNSHP_NBR ||' R'|| EC_ADD3.RANGE_NBR ||' '|| EC_ADD3.MERIDIAN_NBR
   -- ELSE NULL
  --END AS SITE_TRM_ADDRESS,


--FINAL SITE_ADDRESS (for ORD/SBPD/MOB)
--Have fun trying to replicate this code!
  --
  case
    when
      CASE
        WHEN EC_ADD1.STE_NBR is not null then CONCAT (EC_ADD1.STE_NBR, ', ')
        WHEN EC_ADD1.STE_NBR is null and EC_ADD3.STE_NBR is not null then CONCAT (EC_ADD3.STE_NBR, ', ')
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD1.ST_ADR_NBR is not null then EC_ADD1.ST_ADR_NBR
        WHEN EC_ADD1.ST_ADR_NBR is null and EC_ADD3.ST_ADR_NBR is not null then EC_ADD3.ST_ADR_NBR
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD1.ST_ADR_NBR_SFX_CDE)
        WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is null and EC_ADD3.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD3.ST_ADR_NBR_SFX_CDE)
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ST1.ST_NME is not null then CONCAT (' ', EC_ST1.ST_NME)
        WHEN EC_ST1.ST_NME is null and EC_ST3.ST_NME is not null then CONCAT (' ', EC_ST3.ST_NME)
        ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST1.ST_TYP_CDE is not null then CONCAT (' ', EC_ST1.ST_TYP_CDE)
        WHEN EC_ST1.ST_TYP_CDE is null and EC_ST3.ST_TYP_CDE is not null then CONCAT (' ', EC_ST3.ST_TYP_CDE)
        ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD1.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCE)
            ELSE ''
          END
        WHEN SD1.ST_DRCTN_DESCE is null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCE)
            ELSE ''
          END
      END) is not null then
      CASE
        WHEN EC_ADD1.STE_NBR is not null then CONCAT (EC_ADD1.STE_NBR, ', ')
        WHEN EC_ADD1.STE_NBR is null and EC_ADD3.STE_NBR is not null then CONCAT (EC_ADD3.STE_NBR, ', ')
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD1.ST_ADR_NBR is not null then EC_ADD1.ST_ADR_NBR
        WHEN EC_ADD1.ST_ADR_NBR is null and EC_ADD3.ST_ADR_NBR is not null then EC_ADD3.ST_ADR_NBR
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD1.ST_ADR_NBR_SFX_CDE)
        WHEN EC_ADD1.ST_ADR_NBR_SFX_CDE is null and EC_ADD3.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD3.ST_ADR_NBR_SFX_CDE)
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ST1.ST_NME is not null then CONCAT (' ', EC_ST1.ST_NME)
        WHEN EC_ST1.ST_NME is null and EC_ST3.ST_NME is not null then CONCAT (' ', EC_ST3.ST_NME)
        ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST1.ST_TYP_CDE is not null then CONCAT (' ', EC_ST1.ST_TYP_CDE)
        WHEN EC_ST1.ST_TYP_CDE is null and EC_ST3.ST_TYP_CDE is not null then CONCAT (' ', EC_ST3.ST_TYP_CDE)
        ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD1.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD1.ST_DRCTN_DESCE <> SD1.ST_DRCTN_DESCF THEN CONCAT (' ', SD1.ST_DRCTN_DESCE)
            ELSE ''
          END
        WHEN SD1.ST_DRCTN_DESCE is null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD3.ST_DRCTN_DESCE <> SD3.ST_DRCTN_DESCF THEN CONCAT (' ', SD3.ST_DRCTN_DESCE)
            ELSE ''
          END
      END)
    ELSE (
      CASE
        WHEN EC_ADD1.MERIDIAN_NBR is not null then EC_ADD1.SECTION_NBR ||' T'|| EC_ADD1.TWNSHP_NBR ||' R'|| EC_ADD1.RANGE_NBR ||' '|| EC_ADD1.MERIDIAN_NBR
        WHEN EC_ADD3.MERIDIAN_NBR is not null THEN EC_ADD3.SECTION_NBR ||' T'|| EC_ADD3.TWNSHP_NBR ||' R'|| EC_ADD3.RANGE_NBR ||' '|| EC_ADD3.MERIDIAN_NBR
        ELSE NULL
      END)
  END as FINAL_SITE_ADDRESS,


--SITE PLACE_NAME (for ORD/SBPD/MOB)
  CASE
    WHEN EP1.PLACE_NAME is not null then EP1.PLACE_NAME
    ELSE EP3.PLACE_NAME
  END AS SITE_PLACE_NAME,


--SITE CSD_TYP_DESC (for ORD/SBPD/MOB)
  CASE
    WHEN CSDT1.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT1.CSD_TYP_DESCE <> CSDT1.CSD_TYP_DESCF THEN CSDT1.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT1.CSD_TYP_DESCE <> CSDT1.CSD_TYP_DESCF THEN CSDT1.CSD_TYP_DESCE
        ELSE CSDT1.CSD_TYP_DESCE
      END
    WHEN CSDT1.CSD_TYP_DESCE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT3.CSD_TYP_DESCE <> CSDT3.CSD_TYP_DESCF THEN CSDT3.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT3.CSD_TYP_DESCE <> CSDT3.CSD_TYP_DESCF THEN CSDT3.CSD_TYP_DESCE
        ELSE CSDT3.CSD_TYP_DESCE
      END
  END AS SITE_CSD_TYP_DESC_BIL,


--SITE FULL_PLACE (for ORD/SBPD/MOB)
  CASE
    WHEN EP1.PLACE_NAME is not null then CONCAT (EP1.PLACE_NAME, ', ')
    WHEN EP1.PLACE_NAME is null and EP3.PLACE_NAME is not null then CONCAT (EP3.PLACE_NAME, ', ')
    ELSE NULL
  END ||''||CASE
    WHEN CSDT1.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT1.CSD_TYP_DESCE <> CSDT1.CSD_TYP_DESCF THEN CSDT1.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT1.CSD_TYP_DESCE <> CSDT1.CSD_TYP_DESCF THEN CSDT1.CSD_TYP_DESCE
        ELSE CSDT1.CSD_TYP_DESCE
      END
    WHEN CSDT1.CSD_TYP_DESCE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT3.CSD_TYP_DESCE <> CSDT3.CSD_TYP_DESCF THEN CSDT3.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT3.CSD_TYP_DESCE <> CSDT3.CSD_TYP_DESCF THEN CSDT3.CSD_TYP_DESCE
        ELSE CSDT3.CSD_TYP_DESCE
      END
  END AS FULL_SITE_PLACE,


--SITE  PSTL_CDE (for ORD/SBPD/MOB)
  CASE
    WHEN EC_ADD1.PSTL_CDE is not null then EC_ADD1.PSTL_CDE
    ELSE EC_ADD3.PSTL_CDE
  END AS SITE_PSTL_CDE,



--ADV INFORMATION for ADV (for ORD/SBPD/MOB)

--ADV Number (for ORD/SBPD/MOB)
  PLL.ADVANCE_POLL_IND,
  CONCAT (CONCAT (PLL2.PD_NBR, '-'), PLL2.PD_NBR_SFX ) FULL_ADV_PD_NBR,
   PLL2.PD_NBR ADV_PD_NBR, PLL2.PD_NBR_SFX ADV_PD_NBR_SFX,

--SEEE2.SITE_ID ORD_ADVPD_SITE_ID,  SEEE4.SITE_ID MOB_ADVPD_SITE_ID,

 CASE
        WHEN SEEE2.SITE_ID is not null then SEEE2.SITE_ID
        ELSE SEEE4.SITE_ID
      END AS ADVPD_SITE_ID,


--ESTABLISHING ADV POLL NAME (for ORD/SBPD/MOB)

--Related Poll Table
  PARENT_PD_ID ADV_PD_ID,
--DEACTIVATED CHILD_PD_ID CHILD_ORD_PD_ID,

--ADV PD Name (for ORD/SBPD/MOB)
--DEACTIVATED PNAME2.POLL_NAME_ID ADV_POLL_NAME_ID,
PNAME2.POLL_NAME ADV_POLL_NAME_FIXED,
--REPLACE (PNAME2.POLL_NAME, '--', '—') AS ADV_POLL_NAME_FIXED,
--Note that replacing "--" with an en-dash is now taken care of in Chris Wenkoff's Python scripts.



--ADV SITE INFORMATION (for ORD/SBPD/MOB)

--ADV SITE NAME (for ORD/SBPD/MOB)
  CASE
    WHEN SIT1.SITE_NMEE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SIT2.SITE_NMEE <> SIT2.SITE_NMEF THEN SIT2.SITE_NMEF ||' / '|| SIT2.SITE_NMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SIT2.SITE_NMEE <> SIT2.SITE_NMEF THEN SIT2.SITE_NMEE ||' / '|| SIT2.SITE_NMEF
        ELSE SIT2.SITE_NMEE
      END
    WHEN SIT2.SITE_NMEE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SIT4.SITE_NMEE <> SIT4.SITE_NMEF THEN SIT4.SITE_NMEF ||' / '|| SIT4.SITE_NMEE
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SIT4.SITE_NMEE <> SIT4.SITE_NMEF THEN SIT4.SITE_NMEE ||' / '|| SIT4.SITE_NMEF
        ELSE SIT4.SITE_NMEE
      END
  END AS ADV_SITE_NAME_BIL,


--ADV SITE ADDRESS_ID (for ORD/SBPD/MOB)
  CASE
    WHEN EC_ADD2.ADDRESS_ID is not null then EC_ADD2.ADDRESS_ID
    ELSE EC_ADD4.ADDRESS_ID
  END AS ADV_SITE_ADDRESS_ID,

--ADV SITE STE_NBR (for ORD/SBPD/MOB)
--KEEP THE DEACTIVATED CODE AS A REFERENCE

 -- CASE
  --  WHEN EC_ADD2.STE_NBR is not null then EC_ADD2.STE_NBR
 --   ELSE EC_ADD4.STE_NBR
--  END AS ADV_SITE_STE_NBR,

  --ADV SITE ST_ADR_NBR (for ORD/SBPD/MOB)
 -- CASE
 --   WHEN EC_ADD2.ST_ADR_NBR is not null then EC_ADD2.ST_ADR_NBR
 --   ELSE EC_ADD4.ST_ADR_NBR
 -- END AS ADV_SITE_ST_ADR_NBR,

  --ADV SITE ST_ADR_NBR_SFX_CDE (for ORD/SBPD/MOB)
 -- CASE
--    WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is not null then EC_ADD2.ST_ADR_NBR_SFX_CDE
--    ELSE EC_ADD4.ST_ADR_NBR_SFX_CDE
--  END AS ADV_SITE_ST_ADR_NBR_SFX_CDE,

  --ADV SITE ST_NME (for ORD/SBPD/MOB)
 -- CASE
 --   WHEN EC_ST2.ST_NME is not null then EC_ST2.ST_NME
 --   ELSE EC_ST4.ST_NME
 -- END AS ADV_SITE_ST_NME,

  --ADV SITE ST_TYP_CDE (for ORD/SBPD/MOB)
 -- CASE
--    WHEN EC_ST2.ST_TYP_CDE is not null then EC_ST2.ST_TYP_CDE
--    ELSE EC_ST4.ST_TYP_CDE
--  END AS ADV_SITE_ST_TYP_CDE,

  --ADV SITE ST_DRCTN_DESC (for ORD/SBPD/MOB)
 -- CASE
 --   WHEN SD2.ST_DRCTN_DESCE is not null then
 --     CASE
  --      WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN SD2.ST_DRCTN_DESCF
  --      WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN SD2.ST_DRCTN_DESCE
  --      ELSE SD2.ST_DRCTN_DESCE
 --     END
  --  WHEN SD2.ST_DRCTN_DESCE is null then
  --    CASE
  --      WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN SD4.ST_DRCTN_DESCF
  --      WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN SD4.ST_DRCTN_DESCE
  --      ELSE SD4.ST_DRCTN_DESCE
  --    END
 -- END AS ADV_SITE_ST_DRCTN_DESC,

    --ADV SITE Full Street Address (for ORD/SBPD/MOB)
--  CASE
--    WHEN EC_ADD2.STE_NBR is not null then CONCAT (EC_ADD2.STE_NBR, ', ')
--    WHEN EC_ADD2.STE_NBR is null and EC_ADD4.STE_NBR is not null then CONCAT (EC_ADD4.STE_NBR, ', ')
--    ELSE NULL
--  END ||''||CASE
--    WHEN EC_ADD2.ST_ADR_NBR is not null then EC_ADD2.ST_ADR_NBR
--    WHEN EC_ADD2.ST_ADR_NBR is null and EC_ADD4.ST_ADR_NBR is not null then EC_ADD4.ST_ADR_NBR
--    ELSE NULL
--  END ||''||CASE
--    WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD2.ST_ADR_NBR_SFX_CDE)
--    WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is null and EC_ADD4.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD4.ST_ADR_NBR_SFX_CDE)
--    ELSE NULL
--  END ||''||CASE
--    WHEN EC_ST2.ST_NME is not null then CONCAT (' ', EC_ST2.ST_NME)
--    WHEN EC_ST2.ST_NME is null and EC_ST4.ST_NME is not null then CONCAT (' ', EC_ST4.ST_NME)
--    ELSE NULL
--  END ||''|| RTRIM(CASE
--    WHEN EC_ST2.ST_TYP_CDE is not null then CONCAT (' ', EC_ST2.ST_TYP_CDE)
--    WHEN EC_ST2.ST_TYP_CDE is null and EC_ST4.ST_TYP_CDE is not null then CONCAT (' ', EC_ST4.ST_TYP_CDE)
--    ELSE NULL
--  END) ||''|| (CASE
--    WHEN SD2.ST_DRCTN_DESCE is not null then
--      CASE
--        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCF)
--        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCE)
--        ELSE ''
--      END
--    WHEN SD2.ST_DRCTN_DESCE is null then
--      CASE
--        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCF)
--        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCE)
--        ELSE ''
--      END
--  END) as ADV_SITE_ADDRESS,

   --ADV SITE STRM
--  CASE
--    WHEN EC_ADD2.MERIDIAN_NBR is not null then EC_ADD2.SECTION_NBR ||' T'|| EC_ADD2.TWNSHP_NBR ||' R'|| EC_ADD2.RANGE_NBR ||' '|| EC_ADD2.MERIDIAN_NBR
--    WHEN EC_ADD4.MERIDIAN_NBR is not null THEN EC_ADD4.SECTION_NBR ||' T'|| EC_ADD4.TWNSHP_NBR ||' R'|| EC_ADD4.RANGE_NBR ||' '|| EC_ADD4.MERIDIAN_NBR
--    ELSE NULL
--  END ADV_SITE_TRM_ADDRESS,


  --FINAL_ADV SITE ADDRESS (for ORD/SBPD/MOB)
  --Good luck!
  --
  case
    when
      CASE
        WHEN EC_ADD2.STE_NBR is not null then CONCAT (EC_ADD2.STE_NBR, ', ')
        WHEN EC_ADD2.STE_NBR is null and EC_ADD4.STE_NBR is not null then CONCAT (EC_ADD4.STE_NBR, ', ')
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD2.ST_ADR_NBR is not null then EC_ADD2.ST_ADR_NBR
        WHEN EC_ADD2.ST_ADR_NBR is null and EC_ADD4.ST_ADR_NBR is not null then EC_ADD4.ST_ADR_NBR
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD2.ST_ADR_NBR_SFX_CDE)
        WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is null and EC_ADD4.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD4.ST_ADR_NBR_SFX_CDE)
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ST2.ST_NME is not null then CONCAT (' ', EC_ST2.ST_NME)
        WHEN EC_ST2.ST_NME is null and EC_ST4.ST_NME is not null then CONCAT (' ', EC_ST4.ST_NME)
        ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST2.ST_TYP_CDE is not null then CONCAT (' ', EC_ST2.ST_TYP_CDE)
        WHEN EC_ST2.ST_TYP_CDE is null and EC_ST4.ST_TYP_CDE is not null then CONCAT (' ', EC_ST4.ST_TYP_CDE)
        ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD2.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCE)
            ELSE ''
          END
        WHEN SD2.ST_DRCTN_DESCE is null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCE)
            ELSE ''
          END
      END) is not null then
      CASE
        WHEN EC_ADD2.STE_NBR is not null then CONCAT (EC_ADD2.STE_NBR, ', ')
        WHEN EC_ADD2.STE_NBR is null and EC_ADD4.STE_NBR is not null then CONCAT (EC_ADD4.STE_NBR, ', ')
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD2.ST_ADR_NBR is not null then EC_ADD2.ST_ADR_NBR
        WHEN EC_ADD2.ST_ADR_NBR is null and EC_ADD4.ST_ADR_NBR is not null then EC_ADD4.ST_ADR_NBR
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD2.ST_ADR_NBR_SFX_CDE)
        WHEN EC_ADD2.ST_ADR_NBR_SFX_CDE is null and EC_ADD4.ST_ADR_NBR_SFX_CDE is not null then CONCAT ('-', EC_ADD4.ST_ADR_NBR_SFX_CDE)
        ELSE NULL
      END ||''||
      CASE
        WHEN EC_ST2.ST_NME is not null then CONCAT (' ', EC_ST2.ST_NME)
        WHEN EC_ST2.ST_NME is null and EC_ST4.ST_NME is not null then CONCAT (' ', EC_ST4.ST_NME)
        ELSE NULL
      END ||''|| RTRIM(
      CASE
        WHEN EC_ST2.ST_TYP_CDE is not null then CONCAT (' ', EC_ST2.ST_TYP_CDE)
        WHEN EC_ST2.ST_TYP_CDE is null and EC_ST4.ST_TYP_CDE is not null then CONCAT (' ', EC_ST4.ST_TYP_CDE)
        ELSE NULL
      END) ||''|| (
      CASE
        WHEN SD2.ST_DRCTN_DESCE is not null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD2.ST_DRCTN_DESCE <> SD2.ST_DRCTN_DESCF THEN CONCAT (' ', SD2.ST_DRCTN_DESCE)
            ELSE ''
          END
        WHEN SD2.ST_DRCTN_DESCE is null then
          CASE
            WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCF)
            WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and SD4.ST_DRCTN_DESCE <> SD4.ST_DRCTN_DESCF THEN CONCAT (' ', SD4.ST_DRCTN_DESCE)
            ELSE ''
          END
      END)
    ELSE (
      CASE
        WHEN EC_ADD2.MERIDIAN_NBR is not null then EC_ADD2.SECTION_NBR ||' T'|| EC_ADD2.TWNSHP_NBR ||' R'|| EC_ADD2.RANGE_NBR ||' '|| EC_ADD2.MERIDIAN_NBR
        WHEN EC_ADD4.MERIDIAN_NBR is not null THEN EC_ADD4.SECTION_NBR ||' T'|| EC_ADD4.TWNSHP_NBR ||' R'|| EC_ADD4.RANGE_NBR ||' '|| EC_ADD4.MERIDIAN_NBR
        ELSE NULL
      END)
  END as FINAL_ADV_SITE_ADDRESS,


--ADV SITE PLACE_NAME (for ORD/SBPD/MOB)
  CASE
    WHEN EP2.PLACE_NAME is not null then EP2.PLACE_NAME
    ELSE EP4.PLACE_NAME
  END AS ADV_SITE_PLACE_NAME,


--ADV SITE CSD_TYP_DESC (for ORD/SBPD/MOB)
--This accounts for differences between English and French.
  CASE
    WHEN CSDT2.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT2.CSD_TYP_DESCE <> CSDT2.CSD_TYP_DESCF THEN CSDT2.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT2.CSD_TYP_DESCE <> CSDT2.CSD_TYP_DESCF THEN CSDT2.CSD_TYP_DESCE
        ELSE CSDT2.CSD_TYP_DESCE
      END
    WHEN CSDT2.CSD_TYP_DESCE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT4.CSD_TYP_DESCE <> CSDT4.CSD_TYP_DESCF THEN CSDT4.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT4.CSD_TYP_DESCE <> CSDT4.CSD_TYP_DESCF THEN CSDT4.CSD_TYP_DESCE
        ELSE CSDT4.CSD_TYP_DESCE
      END
  END AS ADV_SITE_CSD_TYP_DESC,


--ADV SITE FULL_PLACE (for ORD/SBPD/MOB)
--This accounts for differences between English and French.
  CASE
    WHEN EP2.PLACE_NAME is not null then CONCAT (EP2.PLACE_NAME, ', ')
    WHEN EP2.PLACE_NAME is null and EP4.PLACE_NAME is not null then CONCAT (EP4.PLACE_NAME, ', ')
    ELSE NULL
  END ||''||CASE
    WHEN CSDT2.CSD_TYP_DESCE is not null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT2.CSD_TYP_DESCE <> CSDT2.CSD_TYP_DESCF THEN CSDT2.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT2.CSD_TYP_DESCE <> CSDT2.CSD_TYP_DESCF THEN CSDT2.CSD_TYP_DESCE
        ELSE CSDT2.CSD_TYP_DESCE
      END
    WHEN CSDT2.CSD_TYP_DESCE is null then
      CASE
        WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and CSDT4.CSD_TYP_DESCE <> CSDT4.CSD_TYP_DESCF THEN CSDT4.CSD_TYP_DESCF
        WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and CSDT4.CSD_TYP_DESCE <> CSDT4.CSD_TYP_DESCF THEN CSDT4.CSD_TYP_DESCE
        ELSE CSDT4.CSD_TYP_DESCE
      END
  END AS FULL_ADV_SITE_PLACE,


--ADV SITE PSTL_CDE (for ORD/SBPD/MOB)
  CASE
    WHEN EC_ADD2.PSTL_CDE is not null then EC_ADD2.PSTL_CDE
    ELSE EC_ADD4.PSTL_CDE
  END AS ADV_SITE_PSTL_CDE,


--ELECTORS LISTED VALUES.
--Now derived from a table derived by Jessica Lachance. ELECTOR_COUNT_BY_PD_ID_20240423.xlsx
    EA_PEC.ELECTOR_COUNT



--TABLE JOINS
FROM
  ecdba.REDISTRIBUTION REDIST

--JOIN Electoral District
  LEFT JOIN ecdba.ELECTORAL_DISTRICT EDistrict on
    REDIST.RDSTRBTN_ID = EDistrict.RDSTRBTN_ID

--JOIN PROVINCE
  LEFT JOIN ecdba.PROVINCE PROV on
    EDistrict.PRVNC_ID= PROV.PROVINCE_ID

--JOIN ELECTORAL EVENT
  LEFT JOIN ECDBA.ED_ELCTRL_EVENT EDEE on
    EDistrict.ED_ID = EDEE.ED_ID

--JOIN POLL
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

--JOIN SITE_POLLING_STATION FOR ORD & SBPD
  LEFT JOIN SITES_ADMIN.SITE_POLLING_STATION S_PS on
    PLL.PD_ID = S_PS.PD_ID

--JOIN SITE_LOCATION FOR ORD & SBPD
  left join SITES_ADMIN.SITE_LOCATION S_L1 on
    S_PS.LCTN_ID = S_L1.LCTN_ID

--JOIN SITE_ADV_POLL_STATION  FOR ORD_ADV & SBPD_ADV
  LEFT JOIN SITES_ADMIN.SITE_ADV_POLL_STATION S_ADV_PS on
    S_PS.SITE_ADV_POLL_STN_ID = S_ADV_PS.SITE_ADV_POLL_STN_ID

--JOIN SITE_LOCATION 2 FOR ORD_ADV & SBPD_ADV
  left join SITES_ADMIN.SITE_LOCATION S_L2 on
    S_ADV_PS.LCTN_ID = S_L2.LCTN_ID

--JOIN MOBILE_POLL_PLACE for MOB
  LEFT JOIN MOBILE_POLL_PLACE MPP on
    PLL.PD_ID = MPP.PD_ID

--JOIN SITE_LOCATION 3 for MOB
  left join SITES_ADMIN.SITE_LOCATION S_L3 on
    MPP.LCTN_ID = S_L3.LCTN_ID

--JOIN SITE_ADV_POLL_STATION for MOB_ADV
  LEFT JOIN SITES_ADMIN.SITE_ADV_POLL_STATION S_ADV_PS2 on
    MPP.SITE_ADV_POLL_STN_ID = S_ADV_PS2.SITE_ADV_POLL_STN_ID

--JOIN SITE_LOCATION 4 for MOB_ADV
  left join SITES_ADMIN.SITE_LOCATION S_L4 on
    S_ADV_PS2.LCTN_ID = S_L4.LCTN_ID

--JOINING ORD SITES

--JOIN ORD SITE_ED_ELCTRL_EVENT
  LEFT JOIN SITES_ADMIN.SITE_ED_ELCTRL_EVENT SEEE1 on
    S_L1.SITE_ED_ELCTRL_EVENT_ID = SEEE1.SITE_ED_ELCTRL_EVENT_ID

--JOIN ORD SITES
  LEFT JOIN SITES_ADMIN.SITE SIT1 on
    SEEE1.SITE_ID = SIT1.SITE_ID

--JOIN ORD SITE_ADDRESS with subquery
  LEFT JOIN ( select SAQuery1.SITE_ADDRESS_ID, SAQuery1.ADDRESS_TYP, SAQuery1.SITE_ID, SAQuery1.SITE_PHYSICAL_ADDRESS_ID from SITES_ADMIN.SITE_ADDRESS SAQuery1 where SAQuery1.ADDRESS_TYP in 'CIVIC' ) SA1 on
    SIT1.SITE_ID = SA1.SITE_ID

--JOIN ORD EC_ADDRESS
  LEFT JOIN ECDBA.EC_ADDRESS EC_ADD1 on
    SA1.SITE_PHYSICAL_ADDRESS_ID = EC_ADD1.ADDRESS_ID

--JOIN ORD EC_STREET
  LEFT JOIN ECDBA.EC_STREET EC_ST1 on
    EC_ADD1.STREET_ID = EC_ST1.STREET_ID

--JOIN ORD STREET_DIRECTION
  LEFT JOIN ECDBA.STREET_DIRECTION SD1 on
    EC_ST1.ST_DRCTN_CDE = SD1.ST_DRCTN_CDE

--JOIN ORD EC_PLACE
  LEFT JOIN ECDBA.EC_PLACE EP1 on
    EC_ST1.PLACE_ID = EP1.PLACE_ID

--JOIN ORD CENSUS SUBDIVISION
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD1 on
    EP1.PLACE_ID = CSD1.PLACE_ID

--JOIN ORD CSD_TYPE
  LEFT JOIN ECDBA.CSD_TYPE CSDT1 on
    CSD1.CSD_TYP_ID = CSDT1.CSD_TYP_ID

--JOINING ORD_ADV SITES

--JOIN ORD_ADV SITE_ED_ELCTRL_EVENT
  LEFT JOIN SITES_ADMIN.SITE_ED_ELCTRL_EVENT SEEE2 on
    S_L2.SITE_ED_ELCTRL_EVENT_ID = SEEE2.SITE_ED_ELCTRL_EVENT_ID

--JOIN ORD_ADV SITE
  LEFT JOIN SITES_ADMIN.SITE SIT2 on
    SEEE2.SITE_ID = SIT2.SITE_ID

--JOIN ORD_ADV SITE_ADDRESS with subquery
  LEFT JOIN ( select SAQuery2.SITE_ADDRESS_ID, SAQuery2.ADDRESS_TYP, SAQuery2.SITE_ID, SAQuery2.SITE_PHYSICAL_ADDRESS_ID from SITES_ADMIN.SITE_ADDRESS SAQuery2 where SAQuery2.ADDRESS_TYP in 'CIVIC' ) SA2 on
    SIT2.SITE_ID = SA2.SITE_ID

--JOIN ORD_ADV EC_ADDRESS
  LEFT JOIN ECDBA.EC_ADDRESS EC_ADD2 on
    SA2.SITE_PHYSICAL_ADDRESS_ID = EC_ADD2.ADDRESS_ID

--JOIN ORD_ADV EC_STREET
  LEFT JOIN ECDBA.EC_STREET EC_ST2 on
    EC_ADD2.STREET_ID = EC_ST2.STREET_ID

--JOIN ORD_ADV STREET_DIRECTION
  LEFT JOIN ECDBA.STREET_DIRECTION SD2 on
    EC_ST2.ST_DRCTN_CDE = SD2.ST_DRCTN_CDE

--JOIN ORD_ADV EC_PLACE
  LEFT JOIN ECDBA.EC_PLACE EP2 on
    EC_ST2.PLACE_ID = EP2.PLACE_ID

--JOIN ORD_ADV CENSUS SUBDIVISION
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD2 on
    EP2.PLACE_ID = CSD2.PLACE_ID

--JOIN ORD_ADV CSD_TYPE
  LEFT JOIN ECDBA.CSD_TYPE CSDT2 on
    CSD2.CSD_TYP_ID = CSDT2.CSD_TYP_ID

--JOINING MOB SITES

--JOIN MOB SITE_ED_ELCTRL_EVENT
  LEFT JOIN SITES_ADMIN.SITE_ED_ELCTRL_EVENT SEEE3 on
    S_L3.SITE_ED_ELCTRL_EVENT_ID = SEEE3.SITE_ED_ELCTRL_EVENT_ID

--JOIN MOB SITE
  LEFT JOIN SITES_ADMIN.SITE SIT3 on
    SEEE3.SITE_ID = SIT3.SITE_ID

--JOIN MOB SITE_ADDRESS with subquery
  LEFT JOIN ( select SAQuery3.SITE_ADDRESS_ID, SAQuery3.ADDRESS_TYP, SAQuery3.SITE_ID, SAQuery3.SITE_PHYSICAL_ADDRESS_ID from SITES_ADMIN.SITE_ADDRESS SAQuery3 where SAQuery3.ADDRESS_TYP in 'CIVIC' ) SA3 on
    SIT3.SITE_ID = SA3.SITE_ID

--JOIN MOB EC_ADDRESS
  LEFT JOIN ECDBA.EC_ADDRESS EC_ADD3 on
    SA3.SITE_PHYSICAL_ADDRESS_ID = EC_ADD3.ADDRESS_ID

--JOIN MOB EC_STREET
  LEFT JOIN ECDBA.EC_STREET EC_ST3 on
    EC_ADD3.STREET_ID = EC_ST3.STREET_ID

--JOIN MOB STREET_DIRECTION
  LEFT JOIN ECDBA.STREET_DIRECTION SD3 on
    EC_ST3.ST_DRCTN_CDE = SD3.ST_DRCTN_CDE
--JOIN MOB EC_PLACE
  LEFT JOIN ECDBA.EC_PLACE EP3 on
    EC_ST3.PLACE_ID = EP3.PLACE_ID

--JOIN MOB CENSUS SUBDIVISION
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD3 on
    EP3.PLACE_ID = CSD3.PLACE_ID

--JOIN MOB CSD_TYPE
  LEFT JOIN ECDBA.CSD_TYPE CSDT3 on
    CSD3.CSD_TYP_ID = CSDT3.CSD_TYP_ID

--JOINING MOB ADV SITES

--JOIN MOB ADV SITE_ED_ELCTRL_EVENT
  LEFT JOIN SITES_ADMIN.SITE_ED_ELCTRL_EVENT SEEE4 on
    S_L4.SITE_ED_ELCTRL_EVENT_ID = SEEE4.SITE_ED_ELCTRL_EVENT_ID

--JOIN MOB ADV SITE
  LEFT JOIN SITES_ADMIN.SITE SIT4 on
    SEEE4.SITE_ID = SIT4.SITE_ID

--JOIN MOB ADV SITE_ADDRESS with subquery
  LEFT JOIN ( select SAQuery4.SITE_ADDRESS_ID, SAQuery4.ADDRESS_TYP, SAQuery4.SITE_ID, SAQuery4.SITE_PHYSICAL_ADDRESS_ID from SITES_ADMIN.SITE_ADDRESS SAQuery4 where SAQuery4.ADDRESS_TYP in 'CIVIC' ) SA4 on
    SIT4.SITE_ID = SA4.SITE_ID

--JOIN MOB ADV EC_ADDRESS
  LEFT JOIN ECDBA.EC_ADDRESS EC_ADD4 on
    SA4.SITE_PHYSICAL_ADDRESS_ID = EC_ADD4.ADDRESS_ID

--JOIN MOB ADV EC_STREET
  LEFT JOIN ECDBA.EC_STREET EC_ST4 on
    EC_ADD4.STREET_ID = EC_ST4.STREET_ID

--JOIN MOB ADV STREET_DIRECTION
  LEFT JOIN ECDBA.STREET_DIRECTION SD4 on
    EC_ST4.ST_DRCTN_CDE = SD4.ST_DRCTN_CDE

--JOIN MOB ADV EC_PLACE
  LEFT JOIN ECDBA.EC_PLACE EP4 on
    EC_ST4.PLACE_ID = EP4.PLACE_ID

--JOIN MOB ADV CENSUS SUBDIVISION
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD4 on
    EP4.PLACE_ID = CSD4.PLACE_ID

--JOIN MOB ADV CSD_TYPE
  LEFT JOIN ECDBA.CSD_TYPE CSDT4 on
    CSD4.CSD_TYP_ID = CSDT4.CSD_TYP_ID



--JOIN PD ELECTOR COUNT
 LEFT JOIN EGD_ADMIN.PD_ELECTOR_COUNT EA_PEC on
PLL.PD_ID = EA_PEC.PD_ID and MPP.MOBILE_POLL_STN_ID  = EA_PEC.MOBILE_POLL_STN_ID
--Now derived from a table derived by Jessica Lachance. ELECTOR_COUNT_BY_PD_ID_20240423.xlsx


--SBPD JOIN INFORMATION

--JOIN SBPD Data
  LEFT JOIN ECDBA.SBPD_POLL_PLACE SBPDPP on
   PLL.PD_ID = SBPDPP.PD_ID

  LEFT JOIN ECDBA.EC_ADDRESS   EC_ADD5 on
   SBPDPP.ADDRESS_ID = EC_ADD5.ADDRESS_ID

--JOIN SBPD EC_STREET
  LEFT JOIN ECDBA.EC_STREET EC_ST5 on
    EC_ADD5.STREET_ID = EC_ST5.STREET_ID

--JOIN SBPD STREET_DIRECTION
  LEFT JOIN ECDBA.STREET_DIRECTION SD5 on
    EC_ST5.ST_DRCTN_CDE = SD5.ST_DRCTN_CDE

--JOIN SBPD EC_PLACE
  LEFT JOIN ECDBA.EC_PLACE EP5 on
    EC_ST5.PLACE_ID = EP5.PLACE_ID

--JOIN SBPD CENSUS SUBDIVISION
  LEFT JOIN ECDBA.CENSUS_SUBDIVISION CSD5 on
    EP5.PLACE_ID = CSD5.PLACE_ID

--JOIN SBPD CSD_TYPE
  LEFT JOIN ECDBA.CSD_TYPE CSDT5 on
    CSD5.CSD_TYP_ID = CSDT5.CSD_TYP_ID

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
--REDIST.RDSTRBTN_CRNT_IND = 'Y'
--EDEE.CRNT_IND ='Y'
EDEE.ELCTRL_EVENT_ID  = '88'
  and PLL.ADVANCE_POLL_IND = 'N'
  --and PLL.VOID_IND = 'N'
  and PLL.PD_NBR <> 999
  --and PLL.PD_NBR >499 and PLL.PD_NBR < 600
  and EDistrict.ED_CODE in ED_LIST_HERE

order by
  EDEE.EVENT_ED_CODE, PLL.PD_NBR, PLL.PD_NBR_SFX
