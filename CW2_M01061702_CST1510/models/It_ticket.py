# This is my ITTicket class, it represents a support ticket in an IT system
#student ID: M01061702
class ITTicket:
    """Represents an IT support ticket - like a help desk request."""
    
    def __init__(self, ticket_id: int, priority: str, description: str, 
                 status: str, assigned_to: str, created_at: str, 
                 resolution_time_hours: int, created_at_timestamp: str):
        # Private attributes (start with __) - protects the data
        
        self.__id = ticket_id  # Unique ticket number
        self.__priority = priority  # How urgent: Critical, High, Medium, Low
        self.__description = description  # What the problem is
        self.__status = status  # Current state: Open, In Progress, Closed, etc.
        self.__assigned_to = assigned_to  # Who is working on it
        self.__created_at = created_at  # When ticket was created (human readable)
        self.__resolution_time_hours = resolution_time_hours  # How long to fix (hours)
        self.__created_at_timestamp = created_at_timestamp  # Exact time created (for sorting)
    
    # Action methods, things we can do with a ticket
    
    def assign_to(self, staff: str) -> None:
        """Assign this ticket to a staff member"""
        self.__assigned_to = staff  # Change who it's assigned to
    
    def close_ticket(self) -> None:
        """Mark ticket as closed (finished)"""
        self.__status = "Closed"  # Change status to Closed
    
    # Getter methods which is a safe way to get the  ticket information
    
    def get_id(self) -> int:
        """Get the ticket ID number"""
        return self.__id
    
    def get_priority(self) -> str:
        """Get the priority level"""
        return self.__priority
    
    def get_description(self) -> str:
        """Get the problem description"""
        return self.__description
    
    def get_status(self) -> str:
        """Get the current status"""
        return self.__status
    
    def get_assigned_to(self) -> str:
        """Get who the ticket is assigned to"""
        return self.__assigned_to
    
    def get_created_at(self) -> str:
        """Get when the ticket was created"""
        return self.__created_at
    
    def get_resolution_time_hours(self) -> int:
        """Get how many hours it took to resolve"""
        return self.__resolution_time_hours
    
    # String representation - how the ticket appears when printed
    
    def __str__(self) -> str:
        """Show ticket in a readable format"""
        return (
            f"Ticket {self.__id}: {self.__description[:50]}... "  # First 50 chars of description
            f"[{self.__priority}] – {self.__status} (assigned to: {self.__assigned_to})"
        )