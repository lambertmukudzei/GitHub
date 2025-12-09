# This is my Dataset class - it represents a dataset for data science
# student ID: M01061702
class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, rows: int, 
                 columns: int, uploaded_by: str, upload_date: str, created_at: str):
        # Private attributes (start with __) to protect the data
        
        self.__id = dataset_id          # Unique ID number for the dataset
        self.__name = name              # Name of the dataset (e.g., "Customer Sales Data")
        self.__rows = rows              # Number of rows (data points) in the dataset
        self.__columns = columns        # Number of columns (features/variables) in the dataset
        self.__uploaded_by = uploaded_by # Who uploaded the dataset
        self.__upload_date = upload_date # When the dataset was uploaded
        self.__created_at = created_at   # When the dataset record was created
    
    # Getter methods - safe way to access the private data
    
    def get_id(self) -> int:
        """Get the dataset ID number"""
        return self.__id
    
    def get_name(self) -> str:
        """Get the dataset name"""
        return self.__name
    
    def get_rows(self) -> int:
        """Get the number of rows in the dataset"""
        return self.__rows
    
    def get_columns(self) -> int:
        """Get the number of columns in the dataset"""
        return self.__columns
    
    def get_uploaded_by(self) -> str:
        """Get who uploaded the dataset"""
        return self.__uploaded_by
    
    def get_upload_date(self) -> str:
        """Get when the dataset was uploaded"""
        return self.__upload_date
    
    def get_created_at(self) -> str:
        """Get when the dataset record was created"""
        return self.__created_at
    
    # String representation - how the dataset appears when printed
    
    def __str__(self) -> str:
        """Show dataset in a readable format"""
        return f"Dataset {self.__id}: {self.__name} ({self.__rows} rows, {self.__columns} cols)"