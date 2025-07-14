# 🛠️ Webhook Receiver with Flask & MongoDB

This repository contains a Python Flask application that receives GitHub webhook events (`push`, `pull_request`, and `merge`) and displays them in a live-updating UI.

---

## 📦 Features

- 📥 Receives GitHub webhook events via `/webhook/receiver`
- 📦 Stores event details in MongoDB (Atlas or local)
- 🌐 Displays the latest 10 events on a live-updating UI (`/webhook/`)
- 🔁 Auto-refreshes every 15 seconds to fetch new events
- 🔒 Supports local testing with `Ngrok` for public webhook URL
- ✅ Built as part of Techstax Developer Assessment (Jul 2025)

---
