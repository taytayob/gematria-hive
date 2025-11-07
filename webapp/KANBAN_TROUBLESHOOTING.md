# Kanban Board Troubleshooting

## Common Issues and Solutions

### 1. "Failed to fetch tasks" Error

**Symptoms:**
- Kanban board shows error message
- Tasks don't load
- Network errors in browser console

**Solutions:**

#### Check Backend API is Running
```bash
# Check if FastAPI server is running on port 8000
curl http://localhost:8000/api/tasks

# Or check if process is running
lsof -ti:8000
```

**Start the backend:**
```bash
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
python kanban_api.py
```

#### Check Supabase Configuration
If using Supabase directly, verify credentials in `.env`:
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

#### Check API Base URL
Verify `VITE_API_BASE` in `.env` or check `vite.config.ts` proxy settings:
```env
VITE_API_BASE=/api
```

### 2. CORS Errors

**Symptoms:**
- Browser console shows CORS errors
- Requests fail with CORS policy errors

**Solution:**
Ensure `kanban_api.py` has CORS middleware configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Empty Kanban Board

**Symptoms:**
- Board loads but shows no tasks
- All columns are empty

**Solutions:**

#### Check Database Connection
```bash
# Test database connection
python -c "from task_manager import get_task_manager; tm = get_task_manager(); print(tm.get_all_tasks())"
```

#### Create Sample Tasks
```bash
# Create a test task via API
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"content": "Test task", "status": "pending"}'
```

### 4. Drag and Drop Not Working

**Symptoms:**
- Can't drag tasks between columns
- Tasks don't move when dropped

**Solutions:**

#### Check Browser Console
Look for JavaScript errors that might prevent drag/drop

#### Verify Task Status Update
Check if status update API call is working:
```bash
curl -X PATCH "http://localhost:8000/api/tasks/{task_id}/status?status=in_progress"
```

### 5. Statistics Not Loading

**Symptoms:**
- Statistics panel shows "Loading statistics..."
- Statistics never appear

**Solutions:**

#### Check Statistics Endpoint
```bash
curl http://localhost:8000/api/statistics
```

#### Verify Task Manager
Ensure task manager is properly initialized and can calculate statistics

### 6. Filter Panel Not Working

**Symptoms:**
- Filters don't apply
- Tasks don't filter by phase/role/priority

**Solutions:**

#### Check Phases/Roles/Priorities Endpoints
```bash
curl http://localhost:8000/api/phases
curl http://localhost:8000/api/roles
curl http://localhost:8000/api/priorities
```

#### Verify Enhanced Task Manager
Ensure enhanced task manager is being used (has phase/role/priority support)

### 7. Task Dialog Not Opening

**Symptoms:**
- Click "New Task" or "Edit" but dialog doesn't open
- No error messages

**Solutions:**

#### Check Browser Console
Look for React errors or component mounting issues

#### Verify Dialog Component
Ensure `TaskDialog` component is properly imported and rendered

### 8. Network Error: Unable to Connect

**Symptoms:**
- Error message: "Network error: Unable to connect to API"
- Backend server not responding

**Solutions:**

#### Start Backend Server
```bash
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
python kanban_api.py
```

#### Check Port Configuration
Verify backend is running on correct port (default: 8000)

#### Check Vite Proxy
Verify `vite.config.ts` has correct proxy configuration:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## Quick Diagnostic Commands

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if tasks endpoint works
curl http://localhost:8000/api/tasks

# Check if frontend dev server is running
curl http://localhost:3000

# Check for port conflicts
lsof -ti:8000  # Backend
lsof -ti:3000  # Frontend
```

## Still Not Working?

1. **Check Browser Console** - Look for JavaScript errors
2. **Check Network Tab** - See what API calls are failing
3. **Check Backend Logs** - Look for Python errors
4. **Verify Environment Variables** - Check `.env` file
5. **Restart Both Servers** - Sometimes a restart fixes issues

## Getting Help

If none of these solutions work:
1. Check browser console for specific error messages
2. Check backend logs for Python errors
3. Verify all dependencies are installed
4. Check network connectivity
5. Try clearing browser cache

