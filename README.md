# Ajura AI Backend

This is the Flask backend for Ajura AI. Deploy it on Render or Replit.

## Deployment Steps

### **1. Upload to GitHub**
1. Create a new GitHub repository.
2. Upload all the files in this folder to the repository.

### **2. Deploy on Render**
1. Go to [Render.com](https://render.com/).
2. Create a **New Web Service**.
3. Connect it to your GitHub repo.
4. Select **Python 3.9+**.
5. Set the **Start Command**: `python server.py`.
6. Add an **Environment Variable**:
   - Key: `SECRET_WEBHOOK`
   - Value: `<your-secret-key>`
7. Click **Deploy**.

### **3. Deploy on Replit (Alternative)**
1. Create a new **Replit Python project**.
2. Upload `server.py` and `requirements.txt`.
3. Run `pip install -r requirements.txt`.
4. Start the server: `python server.py`.

## API Endpoints
- **`/api/chat`** → Chat with Ajura AI (POST request with JSON `{ "text": "message" }`).
- **`/api/webhook`** → Hidden update system (requires `Authorization` header).

---
✅ **Now connect your frontend to this backend!**
