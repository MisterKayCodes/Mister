## Ground Rules for Refactoring (Like We Just Did)

Based on our successful refactoring, here are the **ground rules** that work for ANY codebase:

---

### Rule 1: Never Change Behavior While Refactoring

| Do | Don't |
|----|-------|
| Keep all endpoints exactly the same | Change API responses |
| Keep all function names the same | Rename things unnecessarily |
| Keep all imports working | Break existing dependencies |

---

### Rule 2: One Small Step at a Time

| Step | Action |
|------|--------|
| 1 | Find what depends on the file |
| 2 | Create new folder structure |
| 3 | Move ONE group of endpoints at a time |
| 4 | Test after each move |
| 5 | Fix imports immediately |

---

### Rule 3: Map Dependencies First

Before touching anything, answer:
1. What files IMPORT this file?
2. What endpoints does this file EXPORT?
3. What frontend pages CALL these endpoints?

---

### Rule 4: Create Helper Files for Shared Code

If multiple files use the same function, move it to a helper file.

---

### Rule 5: Keep Import Paths Clean

Use relative imports (`.`) only within the same folder. Use absolute imports for everything else.

---

### Rule 6: Test After Every Change

If it breaks, fix imports BEFORE moving the next file.

---

### Rule 7: Update the Main `__init__.py` Last

Only change this AFTER all files are moved and tested.

---

### Rule 8: Keep the Old File as Backup

Don't delete immediately. Delete only after everything works for a week.

---

### Rule 9: Name Files by Responsibility

One file = One responsibility.

---

### Rule 10: Document the New Structure

Create a `README.md` in the new folder.

---

## Golden Rule (Most Important)

> **Refactoring changes the STRUCTURE, not the BEHAVIOR.**

If the code behaves differently after refactoring, you did it wrong. Go back and fix imports.
