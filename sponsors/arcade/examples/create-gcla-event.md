CreateEvent
Enabled
Create a new event/meeting/sync/meetup in the specified calendar.


Toolkit: Google
Google.CreateEvent@1.2.1

Inputs
summary
The title of the event
Required
start_datetime
The datetime when the event starts in ISO 8601 format, e.g., '2024-12-31T15:30:00'.
Required
end_datetime
The datetime when the event ends in ISO 8601 format, e.g., '2024-12-31T17:30:00'.
Required
calendar_id
The ID of the calendar to create the event in, usually 'primary'.
Optional
description
The description of the event
Optional
location
The location of the event
Optional
visibility
The visibility of the event
OptionalOptions: default, public, private, confidential
attendee_emails
The list of attendee emails. Must be valid email addresses e.g., username@domain.com.
Optional

Output
Description: A dictionary containing the created event details
Available Modes: value, error
Value Type: json

Requirements
Provider:
google
Type: oauth2
Scopes: https://www.googleapis.com/auth/calendar.readonly, https://www.googleapis.com/auth/calendar.events

```python
from arcadepy import Arcade

API_KEY = "YOUR_API_KEY"
USER_ID = "YOUR_USER_ID"

client = Arcade()

# Authorize the tool
auth_response = client.tools.authorize(
    tool_name="Google.CreateEvent@1.2.1",
    user_id=USER_ID,
)

# Check if authorization is completed
if auth_response.status != "completed":
    print(f"Click this link to authorize: {auth_response.url}")

# Wait for the authorization to complete
auth_response = client.auth.wait_for_completion(auth_response)

if auth_response.status != "completed":
    raise Exception("Authorization failed")

print("🚀 Authorization successful!")

result = client.tools.execute(
    tool_name="Google.CreateEvent@1.2.1",
    input={
        "owner": "ArcadeAI",
        "name": "arcade-ai",
        "starred": "true",
        "summary": "language learning study session (lesson 1)",
        "start_datetime": "2025-05-02T15:30:00",
        "end_datetime": "2025-05-02T16:30:00"
    },
    user_id=USER_ID,
)

print(result)
```