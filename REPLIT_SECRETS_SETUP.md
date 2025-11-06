# Replit Secrets Setup for Supabase

**Purpose:** Configure environment variables for Supabase database access (Phase 2+)

**Last Updated:** November 6, 2025

---

## Why Use Replit Secrets?

✅ **Secure:** Encrypted storage, not visible in code  
✅ **Agent-accessible:** Replit Agent can use these automatically  
✅ **No git commits:** Secrets never get pushed to GitHub  
✅ **Easy rotation:** Update secrets without changing code  

**Don't use `.env` files in Replit** - they're not secure for production.

---

## Step 1: Access Replit Secrets

1. In your Replit project, look at the left sidebar
2. Click the **🔒 Secrets** icon (lock icon)
   - Or click **Tools** in sidebar → **Secrets**
3. The Secrets panel will open on the right side

---

## Step 2: Add Supabase Credentials

Click **+ Add new secret** and enter each of these:

### Secret 1: SUPABASE_URL

```
Key:   SUPABASE_URL
Value: https://your-project.supabase.co
```

**Where to find this:**
1. Go to [supabase.com](https://supabase.com)
2. Sign in and select your project
3. Click **Settings** (gear icon) → **API**
4. Copy **Project URL**

### Secret 2: SUPABASE_KEY

```
Key:   SUPABASE_KEY
Value: eyJhbGc...your-anon-key-here
```

**Where to find this:**
1. Same location: **Settings → API**
2. Under **Project API keys**, copy **anon/public** key
3. ⚠️ Use **anon** key for client-side, **service_role** only for server-side admin operations

### Secret 3: CLICKHOUSE_HOST (Phase 3+)

```
Key:   CLICKHOUSE_HOST
Value: your-clickhouse-host.com
```

Add this later when setting up ClickHouse analytics database.

### Secret 4: CLICKHOUSE_PASSWORD (Phase 3+)

```
Key:   CLICKHOUSE_PASSWORD
Value: your-secure-password
```

---

## Step 3: Verify Secrets in Code

Your Python code can now access these:

```python
import os
from dotenv import load_dotenv

# Load from .env (local dev in Cursor)
load_dotenv()

# Access secrets (works in both Replit and local)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(f"Connected to: {supabase_url}")  # Don't print the key!
```

**Test in Replit Shell:**

```bash
# This should print your Supabase URL
python -c "import os; print(os.getenv('SUPABASE_URL'))"
```

If it prints your URL, secrets are configured correctly! ✅

---

## Step 4: Agent Access

Replit Agent **automatically has access** to secrets you've added. When you ask Agent to:

- "Set up Supabase database"
- "Connect to Supabase"
- "Query the database"

Agent will use the `SUPABASE_URL` and `SUPABASE_KEY` you configured.

**No extra configuration needed!**

---

## Security Best Practices

### ✅ DO:

- Use **Secrets tool** for all sensitive data (API keys, passwords, tokens)
- Use **anon key** for client-side code
- Rotate keys every 90 days (or when compromised)
- Use different keys for dev vs. production (if you have multiple Repls)

### ❌ DON'T:

- Hardcode secrets in `app.py` or any file
- Commit `.env` files to git (already in `.gitignore`)
- Share secrets in chat/email (use Replit's Share Secrets feature)
- Use `service_role` key in client-side code (too powerful!)

---

## Troubleshooting

### Issue: "Secret not found" error

**Solution:**
1. Check spelling: Secret keys are **case-sensitive**
2. Restart your Repl (**Run** button or `Ctrl+R`)
3. Verify secret exists in Secrets panel

### Issue: Agent can't access secrets

**Solution:**
1. Make sure secrets are added in **Secrets panel** (not `.replit` file)
2. Restart the Repl
3. Ask Agent to "check environment variables for SUPABASE_URL"

### Issue: Works in Replit, not in Cursor

**Solution:**
- Replit Secrets are **only available in Replit**, not locally
- For local dev in Cursor, create `.env` file (see `CURSOR_SYNC_INSTRUCTIONS.md`)
- Keep `.env` in `.gitignore` (already configured)

---

## Secrets for Different Environments

### Replit (Development & Production)

Use **Replit Secrets** panel:
- `SUPABASE_URL`
- `SUPABASE_KEY`

### Cursor (Local Development)

Use `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGc...
```

### Keep Both in Sync

When you change a secret:
1. Update in **Replit Secrets** panel
2. Update in local `.env` file (Cursor)
3. Test in both environments

---

## Advanced: Sharing Secrets with Team

If you're working with a team:

1. **Don't commit secrets to git** (already prevented by `.gitignore`)
2. Use Replit's **Share Secrets** feature:
   - Click **Share** button in Replit
   - Enable **Share secrets with collaborators**
3. Or use a password manager (1Password, LastPass) to share `.env` file securely

---

## Phase 2 Checklist

Before starting Phase 2 (Database & Word Index):

- [ ] Supabase account created
- [ ] Project created in Supabase dashboard
- [ ] `SUPABASE_URL` added to Replit Secrets
- [ ] `SUPABASE_KEY` (anon) added to Replit Secrets
- [ ] Secrets verified with test script
- [ ] Local `.env` file created in Cursor (for local dev)

Once complete, you're ready to:
```bash
pip install supabase
```

And start building the database integration! 🚀

---

**Security Status:** 🔒 Encrypted  
**Agent Access:** ✅ Enabled  
**Git Safe:** ✅ Not committed  

🐝 Your secrets are secure! ✨
