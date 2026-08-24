import csv
import os
from .base_loader import BaseLoader
from .document import Document

class CSVLoader(BaseLoader):
    def __init__(
        self, 
        delimiter: str =',',
        encoding: str ='utf-8',
        quotechar='"',
        has_header=True,
        columns=None
    ):
        self.delimiter = delimiter
        self.encoding=encoding
        self.quotechar= quotechar
        self.has_header = has_header
        self.columns = columns

    def load(self, path):
        self.validate_file(path)
        raw_data = self.read_csv(path)

        if not raw_data:
            return []

        if self.has_header:
            self.validate_columns(raw_data)

        clean_data = self.normalize_values(raw_data)
        documents = self.rows_to_documents(clean_data, path)
        return documents
        
    def validate_file(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Critical error: File missing at '{path}'")
        if os.path.getsize(path) == 0:
            raise ValueError(f"Critical Error: File at '{path}' is empty")

    def read_csv(self, path):
        with open(path, mode='r', encoding=self.encoding) as f:
            if self.has_header:
                reader = csv.DictReader(f, delimiter=self.delimiter, quotechar=self.quotechar)
                return [dict(row) for row in reader]
            else:
                reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
                return [{"column_"+str(i):val for i, val in enumerate(row)} for row in reader]
            
    def validate_columns(self, data):
        if not self.columns or not data:
            return

        first_row_keys = data[0].keys()
        missing_cols = [col for col in self.columns if col not in first_row_keys]
        if missing_cols:
            raise KeyError(f"Missing required columns in CSV: {missing_cols}")

    def rows_to_documents(self, data, path):
        documents = []

        for row_number, row in enumerate(data, start=1):
            if self.columns:
                row = {col: row[col] for col in self.columns}

            text = "\n".join(
                f"{key}: {value}" 
                for key, value in row.items() if value is not None
            )

            documents.append(
                Document(
                    text=text,
                    metadata={
                        "source": str(path),
                        "type": "csv",
                        "row": row_number
                    }
                )
            )
        return documents
    
    def normalize_values(self, rows):
        normalized = []
        for row in rows:
            clean_row = {}
            for key, val in row.items():
                clean_val = val.strip() if isinstance(val, str) else val
                if clean_val in ("", "NA", "N/A", "null", "None"):
                    clean_row[key] = None 
                else: 
                    clean_row[key]= clean_val
            normalized.append(clean_row)
        return normalized