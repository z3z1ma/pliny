"""Loom core — re-export facade.

All public symbols that command modules and ``validate.py`` import from
``loom.core`` are re-exported here from the three implementation modules
so that existing ``from ..core import ...`` lines continue to work
without change.
"""

from __future__ import annotations

# --- primitives ---
from .primitives import (  # noqa: F401
    CANONICAL_SUBTREES,
    SUPPORTING_SUBTREES,
    build_record_index,
    dump_frontmatter,
    extract_headings,
    find_workspace_root,
    flatten_link_values,
    issue,
    markdown_files,
    parse_frontmatter,
    parse_timestamp,
    read_record,
    relative_to_workspace,
    render_record,
    render_with_frontmatter,
    scan_records,
    slugify,
    utc_now,
)

# --- scope ---
from .scope import (  # noqa: F401
    WORKSPACE_SCOPE_ID,
    default_repository_scope,
    discover_repositories,
    merge_repository_scopes,
    normalize_repository_scope,
    repository_ids_by_path,
    repository_ids_for_scope,
    resolve_repository_for_path,
)

# --- records ---
from .records import (  # noqa: F401
    allocate_id,
    create_record,
    next_number,
    normalize_links,
    preferred_remote_url,
    repository_name_from_remote,
    repository_root_for_scope,
    resolve_record_path,
    set_sections,
    short_repository_slug,
    ticket_filename_prefix,
    write_record,
)
