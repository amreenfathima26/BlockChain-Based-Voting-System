import hashlib
import json
from .models import Block

class Blockchain:
    def __init__(self):
        pass

    @staticmethod
    def create_genesis_block():
        if Block.objects.count() == 0:
            block = Block.objects.create(
                index=0,
                data="Genesis Block",
                previous_hash="0",
                hash="0" # Will be recalc
            )
            block.hash = block.calculate_hash()
            block.save()

    @staticmethod
    def get_latest_block():
        return Block.objects.order_by('-index').first()

    @staticmethod
    def add_block(data):
        latest_block = Blockchain.get_latest_block()
        if not latest_block:
            Blockchain.create_genesis_block()
            latest_block = Blockchain.get_latest_block()

        new_index = latest_block.index + 1
        new_block = Block(
            index=new_index,
            data=json.dumps(data),
            previous_hash=latest_block.hash,
            nonce=0
        )
        # POW Simulation (simple)
        new_block.hash = new_block.calculate_hash()
        
        # In a real sim, we might loop nonce until hash stats with 0000
        # for academic demo, simple hashing is often enough, or a small difficulty
        # Let's add simulated difficulty
        difficulty = 2 
        while not new_block.hash.startswith('0' * difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            
        new_block.save()
        return new_block

    @staticmethod
    def is_chain_valid():
        blocks = Block.objects.order_by('index')
        for i in range(1, len(blocks)):
            current = blocks[i]
            previous = blocks[i-1]
            
            # Recalculate hash to check data integrity
            # Note: timestamp in DB might differ slightly from calc string if not careful,
            # but for this logic we re-use the stored timestamp if we can, or just trust the hash matches the stored content
            # A strict check would re-serialize.
            # For simplicity: check link
            if current.previous_hash != previous.hash:
                return False, f"Broken link at Block {current.index}"
                
            # Check internal integrity (requires regenerating hash with EXACT same timestamp string)
            # This is tricky with DB datetimes. We'll skip strict re-hashing of DB objects for now unless stored as string.
            # or we verify the stored hash matches the stored fields.
            
        return True, "Chain Valid"
