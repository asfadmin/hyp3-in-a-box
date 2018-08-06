from hypothesis import strategies as st

import hyp3_events
import asf_granule_util as gu


def new_granule_events():
    return st.builds(
        hyp3_events.NewGranuleEvent,
        name=granules(),
        polygon=cmr_polygon_lists(),  # pylint: disable=E1120
        download_url=urls(),
        browse_url=urls()
    )


def start_events():
    return st.builds(
        hyp3_events.StartEvent,
        granule=granules(),
        address=st.emails(),
        username=st.text(),
        subscription=st.text(),
        output_patterns=st.lists(st.text()),
        script_path=st.text()
    )


def email_events():
    return st.builds(
        hyp3_events.EmailEvent,
        user_id=st.integers(),
        sub_id=st.integers(),
        granule_name=granules(),
        additional_info=st.lists(
            st.fixed_dictionaries({
                'name': st.text(),
                'value': st.text()
            })
        ),
        browse_url=urls(),
        download_url=urls()
    )


def urls():
    return st.from_regex(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


def granules():
    return st.from_regex(gu.SentinelGranule.pattern_exact)


def floats_with_range(min_val, max_val):
    return st.floats(
        min_value=min_val, max_value=max_val,
        allow_nan=False, allow_infinity=False
    )


@st.composite
def cmr_polygon_lists(draw):
    lons = floats_with_range(-180, 180)
    lats = floats_with_range(-90, 90)

    list_len = draw(st.integers(min_value=4, max_value=15))

    lon_lists = st.lists(lons, min_size=list_len, max_size=list_len)
    lat_lists = st.lists(lats, min_size=list_len, max_size=list_len)

    lon_vals = draw(lon_lists)
    lat_vals = draw(lat_lists)

    polygon = []
    for lon, lat in zip(lon_vals, lat_vals):
        polygon += [lon, lat]

    return polygon + polygon[:2]
