# Frontend Editor Coordination Plan

**Date:** January 6, 2025  
**Status:** 🚀 In Progress

---

## 🎯 Objective

Coordinate the integration of enhanced kanban features into the React webapp and add a code editor component for metadata editing, ensuring seamless coordination between the HTML kanban board and React webapp.

---

## 📊 Current State

### HTML Kanban Board (`kanban_enhanced.html`)
- ✅ **Location:** Root directory
- ✅ **Status:** Fully functional with all enhanced features
- ✅ **Features:**
  - Phases, roles, priorities, tags
  - Resources, metadata, dependencies
  - Filter panel
  - Drag-and-drop
  - Statistics panel
- ✅ **API:** Connected to `kanban_api.py` on port 8000

### React Webapp (`webapp/`)
- ✅ **Location:** `webapp/` directory
- ✅ **Status:** Basic kanban board implemented
- ⚠️ **Missing:** Enhanced features (phases, roles, tags, metadata editor)
- ✅ **Tech Stack:**
  - React 18 + TypeScript
  - shadcn/ui components
  - TanStack Query
  - TanStack Router
- ✅ **API:** Connected to `kanban_api.py` via proxy

---

## 🚀 Integration Plan

### Phase 1: Update API Client ✅
- [x] Add phases, roles, priorities endpoints
- [x] Update Statistics interface
- [x] Add Phase and Role interfaces

### Phase 2: Add Code Editor Component
- [ ] Install Monaco Editor or CodeMirror
- [ ] Create MetadataEditor component
- [ ] Integrate into TaskDialog

### Phase 3: Update TaskDialog Component
- [ ] Add phase selector
- [ ] Add role selector
- [ ] Add priority selector
- [ ] Add tags input
- [ ] Add resources input
- [ ] Add metadata editor
- [ ] Add progress slider
- [ ] Add due date picker

### Phase 4: Update KanbanCard Component
- [ ] Display phase badge
- [ ] Display role badge
- [ ] Display priority badge
- [ ] Display tags
- [ ] Display progress bar
- [ ] Display resources count

### Phase 5: Add Filter Panel
- [ ] Create FilterPanel component
- [ ] Add phase filter
- [ ] Add role filter
- [ ] Add priority filter
- [ ] Add tag filter
- [ ] Integrate into KanbanBoard

### Phase 6: Update Queries
- [ ] Add usePhases hook
- [ ] Add useRoles hook
- [ ] Add usePriorities hook
- [ ] Update useTasks to support filters

---

## 🛠️ Code Editor Options

### Option 1: Monaco Editor (VS Code Editor)
**Pros:**
- ✅ Industry standard (VS Code editor)
- ✅ Excellent TypeScript support
- ✅ Rich features (autocomplete, syntax highlighting)
- ✅ JSON validation built-in
- ✅ Large community

**Cons:**
- ⚠️ Larger bundle size (~2MB)
- ⚠️ More complex setup

**Package:** `@monaco-editor/react`

### Option 2: CodeMirror 6
**Pros:**
- ✅ Lightweight (~200KB)
- ✅ Modern architecture
- ✅ Highly customizable
- ✅ Good performance

**Cons:**
- ⚠️ Smaller community than Monaco
- ⚠️ Less features out of the box

**Package:** `@uiw/react-codemirror`

### Option 3: Simple Textarea with JSON Validation
**Pros:**
- ✅ Zero dependencies
- ✅ Simple implementation
- ✅ Small bundle size

**Cons:**
- ⚠️ No syntax highlighting
- ⚠️ No autocomplete
- ⚠️ Poor UX for complex JSON

---

## 🎯 Recommendation: Monaco Editor

**Reasoning:**
1. **Best UX:** Rich editing experience for metadata
2. **JSON Support:** Built-in JSON validation and formatting
3. **TypeScript:** Full TypeScript support aligns with project
4. **Future-Proof:** Can be extended for other code editing needs

**Implementation:**
```bash
npm install @monaco-editor/react
```

---

## 📋 Implementation Checklist

### Step 1: Install Dependencies
- [ ] Install Monaco Editor
- [ ] Update package.json

### Step 2: Create MetadataEditor Component
- [ ] Create `src/components/ui/metadata-editor.tsx`
- [ ] Implement Monaco Editor wrapper
- [ ] Add JSON validation
- [ ] Add error handling

### Step 3: Update TaskDialog
- [ ] Add all enhanced fields
- [ ] Integrate MetadataEditor
- [ ] Add form validation
- [ ] Update API calls

### Step 4: Update KanbanCard
- [ ] Display enhanced fields
- [ ] Add badges for phase/role/priority
- [ ] Add progress bar
- [ ] Add tags display

### Step 5: Add Filter Panel
- [ ] Create FilterPanel component
- [ ] Add filter controls
- [ ] Integrate with useTasks hook
- [ ] Update KanbanBoard

### Step 6: Testing
- [ ] Test all enhanced features
- [ ] Test code editor
- [ ] Test filters
- [ ] Test API integration

---

## 🔄 Coordination Strategy

### HTML Kanban vs React Webapp

**Current Approach:**
- Both use the same API (`kanban_api.py`)
- Both support enhanced features
- HTML kanban: Standalone, browser-ready
- React webapp: Modern, component-based

**Coordination:**
1. **Shared API:** Both use same backend
2. **Feature Parity:** React webapp should match HTML kanban features
3. **Data Consistency:** Both read/write to same database
4. **User Choice:** Users can choose which interface to use

**Future:**
- Consider consolidating to React webapp only
- Or keep both for different use cases

---

## 📝 Next Steps

1. **Install Monaco Editor**
   ```bash
   cd webapp
   npm install @monaco-editor/react
   ```

2. **Create MetadataEditor Component**
   - Implement Monaco Editor wrapper
   - Add JSON validation
   - Style with Tailwind

3. **Update TaskDialog**
   - Add all enhanced fields
   - Integrate MetadataEditor
   - Update form handling

4. **Update KanbanCard**
   - Display enhanced fields
   - Add badges and progress

5. **Add Filter Panel**
   - Create FilterPanel component
   - Integrate with KanbanBoard

6. **Test Integration**
   - Test all features
   - Verify API integration
   - Check browser compatibility

---

## 🎉 Expected Outcome

After completion:
- ✅ React webapp supports all enhanced features
- ✅ Code editor for metadata editing
- ✅ Filter panel for advanced filtering
- ✅ Enhanced task cards with all metadata
- ✅ Seamless coordination with HTML kanban
- ✅ Consistent API usage across both interfaces

---

**Status:** Ready to implement! 🚀

