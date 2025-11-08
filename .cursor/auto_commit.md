# Auto-Commit Workflow for Cursor

**Purpose:** Automatically commit after every completion and provide status updates

---

## 🔄 Auto-Commit After Completion

After completing any work, automatically:

1. **Stage all changes**
2. **Commit with descriptive message**
3. **Push to remote**
4. **Generate status report**

---

## 📊 Status Report Format

After every completion, provide:

1. **What Was Completed**
   - List of changes made
   - Files modified/created
   - Features added/fixed

2. **Current Status**
   - Current phase
   - Critical path items
   - Active tasks
   - System status

3. **Next Steps**
   - Immediate actions
   - This week priorities
   - Blockers (if any)

4. **Understanding**
   - Where we are in the project
   - What phase we're in
   - What's next on critical path

---

## 🎯 Always Include

### After Every Completion:
- ✅ **Summary of work completed**
- 📊 **Current status update**
- 🎯 **Next steps**
- 🚨 **Critical path items**
- 📈 **Phase status**
- 🔧 **System status**

### Status Template:
```
✅ ========================================
✅ WORK COMPLETED
✅ ========================================
✅
✅ Completed:
✅ - [List of changes]
✅
✅ Current Status:
✅ - Phase: [Current phase]
✅ - Critical Path: [Items]
✅ - Active Tasks: [Tasks]
✅
✅ Next Steps:
✅ 1. [Immediate action]
✅ 2. [This week priority]
✅
✅ ========================================
```

---

## 🔄 Workflow

1. **Complete work** → Make changes
2. **Auto-commit** → Run `./scripts/auto_commit.sh "message"`
3. **Generate status** → Run `./scripts/generate_status.sh`
4. **Provide update** → Show status to user
5. **Next steps** → Outline what's next

---

## 📝 Commit Message Format

Always use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Refactoring
- `test:` - Tests
- `chore:` - Maintenance

Example:
```bash
./scripts/auto_commit.sh "feat: Add MCP tool registry support to observer agent"
```

---

**Remember:** Always commit, always provide status, always show next steps! 🐝✨

