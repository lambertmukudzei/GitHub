# This is my SecurityIncident class - it represents a cybersecurity incident
# student ID: M01061702
class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""
    
    def __init__(self, incident_id: int, timestamp: str, severity: str, 
                 category: str, status: str, description: str, created_at: str):
        # All attributes are private (start with __)
        # This protects the incident data from being changed accidentally
        
        self.__id = incident_id           # Unique ID number for this incident
        self.__timestamp = timestamp      # When the incident happened
        self.__severity = severity        # How serious: Critical, High, Medium, Low
        self.__category = category        # Type: Malware, Phishing, DDoS, etc.
        self.__status = status            # Current status: Open, In Progress, Resolved
        self.__description = description  # What happened
        self.__created_at = created_at    # When this record was created
    
    # Getter methods, these let us safely access the private data
    
    def get_id(self) -> int:
        """Get the incident ID number"""
        return self.__id
    
    def get_timestamp(self) -> str:
        """Get when the incident happened"""
        return self.__timestamp
    
    def get_severity(self) -> str:
        """Get the severity level (Critical, High, Medium, Low)"""
        return self.__severity
    
    def get_category(self) -> str:
        """Get the incident category (Malware, Phishing, etc.)"""
        return self.__category
    
    def get_status(self) -> str:
        """Get current status (Open, In Progress, Resolved)"""
        return self.__status
    
    def get_description(self) -> str:
        """Get description of what happened"""
        return self.__description
    
    def get_created_at(self) -> str:
        """Get when this record was created"""
        return self.__created_at
    
    # Setter method - only status can be updated (it's the only one that changes)
    
    def update_status(self, new_status: str) -> None:
        """Change the incident status (Open → In Progress → Resolved)"""
        self.__status = new_status
    
    # Helper method, this converts severity text to a number for analysis
    
    def get_severity_level(self) -> int:
        """Return an integer severity level (higher = more severe)"""
        mapping = {
            "low": 1,        # Least severe
            "medium": 2,     # Medium severity
            "high": 3,       # High severity  
            "critical": 4,   # Most severe
        }
        # Convert severity to lowercase and get number, default to 0 if not found
        return mapping.get(self.__severity.lower(), 0)
    
    # String representation - how the incident appears when printed
    
    def __str__(self) -> str:
        """Show incident in a readable format"""
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__category}"