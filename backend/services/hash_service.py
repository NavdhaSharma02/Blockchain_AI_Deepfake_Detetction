"""
Hash Service
Generates SHA-256 hashes for media files
"""

import hashlib
from pathlib import Path
from typing import Union

class HashService:
    """Service for generating cryptographic hashes of media files"""
    
    @staticmethod
    def generate_file_hash(file_path: Union[str, Path]) -> str:
        """
        Generate SHA-256 hash of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hexadecimal string representation of the hash
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    @staticmethod
    def generate_bytes_hash(file_bytes: bytes) -> str:
        """
        Generate SHA-256 hash from bytes
        
        Args:
            file_bytes: File content as bytes
            
        Returns:
            Hexadecimal string representation of the hash
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_bytes)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def verify_file_integrity(file_path: Union[str, Path], expected_hash: str) -> bool:
        """
        Verify file integrity by comparing hashes
        
        Args:
            file_path: Path to the file
            expected_hash: Expected hash value
            
        Returns:
            True if hashes match, False otherwise
        """
        actual_hash = HashService.generate_file_hash(file_path)
        return actual_hash == expected_hash
