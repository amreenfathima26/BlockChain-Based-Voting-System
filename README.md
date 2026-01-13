# SecureVote: AI-Enhanced Blockchain Voting System

A secure, academic simulation of a blockchain-based voting system built with Django.

## 🚀 Key Features
- **Blockchain Core**: Simulates a distributed ledger where each vote is a block linked by SHA-256 hashes.
- **Role-Based Access**:
  - **Admin**: Approves users, manages elections, views the ledger.
  - **Candidate**: registers for elections, views analytics.
  - **Voter**: Casts immutable votes, chats with AI.
- **AI Assistant**: Integration with **GROQ API** to provide voters with real-time help and fraud alerts for admins.
- **Dynamic Dashboards**: Premium UI with Glassmorphism and Chart.js visualizations.

## 🛠️ Installation

1. **Clone the repository**
2. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variables** (Optional for full features)
   - `GROQ_API_KEY`: For AI features
   - `DB_NAME`, `DB_USER`, etc.: For PostgreSQL
4. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create Admin**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run Server**
   ```bash
   python manage.py runserver
   ```

## 📚 Academic Concepts Simulated
- **Immutability**: Once a block is saved, it cannot be changed.
- **Consensus**: Admin approval acts as a centralized 'Proof of Authority'.
- **Transparency**: The ledger is visible to admins (and can be exposed to public).
- **Security**: Hashing ensures any data tampering breaks the chain.

## 🔮 Future Scope
- Migrate from simulated blocks to Ethereum/Hyperledger.
- Implement true decentralized consensus (PoW/PoS).
- Mobile App using React Native.
