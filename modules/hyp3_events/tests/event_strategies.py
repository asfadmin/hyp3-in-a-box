from hypothesis import strategies as st

import hyp3_events

url_strategy = st.from_regex('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')


notify_only_event = st.builds(
    hyp3_events.NotifyOnlyEvent,
    address=st.emails(),
    subject=st.text(),
    additional_info=st.fixed_dictionaries({
        'name': st.text(),
        'value': st.text()
    }),
    browse_url=url_strategy,
    download_url=url_strategy
)


strategies = {
    hyp3_events.NotifyOnlyEvent: notify_only_event
}
