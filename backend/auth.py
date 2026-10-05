"""
Role-Based Access Control and Authentication Engine
Dr. B.R. Ambedkar Digital Heritage Archive

Roles:
- visitor: Public read-only access
- student: Authenticated with "{STUDENT}". Access to standard OCR & contribution (5MB limit).
- researcher: Authenticated with "RESEARCHER" / "RESEARCHER2026". Full access to Kraken OCR, custom models, and database document relations.
"""

from typing import Dict, Any, Optional

STUDENT_PASSCODES = {"{STUDENT}", "STUDENT", "student", "{student}"}
RESEARCHER_PASSCODES = {"RESEARCHER", "RESEARCHER2026", "researcher", "{RESEARCHER}"}

ROLE_PERMISSIONS = {
    "visitor": {
        "can_search": True,
        "can_view_timeline": True,
        "can_view_ideas": True,
        "can_use_standard_ocr": False,
        "can_use_kraken_ocr": False,
        "can_add_relations": False,
        "can_upload_models": False,
        "max_file_size_mb": 0
    },
    "student": {
        "can_search": True,
        "can_view_timeline": True,
        "can_view_ideas": True,
        "can_use_standard_ocr": True,
        "can_use_kraken_ocr": False,
        "can_add_relations": False,
        "can_upload_models": False,
        "max_file_size_mb": 5
    },
    "researcher": {
        "can_search": True,
        "can_view_timeline": True,
        "can_view_ideas": True,
        "can_use_standard_ocr": True,
        "can_use_kraken_ocr": True,
        "can_add_relations": True,
        "can_upload_models": True,
        "max_file_size_mb": 5
    }
}

def authenticate_user(passcode: str, requested_role: Optional[str] = None) -> Dict[str, Any]:
    cleaned = (passcode or "").strip()
    
    if cleaned in RESEARCHER_PASSCODES or (requested_role == "researcher" and cleaned in RESEARCHER_PASSCODES):
        return {
            "authenticated": True,
            "role": "researcher",
            "role_display": "Researcher / Scholar",
            "permissions": ROLE_PERMISSIONS["researcher"]
        }
        
    if cleaned in STUDENT_PASSCODES or (requested_role == "student" and cleaned in STUDENT_PASSCODES):
        return {
            "authenticated": True,
            "role": "student",
            "role_display": "Student",
            "permissions": ROLE_PERMISSIONS["student"]
        }
        
    if not cleaned or requested_role == "visitor":
        return {
            "authenticated": True,
            "role": "visitor",
            "role_display": "Visitor",
            "permissions": ROLE_PERMISSIONS["visitor"]
        }
        
    return {
        "authenticated": False,
        "role": "visitor",
        "role_display": "Visitor",
        "error": "Invalid passcode provided for requested role.",
        "permissions": ROLE_PERMISSIONS["visitor"]
    }

def verify_role_access(role: str, required_capability: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["visitor"])
    return perms.get(required_capability, False)
