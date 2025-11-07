# Troubleshooting Guide

## Issue: App doesn't work on port 3000

### Check if port is in use:
```bash
lsof -ti:3000
```

If something is using port 3000, kill it:
```bash
kill -9 $(lsof -ti:3000)
```

Or change the port in `vite.config.ts`:
```typescript
server: {
  port: 3001, // Change to different port
}
```

### Check if dependencies are installed:
```bash
cd webapp
npm install
```

### Check if dev server starts:
```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

## Issue: No menu/sidebar on kanban page

The sidebar should be visible on ALL pages since it's in the Layout component.

### Verify Layout is working:
1. Check browser console for errors
2. Check if sidebar is hidden by CSS
3. Check if router is working

### Check browser console:
Open DevTools (F12) and check:
- Any JavaScript errors?
- Any CSS issues?
- Is the sidebar element in the DOM?

### Verify sidebar is rendering:
1. Open browser DevTools
2. Inspect element
3. Look for `<aside>` element with class "fixed top-0 left-0"
4. Check if it has `display: none` or is hidden

### Check if router is working:
1. Navigate to different pages
2. Check if URL changes
3. Check if content changes

## Common Issues

### 1. Dependencies not installed
**Solution:**
```bash
cd webapp
rm -rf node_modules package-lock.json
npm install
```

### 2. TypeScript errors
**Solution:**
```bash
npm run build
```
Check for TypeScript errors and fix them.

### 3. Vite cache issues
**Solution:**
```bash
rm -rf node_modules/.vite
npm run dev
```

### 4. Port already in use
**Solution:**
```bash
# Kill process on port 3000
kill -9 $(lsof -ti:3000)

# Or change port in vite.config.ts
```

### 5. Backend not running
**Solution:**
```bash
# Start backend in separate terminal
python kanban_api.py
```

### 6. CORS issues
**Solution:**
Check `kanban_api.py` has CORS enabled:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Debug Steps

1. **Check if app starts:**
   ```bash
   npm run dev
   ```

2. **Check browser console:**
   - Open DevTools (F12)
   - Look for errors

3. **Check network tab:**
   - See if API calls are working
   - Check for 404 errors

4. **Check elements:**
   - Inspect sidebar element
   - Check if it's in the DOM
   - Check CSS classes

5. **Check router:**
   - Navigate between pages
   - Check if URL changes
   - Check if content updates

## Still Having Issues?

1. Clear browser cache
2. Try incognito mode
3. Check browser console for errors
4. Verify all dependencies are installed
5. Check if backend is running
6. Restart dev server

