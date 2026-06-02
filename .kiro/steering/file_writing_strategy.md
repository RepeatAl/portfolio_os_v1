# File Writing Strategy

## Rule

When creating new files with substantial content (>50 lines), always use chunked writing:

1. Use `fsWrite` to create the file with initial content
2. Use `fsAppend` to add remaining content in manageable chunks
3. Never attempt to write large files in a single `fsWrite` operation

## Rationale

Large single writes can fail due to tool limitations.
Chunked writing ensures reliable file creation.

## Implementation

**Step 1:** Create file with first section
**Step 2:** Append subsequent sections
**Step 3:** Verify file completeness

This approach maximizes success rate for large documentation files.
