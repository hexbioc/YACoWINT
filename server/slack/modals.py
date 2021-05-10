import json

from server import config
from server.storage.models import SlackUserSubscription


def subscription_modal(state_option=None, district_option=None, age_option=None):
    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Pick a state",
                        "emoji": True,
                    },
                    "action_id": "state_select",
                    **({"initial_option": state_option} if state_option else {}),
                }
            ],
        }
    ]

    if state_option is not None:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "external_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Pick a district",
                            "emoji": True,
                        },
                        "action_id": "district_select",
                        **(
                            {"initial_option": district_option}
                            if district_option
                            else {}
                        ),
                    }
                ],
            },
        )

    if district_option is not None and state_option is not None:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "static_select",
                        "placeholder": {"type": "plain_text", "text": "Age limit"},
                        "action_id": "age_select",
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "18-45"},
                                "value": "18",
                            },
                            {
                                "text": {"type": "plain_text", "text": "45+"},
                                "value": "45",
                            },
                        ],
                        **({"initial_option": age_option} if age_option else {}),
                    }
                ],
            },
        )

    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Select Region", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": blocks,
        "private_metadata": json.dumps(
            dict(
                state_option=state_option,
                district_option=district_option,
                age_option=age_option,
            )
        ),
    }

    if age_option is not None:
        view["submit"] = {"type": "plain_text", "text": "Subscribe", "emoji": True}
    return view


def successful_subscription_modal(subscription: SlackUserSubscription):
    response = (
        "Subscribed! You will be notified on Slack whenever an available slot is found"
        f" over the next {config.TRACK_WEEKS_DEFAULT} week(s) each day, in your"
        " chosen region. To unsubscribe from all notifications, run `/cowin unsub`."
    )

    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Success"},
        "close": {"type": "plain_text", "text": "Ok"},
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": response}}],
    }
