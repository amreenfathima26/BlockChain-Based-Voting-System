# SecureVote: Project Documentation & User Manual

## 1. Project Overview
SecureVote is a next-generation decentralized voting application that combines the security of **Blockchain technology** with an intuitive, glassmorphism-styled web interface. It ensures that every vote is immutable, transparent, and verifiable, while providing distinct secure portals for Voters, Candidates, Administrators, and Superadmins.

---

## 2. System Credentials (Access Keys)
Use these credentials to access the different roles in the system.

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Superadmin (God)** | `admin` | `admin123` | Full system control, "God Mode" access, Site Config. |
| **Administrator** | `election_admin` | `admin123` | Manage elections, approve candidates, monitor polls. |
| **Candidate** | `candidate_01` | `pass123` | View campaign stats, check election status. |
| **Voter** | `voter_01` | `pass123` | Cast votes, chat with AI, view history. |

> **Note:** "God Mode" requires you to re-enter the Superadmin password (`admin123`) every time you access the secure dashboard.

---

## 3. Blockchain Implementation (The Core)

The system utilizes a custom Python-based blockchain engine to record votes. This is **not** a standard database table; it is a cryptographically linked ledger.

### 3.1 Data Structure
Each block contains:
-   **Index:** Position in the chain (e.g., Block #105).
-   **Timestamp:** Exact time of the transaction.
-   **Data Payload:** JSON object containing:
    -   `election_id`: The ID of the election.
    -   `candidate_id`: The ID of the recipient candidate.
    -   `voter_hash`: Anonymized SHA-256 hash of the voter's ID (ensures privacy).
-   **Previous Hash:** The digital signature of the *previous* block.
-   **Hash:** The digital signature of the *current* block (calculated from all above data).
-   **Nonce:** Proof-of-Work number.

### 3.2 How It Works
1.  **Vote Casting:** When a user votes, the system creates a transaction packet.
2.  **Hashing:** The system calculates a SHA-256 hash of the packet + the previous block's hash.
3.  **Chaining:** This new block is appended to the chain.
4.  **Immutability:** If a hacker tries to modify a past vote (Block #50), the hash of Block #50 changes. Since Block #51 contains Block #50's hash, Block #51 also changes, cascading to the end of the chain. This makes tampering immediately detectable.

### 3.3 Verification
-   **Block Explorer:** Users can view the raw blockchain ledger at `/ledger` to verify their vote exists on the chain.
-   **Chain Validatiy:** The Admin dashboard runs a real-time integrity check to ensure `Hash[i] == Hash(Block[i])`.

---

## 4. Project Folder Structure

A high-level overview of the codebase organization:

```text
secure_vote/
├── manage.py                   # Django CLI entry point
├── db.sqlite3                  # Relational Database (Users, Elections)
├── secure_vote/                # Project Settings
│   ├── settings.py             # Config (Apps, DB, Middleware)
│   └── urls.py                 # Main URL routing
├── core/                       # Core App (Users, Ledger, God Mode)
│   ├── blockchain.py           # ★ Custom Blockchain Engine
│   ├── models.py               # CustomUser, Block, SiteConfiguration
│   ├── views.py                # Admin/Superadmin Dashboards
│   └── urls.py                 # Auth routes
├── voting/                     # Voting App (Elections, Candidates)
│   ├── models.py               # Election, Candidate, Vote
│   ├── views.py                # Voter/Candidate Dashboards, Casting
│   └── forms.py                # Election creation forms
├── ai_agent/                   # AI App (Chatbot)
│   ├── utils.py                # Groq API Integration (LLaMA3)
│   └── views.py                # Chat API endpoints
└── templates/                  # HTML Frontend
    ├── base.html               # Main Layout (Glassmorphism design)
    ├── core/                   # Admin & Auth Templates
    │   ├── superadmin_dashboard.html # God Mode UI
    │   └── admin_dashboard.html      # Admin UI
    ├── voting/                 # Voting Templates
    │   ├── voter_dashboard.html      # Voter UI
    │   └── candidate_dashboard.html  # Analytics UI
    └── static/                 # CSS/JS Assets (if any)
```

---

## 5. Key Features Highlights

### 👑 God Mode (Superadmin)
-   **Access:** Restricted to Superusers with password re-entry presence.
-   **Capabilities:**
    -   **Global User Management:** Create, Delete, Approve users.
    -   **Password Reset:** Overwrite any user's password securely (Eye toggle included).
    -   **System Controls:** Toggle "Maintenance Mode" or "Stop New Registrations".
    -   **Simulation:** Adjust "Voter Turnout" and "System Load" stats for demos.

### 🤖 AI Agent Integration
-   **Powered By:** Groq API (LLaMA-3-70b-versatile).
-   **Functionality:**
    -   Context-aware answering of voter questions ("Who is ensuring security?").
    -   Real-time analysis of election trends (Simulated fraud detection).

### 🎨 Premium UI/UX
-   **Glassmorphism:** Translucent "frosted glass" cards using `backdrop-filter: blur`.
-   **Dynamic Themes:**
    -   **Admin:** Professional Slate/Blue theme.
    -   **Voter:** Trustworthy Emerald/Green theme.
    -   **Candidate:** Energetic Amber/Orange theme.
-   **Interactive Data:** Chart.js graphs for real-time election results.

---

## 6. Deployment & Running
1.  **Install Requirements:** `pip install -r requirements.txt`
2.  **Migrate DB:** `python manage.py migrate`
3.  **Run Server:** `python manage.py runserver`
4.  **Access:** Open `http://127.0.0.1:8000`

---
*© GV-Blockchain 2025 - Secure, Transparent, Immutable.*
