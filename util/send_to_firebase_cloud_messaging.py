# from firebase_admin import messaging, auth


def send_to_firebase_cloud_messaging(token, title, body, deep_link):
    pass
    # registration_token = token
    # message = messaging.Message(
    #     notification=messaging.Notification(
    #         title=title,
    #         body=body,
    #     ),
    #     token=registration_token,
    #     data={
    #         "url": deep_link,
    #     },
    # )
    # try:
    #     response = messaging.send(message)
    #     print(f"Successfully sent message: {response}")
    # except Exception as e:
    #     print("예외가 발생했습니다.", e)
