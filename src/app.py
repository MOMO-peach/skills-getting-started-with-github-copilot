"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball": {
        "description": "Learn basketball skills and compete in games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu", "aiden@mergington.edu"]
    },
    "Soccer": {
        "description": "Train and compete in soccer matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["ryan@mergington.edu", "james@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art forms including painting, drawing, and sculpture",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "charlotte@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Learn musical instruments and perform in ensembles",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "grace@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore advanced scientific concepts",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation skills and compete in debate competitions",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["lucas@mergington.edu", "hannah@mergington.edu"]
    }
}

# Additional activities
activities.update({
    "Basketball Team": {
        "description": "Competitive basketball team practices and games",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["tyler@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Casual and competitive soccer matches",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["anna@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["lucy@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater workshops and school productions",
        "schedule": "Fridays, 4:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Problem solving and competition preparation",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["sophia@mergington.edu"]
    },
    "Science Club": {
        "description": "Experiments, projects, and science fairs",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Validate activity capacity
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
