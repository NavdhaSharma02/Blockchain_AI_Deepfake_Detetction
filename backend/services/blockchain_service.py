"""
Blockchain Service
Handles interaction with the MediaRegistry smart contract
"""

import json
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

class BlockchainService:
    """Service for blockchain operations using Web3.py"""
    
    def __init__(self):
        """Initialize Web3 connection and contract"""
        self.rpc_url = os.getenv('POLYGON_RPC_URL', 'https://rpc-mumbai.maticvigil.com/')
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Load contract ABI
        abi_path = os.path.join(os.path.dirname(__file__), '../../contracts/MediaRegistry_abi.json')
        
        if os.path.exists(abi_path):
            with open(abi_path, 'r') as f:
                self.contract_abi = json.load(f)
        else:
            self.contract_abi = None
        
        # Initialize contract instance if address is available
        if self.contract_address and self.contract_abi:
            self.contract = self.web3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
        else:
            self.contract = None
    
    def is_connected(self) -> bool:
        """Check if connected to blockchain"""
        return self.web3.is_connected()
    
    def verify_media(self, media_hash: str) -> Dict[str, Any]:
        """
        Check if media hash exists in blockchain registry
        
        Args:
            media_hash: SHA-256 hash of the media
            
        Returns:
            Dictionary with verification results
        """
        if not self.contract:
            return {
                "verified": False,
                "exists": False,
                "error": "Contract not initialized. Please deploy the smart contract first."
            }
        
        try:
            # Call the verifyMedia function (view function, no transaction)
            exists = self.contract.functions.verifyMedia(media_hash).call()
            
            if exists:
                # Get detailed media info
                media_info = self.contract.functions.getMediaInfo(media_hash).call()
                
                return {
                    "verified": True,
                    "exists": True,
                    "media_hash": media_info[0],
                    "uploader": media_info[1],
                    "timestamp": media_info[2],
                    "metadata": media_info[3],
                    "message": "Media is registered on blockchain"
                }
            else:
                return {
                    "verified": False,
                    "exists": False,
                    "message": "Media not found in blockchain registry"
                }
        
        except Exception as e:
            return {
                "verified": False,
                "exists": False,
                "error": f"Blockchain verification failed: {str(e)}"
            }
    
    def register_media(self, media_hash: str, metadata: str = "") -> Dict[str, Any]:
        """
        Register media hash on blockchain
        
        Args:
            media_hash: SHA-256 hash of the media
            metadata: Additional metadata (JSON string)
            
        Returns:
            Dictionary with registration results
        """
        if not self.contract:
            return {
                "success": False,
                "error": "Contract not initialized"
            }
        
        if not self.private_key:
            return {
                "success": False,
                "error": "Private key not configured"
            }
        
        try:
            # Set up account
            account = self.web3.eth.account.from_key(self.private_key)
            
            # Check if already registered
            exists = self.contract.functions.verifyMedia(media_hash).call()
            if exists:
                return {
                    "success": False,
                    "error": "Media already registered on blockchain"
                }
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.registerMedia(
                media_hash,
                metadata
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.web3.eth.gas_price,
            })
            
            # Sign and send transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "gas_used": tx_receipt.gasUsed,
                "message": "Media successfully registered on blockchain"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Registration failed: {str(e)}"
            }
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get statistics about the registry"""
        if not self.contract:
            return {"error": "Contract not initialized"}
        
        try:
            count = self.contract.functions.getRegisteredCount().call()
            return {
                "total_registered": count,
                "network": "Polygon Mumbai Testnet",
                "connected": self.is_connected()
            }
        except Exception as e:
            return {"error": str(e)}
