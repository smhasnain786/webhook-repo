# GitHub Webhook Event Tracker

This project tracks GitHub repository activity using **GitHub Webhooks** and displays it in a simple, modern UI.  
It listens for **Push** and **Pull Request** events, stores them in MongoDB, and shows them in near real-time.

This project was built as part of a technical assignment to demonstrate webhook handling, backend processing, and basic frontend updates.

---


## 🛠 Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB Atlas
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Webhook Provider:** GitHub
- **Local Exposure:** VS Code built-in Port Forwarding

---


---

## ⚙️ Running the Project Locally

1. Clone the repository
```bash
git clone https://github.com/smhasnain786/webhook-repo.git
cd webhook-repo
python run.py

---

## Webhook setup

1. The Flask server runs on localhost:5000
2. The port was exposed using VS Code’s built-in Port Forwarding
3. The generated public URL was added to GitHub Webhooks