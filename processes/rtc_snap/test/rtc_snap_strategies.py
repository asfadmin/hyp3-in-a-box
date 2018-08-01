from hypothesis import strategies as st

import asf_granule_util as gu


def granules():
    return st.from_regex(gu.SentinelGranule.pattern_exact)


def rtc_example_files():
    g = 'S1B_IW_GRDH_1SDV_20170731T100601_20170731T100626_006730_00BD74_1D4A'
    base = f'{g}-PREDORB-30m-rtc-s1tbx'

    return [
        f"{base}/ESA_citation.txt",
        f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVH.tif",
        f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV_large.png",
        f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV.png",
        f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV.tif"
    ]


def rtc_output():
    g = 'S1B_IW_GRDH_1SDV_20170731T100601_20170731T100626_006730_00BD74_1D4A'
    base = f'{g}-PREDORB-30m-rtc-s1tbx'

    return [
        [
            f"{base}/ESA_citation.txt",
            f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVH.tif",
            f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV_large.png",
            f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV.png",
            f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV.tif"
        ],
        f"{base}/{g}_OB_CAL_SF_ML_TF_TC_GVV.png"
    ]
