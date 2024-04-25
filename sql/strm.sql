SELECT
--  Redistribution Information
  REDIST.RDSTRBTN_ID, REDIST.RDSTRBTN_YEAR, REDIST.RDSTRBTN_CRNT_IND,
  --Province
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
  --ED Code, Electoral event
  EDistrict.ED_CODE,
 
  -- CASE
--    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN (REPLACE (EDistrict.ED_NAMEF, '--', '—')) ||' / '|| (REPLACE (EDistrict.ED_NAMEE, '--', '—'))
 --   WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN (REPLACE (EDistrict.ED_NAMEE, '--', '—')) ||' / '|| (REPLACE (EDistrict.ED_NAMEF, '--', '—'))
 --   ELSE (REPLACE (EDistrict.ED_NAMEE, '--', '—'))
 -- END AS ED_NAME_BIL,
 
 CASE
    WHEN EDistrict.ED_CODE > 24000 and EDistrict.ED_CODE< 24999 and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN EDistrict.ED_NAMEF ||' / '|| EDistrict.ED_NAMEE
    WHEN (EDistrict.ED_CODE < 24000 or EDistrict.ED_CODE> 24999) and EDistrict.ED_NAMEE <> EDistrict.ED_NAMEF THEN EDistrict.ED_NAMEE ||' / '|| EDistrict.ED_NAMEF
    ELSE EDistrict.ED_NAMEE
  END AS ED_NAME_BIL, 
  
  EDistrict.ED_ID, EDEE.ELCTRL_EVENT_ID,
  EDEE.ED_ELCTRL_EVENT_ID, EDEE.CRNT_IND, EDEE.EVENT_ED_CODE,
  --  PD Information
 CONCAT (CONCAT (PLL.PD_NBR, '-'), PLL.PD_NBR_SFX ) FULL_PD_NBR,
  PLL.PD_NBR, PLL.PD_NBR_SFX, PLL.PD_ID, MPP.MOBILE_POLL_STN_ID,
  --STRM Information
  STRM.TWNSHIP, STRM.RNGE, STRM.MRDN, STRM.SECTION, STRM.TRM_DESCE, STRM.TRM_DESCF, STRM.LAST_UPD_DT



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



where
  REDIST.RDSTRBTN_CRNT_IND = 'N'
--  and EDEE.CRNT_IND ='Y'
  and EDEE.ELCTRL_EVENT_ID = '88'
  and PLL.ADVANCE_POLL_IND = 'N'
  and PLL.VOID_IND = 'N'
  and PLL.PD_NBR <> 999
  and EDistrict.ED_CODE in ED_LIST_HERE

order by
  EDEE.EVENT_ED_CODE, PLL.PD_NBR, PLL.PD_NBR_SFX
