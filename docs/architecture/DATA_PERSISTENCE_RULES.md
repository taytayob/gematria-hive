# Data Persistence Rules - System-Level Requirements

## Critical System Rule: ALL Data MUST Be Stored

**This is a non-negotiable system-level requirement.** Any agent that collects, scrapes, or processes data MUST store it in the database. Failure to do so wastes resources and violates the core principle of the system.

## Rule Enforcement

### 1. Browser Agent
- **REQUIREMENT**: All scraped pages MUST be stored in `scraped_content` table
- **ENFORCEMENT**: 
  - Browser agent automatically stores all scraped data
  - If storage fails, the entire operation fails
  - Status is set to "failed" if data cannot be persisted
- **VALIDATION**: Orchestrator validates that `pages_stored == pages_scraped`

### 2. Ingestion Agent
- **REQUIREMENT**: All ingested data MUST be stored in appropriate tables
- **ENFORCEMENT**: 
  - Ingestion agent validates storage success
  - Returns count of successfully stored items
  - Logs errors if storage fails

### 3. All Data-Collecting Agents
- **REQUIREMENT**: Any agent that collects data MUST store it
- **ENFORCEMENT**: 
  - Agents must have storage methods
  - Storage failures must cause operation failure
  - No silent data loss allowed

## Implementation Details

### Browser Agent Storage
```python
# System-level rule enforced in agents/browser.py
def _store_scraped_data(self, formatted_data: List[Dict], base_url: str) -> int:
    """
    SYSTEM-LEVEL RULE: This method MUST succeed or the entire operation fails.
    Data cannot be scraped without being stored - this wastes resources.
    """
    # Stores in scraped_content table
    # Returns count of stored items
    # Fails operation if storage fails
```

### Orchestrator Validation
```python
# System-level validation in agents/orchestrator.py
if pages_scraped > 0 and pages_stored == 0:
    logger.error("CRITICAL SYSTEM VIOLATION: Data loss occurred!")
    final_state["status"] = "failed"
```

## Database Schema

### scraped_content Table
- Stores all scraped web content
- Required fields: `url`, `title`, `content`, `source_site`
- Uses `upsert` to avoid duplicates (on conflict with `url`)

### gematria_words Table
- Stores all extracted words with gematria values
- Required fields: `phrase`, `jewish_gematria`, etc.
- Uses `upsert` to avoid duplicates (on conflict with `phrase`)

## Error Handling

### Storage Failures
1. **Critical Error**: If storage fails completely, operation fails
2. **Partial Failure**: If some items fail, operation continues but logs warning
3. **Retry Logic**: Individual inserts retry if batch insert fails

### Logging
- All storage operations are logged
- Critical failures are logged as ERROR
- Partial failures are logged as WARNING
- Success is logged as INFO

## Testing

### Validation Tests
- Test that scraped data is stored
- Test that storage failures cause operation failure
- Test that partial failures are logged
- Test that duplicate data is handled correctly

## Future Enhancements

1. **Automatic Retry**: Add automatic retry for failed storage operations
2. **Queue System**: Use queue for async storage to prevent blocking
3. **Backup Storage**: Store data in multiple locations for redundancy
4. **Monitoring**: Add monitoring to track storage success rates

## Compliance

All agents must comply with these rules. Any agent that collects data must:
1. Have a storage method
2. Validate storage success
3. Fail operation if storage fails
4. Log all storage operations

**This is a system-level requirement and cannot be bypassed.**

