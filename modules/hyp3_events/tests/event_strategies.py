from hypothesis import strategies as st

import hyp3_events
import asf_granule_util as gu


def get_start_event_strategy():
    return st.builds(
        hyp3_events.StartEvent,
        granule=granules_strategty(),
        address=st.emails(),
        username=st.text(),
        subscription=st.text(),
        output_files=st.lists(st.text())
    )


def get_notify_only_strategy():
    return st.builds(
        hyp3_events.NotifyOnlyEvent,
        address=st.emails(),
        subject=st.text(),
        additional_info=st.lists(
            st.fixed_dictionaries({
                'name': st.text(),
                'value': st.text()
            })
        ),
        browse_url=get_url_strategy(),
        download_url=get_url_strategy()
    )


def get_url_strategy():
    return st.from_regex(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


def get_new_granule_strategy():
    return st.builds(
        hyp3_events.NewGranuleEvent,
        name=granules_strategty(),
        polygon=cmr_polygon_list(),  # pylint: disable=E1120
        download_url=get_url_strategy(),
        browse_url=get_url_strategy()
    )


def granules_strategty():
    return st.from_regex(gu.SentinelGranule.pattern_exact)


def floats_with_range(min_val, max_val):
    return st.floats(
        min_value=min_val, max_value=max_val,
        allow_nan=False, allow_infinity=False
    )


@st.composite
def cmr_polygon_list(draw):
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


strategies = {
    hyp3_events.NotifyOnlyEvent: get_notify_only_strategy(),
    hyp3_events.NewGranuleEvent: get_new_granule_strategy(),
    hyp3_events.StartEvent: get_start_event_strategy()
}
