# System Architecture Documentation: SecureVote Blockchain Voting System

## 1. Executive Summary
SecureVote is a hybrid blockchain-based voting system designed to ensure **transparency**, **immutability**, and **security** in digital elections. It leverages a custom Python-based blockchain for recording votes while utilizing a relational database (SQLite/PostgreSQL) for user management and metadata. The system features a role-based access control (RBAC) model (Voter, Candidate, Admin, Superadmin) and integrates AI for vote analytics and fraud prevention simulation.

## 2. Technology Stack

### Backend
-   **Framework:** Django 5.x (Python)
-   **Database:** SQLite (Development) / PostgreSQL (Production-ready)
-   **Blockchain Engine:** Custom Python implementation with SHA-256 hashing and logical block linking.
-   **AI Integration:** Groq API (LLaMA-3 model) for chatbot and fraud analysis.

### Frontend
-   **Template Engine:** Django Templates (DTL)
-   **Styling:** Custom CSS with Glassmorphism design system (no external CSS frameworks like Bootstrap/Tailwind to ensure custom aesthetic).
-   **Interactivity:** Vanilla JavaScript, Chart.js for analytics.

## 3. Core Modules

### 3.1. Blockchain Ledger (`core/blockchain.py`)
The backbone of the voting integrity.
-   **Block Structure:** Index, Timestamp, Data (Vote details), Previous Hash, Hash, Nonce.
-   **Consensus:** Proof-of-Work (simulated via nonce difficulty) or Proof-of-Authority (Admin validation).
-   **Immutability:** Each block's hash depends on the previous block's hash. Changing a past vote invalidates the entire chain.
-   **Genesis Block:** Created automatically upon system initialization.

### 3.2. User Management & RBAC
-   **Voter:** Can view active elections and cast one vote per election.
-   **Candidate:** Can view their own realtime vote stats and campaign status.
-   **Admin:** Manages elections (Create, Start, End), approves candidates/voters.
-   **Superadmin (God Mode):**
    -   Global system configuration (Site name, API keys).
    -   User management (Create/Delete/Approve/Password Reset).
    -   Simulation controls (Voter participation, System load).

### 3.3. Voting Mechanism
1.  **Eligibility Check:** Core logic asserts `Vote.objects.filter(user=request.user, election=election).exists()` is False.
2.  **Transaction Creation:** A vote is packaged into a JSON object including Election ID, Candidate ID, and an anonymous Voter Hash.
3.  **Block Mining:** `Blockchain.add_block(data)` hashes the transaction and appends it to the chain.
4.  **Off-Chain Sync:** A `Vote` record is saved in the relational DB for easy UI querying (preventing double-voting) but the *truth* is in the `Block` model.

## 4. Security Implementation

-   **SHA-256 Hashing:** Used for linking blocks.
-   **Session Security:** "God Mode" requires strict session re-authentication. Navigating away locks the mode.
-   **Password Hashing:** Django's PBKDF2 with SHA-256 password hasher.
-   **Visibility Toggles:** Password fields in God Mode are masked by default.
-   **CSRF Protection:** All forms protected by Django CSRF tokens.

## 5. Database Schema (Key Models)

-   `CustomUser` (AbstractUser): Fields for `role`, `is_approved`.
-   `Election`: Title, Description, Start/End Dates, Active Status.
-   `Candidate`: Link to User, Link to Election, Party, Manifesto, Approval Status.
-   `Block`: Index, Hash, Prev_Hash, Data (JSON), Timestamp.
-   `Vote`: Link to User, Link to Election, Block Index (Foreign Key-like reference to Ledger).
-   `SiteConfiguration` (Singleton): Global settings, API keys, Theme toggles.

## 6. AI Agent (`ai_agent`)
-   **Context:** System prompt includes election details and blockchain stats.
-   **Function:** Answers voter queries ("Who is winning?", "How do I vote?") using RAG-like context injection.
-   **Provider:** Groq API (High-performance inference).

## 7. Future Scalability
-   **Migration to Distributed Ledger:** The current `Block` model can be replaced or bridged to Ethereum/Polygon Web3 providers.
-   **Homomorphic Encryption:** To allow tallying encrypted votes without decryption.
-   **Biometric Auth:** Integation with webcam/fingerprint sensors for voter verification.
