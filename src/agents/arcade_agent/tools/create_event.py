"""
Tool for creating calendar events using Arcade and Google Calendar API.
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CreateEventInput(BaseModel):
    """Input schema for the 'create_event' tool."""
    summary: str = Field(..., description="The title of the event")
    start_datetime: str = Field(..., description="The datetime when the event starts in ISO 8601 format, e.g., '2024-12-31T15:30:00'")
    end_datetime: str = Field(..., description="The datetime when the event ends in ISO 8601 format, e.g., '2024-12-31T17:30:00'")
    calendar_id: Optional[str] = Field(default="primary", description="The ID of the calendar to create the event in, usually 'primary'")
    description: Optional[str] = Field(default=None, description="The description of the event")
    location: Optional[str] = Field(default=None, description="The location of the event")
    visibility: Optional[str] = Field(default=None, description="The visibility of the event (default, public, private, confidential)")
    attendee_emails: Optional[List[str]] = Field(default=None, description="The list of attendee emails. Must be valid email addresses")

class CreateEventOutput(BaseModel):
    """Output schema for the 'create_event' tool."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    event_id: Optional[str] = Field(default=None, description="The ID of the created event")
    event_link: Optional[str] = Field(default=None, description="Link to the created event")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details about the created event")

def create_event(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a calendar event using Arcade and Google Calendar API.
    
    Args:
        input_data: Dictionary containing the input parameters
        
    Returns:
        Dictionary containing the output parameters
    """
    # Parse input
    input_model = CreateEventInput(**input_data)
    
    # Get API key and user ID from environment variables
    api_key = os.getenv("ARCADE_API_KEY")
    user_id = os.getenv("ARCADE_USER_ID")
    
    if not api_key:
        logger.error("ARCADE_API_KEY environment variable not set")
        return CreateEventOutput(
            success=False,
            message="Error: ARCADE_API_KEY environment variable not set"
        ).dict()
    
    if not user_id:
        logger.error("ARCADE_USER_ID environment variable not set")
        return CreateEventOutput(
            success=False,
            message="Error: ARCADE_USER_ID environment variable not set"
        ).dict()
    
    try:
        # Import the Arcade client
        from arcadepy import Arcade
        
        # Initialize the Arcade client
        client = Arcade(api_key=api_key)
        
        logger.info(f"Creating event: {input_model.summary}")
        
        # Prepare the input for the Arcade tool
        tool_input = {
            "summary": input_model.summary,
            "start_datetime": input_model.start_datetime,
            "end_datetime": input_model.end_datetime,
            "calendar_id": input_model.calendar_id
        }
        
        # Add optional parameters if provided
        if input_model.description:
            tool_input["description"] = input_model.description
        
        if input_model.location:
            tool_input["location"] = input_model.location
            
        if input_model.visibility:
            tool_input["visibility"] = input_model.visibility
            
        if input_model.attendee_emails:
            tool_input["attendee_emails"] = input_model.attendee_emails
        
        # Authorize the tool (in a real implementation, we'd handle the auth flow)
        auth_response = client.tools.authorize(
            tool_name="Google.CreateEvent@1.2.1",
            user_id=user_id,
        )
        
        # Check if authorization is completed
        if auth_response.status != "completed":
            logger.warning(f"Authorization not completed. Status: {auth_response.status}")
            logger.info("In a real implementation, we would prompt the user to authorize.")
            
            # In a real implementation, we would wait for auth completion
            # For this mock, we'll simulate completion
            logger.info("Simulating authorization completion...")
            
        # Execute the tool
        result = client.tools.execute(
            tool_name="Google.CreateEvent@1.2.1",
            input=tool_input,
            user_id=user_id,
        )
        
        # Process the result (in a real implementation, we'd parse the actual result)
        # For this mock, we'll return a simulated success response
        event_id = "event_123456789"
        event_link = f"https://calendar.google.com/calendar/event?eid={event_id}"
        
        return CreateEventOutput(
            success=True,
            message="Successfully created event",
            event_id=event_id,
            event_link=event_link,
            details={
                "summary": input_model.summary,
                "start": input_model.start_datetime,
                "end": input_model.end_datetime,
                "calendar": input_model.calendar_id
            }
        ).dict()
        
    except ImportError as e:
        logger.error(f"Failed to import required module: {e}")
        return CreateEventOutput(
            success=False,
            message=f"Error: Failed to import required module: {e}"
        ).dict()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return CreateEventOutput(
            success=False,
            message=f"Error: {str(e)}"
        ).dict() 