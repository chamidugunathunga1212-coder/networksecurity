from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file: str
    test_file: str