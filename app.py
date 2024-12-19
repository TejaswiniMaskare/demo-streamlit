import streamlit as st
st.write("hello")
import base64
import json
from datetime import datetime

def decode_token(token):
    try:
        # Split the JWT and decode the payload
        base64_url = token.split('.')[1]
        base64_bytes = base64_url + '=' * (-len(base64_url) % 4)  # Fix padding
        decoded_bytes = base64.urlsafe_b64decode(base64_bytes)
        payload = json.loads(decoded_bytes.decode('utf-8'))

        # Parse the required fields
        my_jwt_data = {
            "token": token,
            "role": payload.get("http://schemas.microsoft.com/ws/2008/06/identity/claims/role", ""),
            "employeeId": payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier", ""),
            "firstName": payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname", ""),
            "lastName": payload.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname", ""),
            "expiry": datetime.fromtimestamp(payload["exp"]).strftime("%Y-%m-%d %H:%M:%S") if "exp" in payload else None,
            "isTeamLead": payload.get("isTeamLead", "false").lower() == "true",
            "isProjectLead": payload.get("isProjectLead", "false").lower() == "true",
            "isReviewer": payload.get("isReviewer", "false").lower() == "true",
            "isFeedbackProvided": payload.get("isFeedbackProvided", "false").lower() == "true"
        }

        return my_jwt_data

    except (IndexError, ValueError, KeyError, jwt.DecodeError) as e:
        print(f"Error decoding token: {e}")
        return None

def get_token_data(token):
    decoded_obj = decode_token(token)
    if decoded_obj:
        return json.dumps(decoded_obj, indent=4)
    return None


query_params = st.query_params

# Extract the 'userId' parameter
user_id = query_params.get('userId', [None])[0]

# Display the extracted value
if user_id:
    # st.write(f"User ID: {user_id}")
    st.write(get_token_data(st.query_params['userId']))
else:
    st.write("No User ID provided.")


# st.write(st.query_params['userId'])