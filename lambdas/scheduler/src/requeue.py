from hyp3_events import StartEvent
import dispatch

# this is using the Flask route decorator, should check to make sure
# the hyp3 API doesn't have a better way to receive the command via hyperlink
@app.route('/queue/')
def requeue_view(granule_name: str, sub_id: str, user_id: str, script_path: str, output_type: str):
    requeue(granule_name, sub_id, user_id, script_path, output_type)


def requeue(granule_name: str, sub_id: str, user_id: str, script: str, output_type: str):


    re_start_event = StartEvent(
        granule=granule_name,
        user_id=user_id,
        sub_id=sub_id,
        output_patterns=output_type,
        script_path=script,
        additional_info=[
            {
                'name': 'Requeued',
                'value': 'True'
            }
        ]
    )

    dispatch.all_events([re_start_event])