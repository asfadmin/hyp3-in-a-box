from hypothesis import strategies as st

import hyp3_events


def get_notify_only_strategy():
    return st.builds(
        hyp3_events.NotifyOnlyEvent,
        address=st.emails(),
        subject=st.text(),
        additional_info=st.fixed_dictionaries({
            'name': st.text(),
            'value': st.text()
        }),
        browse_url=get_url_strategy(),
        download_url=get_url_strategy()
    )


def get_url_strategy():
    return st.from_regex(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


def get_new_granule_strategy():
    return st.builds(
        hyp3_events.NewGranuleEvent,
        name=st.text(),
        polygon=cmr_polygon_list(),
        download_url=get_url_strategy()
    )


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


print(cmr_polygon_list().example())

strategies = {
    hyp3_events.NotifyOnlyEvent: get_notify_only_strategy(),
    hyp3_events.NewGranuleEvent: get_new_granule_strategy()
}
