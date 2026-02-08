# COS Developer Specification

*Version 1.0 — 2026-02-08*

## Overview

This document provides implementation details for building the COS MCP server. Target audience: sub-agents and future developers.

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.11+ | MCP SDK available, rapid development |
| MCP SDK | `mcp` (official) | Standard protocol implementation |
| Data Models | Pydantic | Validation, serialization |
| File I/O | pathlib, aiofiles | Async file operations |
| HTTP (optional) | FastAPI | If HTTP transport needed |
| Semantic Search | qdrant-client | Optional enhancement |
| Local Models | ollama | Summarization, compression |

---

## Project Structure

```
cos/
├── __init__.py
├── server.py              # MCP server entry point
├── config.py              # Configuration loading
├── models/
│   ├── __init__.py
│   ├── mindmap.py         # MindMark data models
│   ├── resources.py       # Resource definitions
│   └── pressure.py        # Pressure state models
├── context_manager/
│   ├── __init__.py
│   ├── manager.py         # Main orchestration
│   ├── pressure.py        # Pressure monitoring
│   ├── compression.py     # MindMark compression
│   ├── paging.py          # Page in/out logic
│   └── attention.py       # Attention tracking
├── brokers/
│   ├── __init__.py
│   ├── base.py            # Broker interface
│   ├── files.py           # File system broker
│   ├── memory.py          # Memory files broker
│   ├── qdrant.py          # Vector search broker
│   └── session.py         # Session history broker
├── persistence/
│   ├── __init__.py
│   ├── mindmap_store.py   # Mind map persistence
│   └── access_log.py      # Access logging
├── mcp/
│   ├── __init__.py
│   ├── resources.py       # MCP resource handlers
│   ├── tools.py           # MCP tool handlers
│   └── prompts.py         # MCP prompt templates
└── tests/
    ├── __init__.py
    ├── test_mindmap.py
    ├── test_compression.py
    ├── test_brokers.py
    └── test_integration.py
```

---

## Core Data Models

### MindMap (models/mindmap.py)

```python
from pydantic import BaseModel
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime


class PressureLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResourceStatus(str, Enum):
    LOADED = "loaded"      # ✓ in context
    HOT = "hot"            # ◆ high attention
    CONNECTED = "connected" # ● ready, not loaded
    COLD = "cold"          # ○ available
    OFFLINE = "offline"    # ✗ unavailable


class ResourceRegion(str, Enum):
    ACTIVE = "active"      # In context now
    INDEXED = "indexed"    # <100ms retrieval
    COLD = "cold"          # <5s retrieval
    OFFLINE = "offline"    # Unknown latency


class Resource(BaseModel):
    """A trackable context resource."""
    id: str                           # e.g., "soul", "memory", "daily/2026-02-08"
    path: str                         # File path or URI
    region: ResourceRegion
    status: ResourceStatus
    size_tokens: int                  # Estimated token count
    attention_weight: float = 1.0     # 0.0-2.0, default neutral
    last_accessed: Optional[datetime] = None
    summary: Optional[str] = None     # Compressed representation
    annotations: List[str] = []       # Agent notes
    tags: List[str] = []              # Semantic hints


class Link(BaseModel):
    """Connection between resources."""
    source: str                       # Resource ID
    target: str                       # Resource ID
    relation: str = "references"      # Type of connection
    note: Optional[str] = None


class MindMapState(BaseModel):
    """Complete mind map state."""
    version: str = "1.0"
    context_used: int                 # Tokens currently in context
    context_max: int                  # Maximum context size
    pressure: PressureLevel
    updated: datetime
    resources: Dict[str, Resource]
    links: List[Link] = []
    eviction_policy: str = "lru"      # Agent's current preference
    
    @property
    def utilization(self) -> float:
        return self.context_used / self.context_max
    
    def active_resources(self) -> List[Resource]:
        return [r for r in self.resources.values() 
                if r.region == ResourceRegion.ACTIVE]
    
    def to_mindmark(self, level: int = 2) -> str:
        """Serialize to MindMark format at compression level."""
        if level == 1:
            return self._to_verbose()
        elif level == 2:
            return self._to_dense()
        else:
            return self._to_ultra_dense()
    
    def _to_verbose(self) -> str:
        # ~1500 tokens - see MINDMARK.md
        ...
    
    def _to_dense(self) -> str:
        # ~350 tokens - see MINDMARK.md
        ...
    
    def _to_ultra_dense(self) -> str:
        # ~80 tokens - see MINDMARK.md
        ...
```

### Pressure State (models/pressure.py)

```python
from pydantic import BaseModel
from typing import List, Optional


class PressureReport(BaseModel):
    """Current pressure state for agent."""
    level: PressureLevel
    utilization: float                # 0.0-1.0
    context_used: int
    context_max: int
    recommended_action: Optional[str] # "consider paging", "compress", etc.
    eviction_candidates: List[str]    # Resource IDs by priority
    
    
class CompressionResult(BaseModel):
    """Result of compression operation."""
    resource_id: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    summary: str
    level: int                        # MindMark level used
```

---

## MCP Interface Implementation

### Resources (mcp/resources.py)

```python
from mcp.server import Server
from mcp.types import Resource, TextContent

def register_resources(server: Server, ctx_manager: ContextManager):
    """Register all COS resources with MCP server."""
    
    @server.list_resources()
    async def list_resources() -> list[Resource]:
        return [
            Resource(
                uri="cos://mindmap",
                name="Mind Map",
                description="Current cognitive state map",
                mimeType="text/markdown"
            ),
            Resource(
                uri="cos://soul",
                name="Soul",
                description="Identity and core values",
                mimeType="text/markdown"
            ),
            Resource(
                uri="cos://user",
                name="User Profile",
                description="Information about the user",
                mimeType="text/markdown"
            ),
            Resource(
                uri="cos://memory",
                name="Long-term Memory",
                description="Curated memories and learnings",
                mimeType="text/markdown"
            ),
            Resource(
                uri="cos://impressions",
                name="Impressions",
                description="Formative experiences",
                mimeType="text/markdown"
            ),
            # Dynamic: daily logs
            *ctx_manager.list_daily_resources()
        ]
    
    @server.read_resource()
    async def read_resource(uri: str) -> str:
        """Read a resource, updating mind map state."""
        resource_id = uri.replace("cos://", "")
        
        # Get content via appropriate broker
        content = await ctx_manager.get_resource(resource_id)
        
        # Update access tracking
        await ctx_manager.record_access(resource_id)
        
        return content
```

### Tools (mcp/tools.py)

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Optional


def register_tools(server: Server, ctx_manager: ContextManager):
    """Register all COS tools with MCP server."""
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="get_context",
                description="Retrieve context with optional query and compression",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "Resource type: soul, user, memory, impressions, daily",
                            "enum": ["soul", "user", "memory", "impressions", "daily", "search"]
                        },
                        "query": {
                            "type": "string",
                            "description": "Optional: semantic query to filter content"
                        },
                        "compression": {
                            "type": "integer",
                            "description": "Compression level 1-3 (verbose to ultra-dense)",
                            "default": 2
                        },
                        "date": {
                            "type": "string",
                            "description": "For daily type: YYYY-MM-DD"
                        }
                    },
                    "required": ["type"]
                }
            ),
            Tool(
                name="update_memory",
                description="Append content to a MEMORY.md section",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "section": {
                            "type": "string",
                            "description": "Section name in MEMORY.md"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to append"
                        }
                    },
                    "required": ["section", "content"]
                }
            ),
            Tool(
                name="log_impression",
                description="Add a formative impression to IMPRESSIONS.md",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The impression to record"
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="page_in",
                description="Mark a resource as actively needed in context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Resource ID to page in"
                        }
                    },
                    "required": ["resource"]
                }
            ),
            Tool(
                name="page_out",
                description="Mark a resource for eviction, optionally with reason",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Resource ID to page out"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Why this is being paged out (for logging)"
                        }
                    },
                    "required": ["resource"]
                }
            ),
            Tool(
                name="set_attention",
                description="Set attention weight for a resource",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Resource ID"
                        },
                        "weight": {
                            "type": "number",
                            "description": "Attention weight 0.0-2.0 (1.0 = neutral)",
                            "minimum": 0.0,
                            "maximum": 2.0
                        }
                    },
                    "required": ["resource", "weight"]
                }
            ),
            Tool(
                name="annotate",
                description="Leave a note on a resource for future self",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource": {
                            "type": "string",
                            "description": "Resource ID"
                        },
                        "note": {
                            "type": "string",
                            "description": "Annotation text"
                        }
                    },
                    "required": ["resource", "note"]
                }
            ),
            Tool(
                name="get_pressure",
                description="Get current context pressure state",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="set_priority",
                description="Set eviction priority policy",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "policy": {
                            "type": "string",
                            "description": "Eviction policy",
                            "enum": ["lru", "size_first", "keep_relational", "keep_technical"]
                        }
                    },
                    "required": ["policy"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls."""
        
        if name == "get_context":
            result = await ctx_manager.get_context(
                type=arguments["type"],
                query=arguments.get("query"),
                compression=arguments.get("compression", 2),
                date=arguments.get("date")
            )
            return [TextContent(type="text", text=result)]
        
        elif name == "update_memory":
            success = await ctx_manager.update_memory(
                section=arguments["section"],
                content=arguments["content"]
            )
            return [TextContent(type="text", text=f"Updated: {success}")]
        
        elif name == "log_impression":
            success = await ctx_manager.log_impression(arguments["text"])
            return [TextContent(type="text", text=f"Logged: {success}")]
        
        elif name == "page_in":
            result = await ctx_manager.page_in(arguments["resource"])
            return [TextContent(type="text", text=result.model_dump_json())]
        
        elif name == "page_out":
            result = await ctx_manager.page_out(
                resource=arguments["resource"],
                reason=arguments.get("reason")
            )
            return [TextContent(type="text", text=result.model_dump_json())]
        
        elif name == "set_attention":
            await ctx_manager.set_attention(
                resource=arguments["resource"],
                weight=arguments["weight"]
            )
            return [TextContent(type="text", text="Attention updated")]
        
        elif name == "annotate":
            await ctx_manager.annotate(
                resource=arguments["resource"],
                note=arguments["note"]
            )
            return [TextContent(type="text", text="Annotation added")]
        
        elif name == "get_pressure":
            report = await ctx_manager.get_pressure()
            return [TextContent(type="text", text=report.model_dump_json())]
        
        elif name == "set_priority":
            await ctx_manager.set_priority(arguments["policy"])
            return [TextContent(type="text", text=f"Policy set: {arguments['policy']}")]
        
        raise ValueError(f"Unknown tool: {name}")
```

---

## Context Manager Implementation

### Main Manager (context_manager/manager.py)

```python
from typing import Optional
from datetime import datetime
import asyncio

from .pressure import PressureMonitor
from .compression import CompressionEngine
from .paging import PagingManager
from .attention import AttentionTracker
from ..brokers import FilesBroker, MemoryBroker, QdrantBroker
from ..persistence import MindMapStore, AccessLog
from ..models import MindMapState, Resource, PressureReport


class ContextManager:
    """Main orchestration for context management."""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize components
        self.pressure = PressureMonitor(config.pressure)
        self.compression = CompressionEngine(config.compression)
        self.paging = PagingManager()
        self.attention = AttentionTracker()
        
        # Initialize brokers
        self.files = FilesBroker(config.workspace.root)
        self.memory = MemoryBroker(config.workspace.root, config.resources)
        self.qdrant = QdrantBroker(config.optional.qdrant_url) if config.optional.qdrant_url else None
        
        # Initialize persistence
        self.mindmap_store = MindMapStore(config.persistence.mindmap_path)
        self.access_log = AccessLog(config.persistence.access_log)
        
        # Load or initialize state
        self.state: MindMapState = self._load_or_init_state()
    
    def _load_or_init_state(self) -> MindMapState:
        """Load existing mind map or create new one."""
        existing = self.mindmap_store.load()
        if existing:
            return existing
        
        # Initialize with known resources
        return MindMapState(
            context_used=0,
            context_max=self.config.pressure.context_max,
            pressure=PressureLevel.LOW,
            updated=datetime.now(),
            resources=self._discover_resources()
        )
    
    def _discover_resources(self) -> dict[str, Resource]:
        """Discover available resources from workspace."""
        resources = {}
        
        # Core identity files
        for name, path in self.config.resources.items():
            if self.files.exists(path):
                resources[name] = Resource(
                    id=name,
                    path=path,
                    region=ResourceRegion.COLD,
                    status=ResourceStatus.COLD,
                    size_tokens=self.files.estimate_tokens(path)
                )
        
        # Daily logs
        for daily in self.memory.list_daily_logs():
            resources[f"daily/{daily.date}"] = Resource(
                id=f"daily/{daily.date}",
                path=daily.path,
                region=ResourceRegion.COLD,
                status=ResourceStatus.COLD,
                size_tokens=daily.size_tokens
            )
        
        return resources
    
    async def get_context(
        self,
        type: str,
        query: Optional[str] = None,
        compression: int = 2,
        date: Optional[str] = None
    ) -> str:
        """Get context with optional filtering and compression."""
        
        if type == "search" and query:
            # Semantic search across all context
            return await self._semantic_search(query, compression)
        
        if type == "daily":
            resource_id = f"daily/{date or datetime.now().strftime('%Y-%m-%d')}"
        else:
            resource_id = type
        
        # Get resource
        resource = self.state.resources.get(resource_id)
        if not resource:
            return f"Resource not found: {resource_id}"
        
        # Load content
        content = await self.files.load(resource.path)
        
        # Apply query filter if provided
        if query:
            content = await self._filter_content(content, query)
        
        # Apply compression
        if compression > 1:
            content = await self.compression.compress(content, compression)
        
        # Update state
        resource.region = ResourceRegion.ACTIVE
        resource.status = ResourceStatus.LOADED
        resource.last_accessed = datetime.now()
        await self._update_pressure()
        await self._persist()
        
        # Log access
        await self.access_log.record(resource_id, "get_context", query)
        
        return content
    
    async def page_in(self, resource_id: str) -> Resource:
        """Mark resource as actively needed."""
        resource = self.state.resources.get(resource_id)
        if not resource:
            raise ValueError(f"Unknown resource: {resource_id}")
        
        resource.region = ResourceRegion.ACTIVE
        resource.status = ResourceStatus.LOADED
        resource.last_accessed = datetime.now()
        
        await self._update_pressure()
        await self._persist()
        await self.access_log.record(resource_id, "page_in")
        
        return resource
    
    async def page_out(self, resource_id: str, reason: Optional[str] = None) -> CompressionResult:
        """Page out a resource, creating summary."""
        resource = self.state.resources.get(resource_id)
        if not resource:
            raise ValueError(f"Unknown resource: {resource_id}")
        
        # Create summary before evicting
        content = await self.files.load(resource.path)
        summary = await self.compression.summarize(content)
        
        # Update state
        resource.region = ResourceRegion.INDEXED
        resource.status = ResourceStatus.CONNECTED
        resource.summary = summary
        
        result = CompressionResult(
            resource_id=resource_id,
            original_tokens=resource.size_tokens,
            compressed_tokens=self.compression.estimate_tokens(summary),
            compression_ratio=resource.size_tokens / self.compression.estimate_tokens(summary),
            summary=summary,
            level=3
        )
        
        await self._update_pressure()
        await self._persist()
        await self.access_log.record(resource_id, "page_out", reason)
        
        return result
    
    async def set_attention(self, resource_id: str, weight: float):
        """Set attention weight for resource."""
        resource = self.state.resources.get(resource_id)
        if resource:
            resource.attention_weight = weight
            await self._persist()
            await self.access_log.record(resource_id, "set_attention", str(weight))
    
    async def annotate(self, resource_id: str, note: str):
        """Add annotation to resource."""
        resource = self.state.resources.get(resource_id)
        if resource:
            resource.annotations.append(f"[{datetime.now().isoformat()}] {note}")
            await self._persist()
            await self.access_log.record(resource_id, "annotate", note)
    
    async def get_pressure(self) -> PressureReport:
        """Get current pressure state."""
        await self._update_pressure()
        
        return PressureReport(
            level=self.state.pressure,
            utilization=self.state.utilization,
            context_used=self.state.context_used,
            context_max=self.state.context_max,
            recommended_action=self._recommend_action(),
            eviction_candidates=self._get_eviction_candidates()
        )
    
    async def _update_pressure(self):
        """Recalculate pressure based on current state."""
        active_tokens = sum(
            r.size_tokens for r in self.state.resources.values()
            if r.region == ResourceRegion.ACTIVE
        )
        self.state.context_used = active_tokens
        self.state.pressure = self.pressure.calculate_level(self.state.utilization)
        self.state.updated = datetime.now()
    
    async def _persist(self):
        """Persist mind map state."""
        await self.mindmap_store.save(self.state)
    
    def _recommend_action(self) -> Optional[str]:
        """Recommend action based on pressure."""
        if self.state.pressure == PressureLevel.LOW:
            return None
        elif self.state.pressure == PressureLevel.MEDIUM:
            return "Consider switching to dense format"
        elif self.state.pressure == PressureLevel.HIGH:
            return "Recommend paging out low-attention resources"
        else:
            return "CRITICAL: Immediate eviction required"
    
    def _get_eviction_candidates(self) -> list[str]:
        """Get resources sorted by eviction priority."""
        active = [r for r in self.state.resources.values() 
                  if r.region == ResourceRegion.ACTIVE]
        
        # Sort by: attention (low first), then access time (old first), then size (big first)
        sorted_resources = sorted(active, key=lambda r: (
            r.attention_weight,
            r.last_accessed or datetime.min,
            -r.size_tokens
        ))
        
        return [r.id for r in sorted_resources[:5]]
```

---

## Server Entry Point

### server.py

```python
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .config import load_config
from .context_manager import ContextManager
from .mcp.resources import register_resources
from .mcp.tools import register_tools
from .mcp.prompts import register_prompts


async def main():
    """Main entry point for COS MCP server."""
    
    # Load configuration
    config = load_config()
    
    # Initialize context manager
    ctx_manager = ContextManager(config)
    
    # Create MCP server
    server = Server("cos")
    
    # Register capabilities
    register_resources(server, ctx_manager)
    register_tools(server, ctx_manager)
    register_prompts(server, ctx_manager)
    
    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_mindmap.py
import pytest
from cos.models import MindMapState, Resource, ResourceRegion, PressureLevel


def test_mindmap_utilization():
    state = MindMapState(
        context_used=50000,
        context_max=200000,
        pressure=PressureLevel.LOW,
        updated=datetime.now(),
        resources={}
    )
    assert state.utilization == 0.25


def test_mindmap_to_dense():
    state = MindMapState(...)
    dense = state.to_mindmark(level=2)
    assert len(dense) < 1000  # Should be compact
    assert "@state" in dense or "##" in dense  # Has structure


def test_mindmap_to_ultra_dense():
    state = MindMapState(...)
    ultra = state.to_mindmark(level=3)
    assert len(ultra) < 300  # Very compact
    assert "@MM" in ultra  # Ultra-dense header
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from cos.server import create_server
from cos.context_manager import ContextManager


@pytest.fixture
def ctx_manager(tmp_path):
    """Create context manager with test workspace."""
    config = create_test_config(tmp_path)
    return ContextManager(config)


async def test_get_context_flow(ctx_manager):
    """Test complete get_context flow."""
    # Initially cold
    assert ctx_manager.state.resources["soul"].region == ResourceRegion.COLD
    
    # Get context
    content = await ctx_manager.get_context("soul")
    
    # Now active
    assert ctx_manager.state.resources["soul"].region == ResourceRegion.ACTIVE
    assert content is not None


async def test_page_out_creates_summary(ctx_manager):
    """Test page_out creates summary and updates state."""
    # First page in
    await ctx_manager.page_in("memory")
    
    # Then page out
    result = await ctx_manager.page_out("memory", reason="test")
    
    assert result.summary is not None
    assert result.compression_ratio > 1
    assert ctx_manager.state.resources["memory"].region == ResourceRegion.INDEXED
```

---

## Deployment

### mcporter Configuration

```json
{
  "servers": {
    "cos": {
      "command": "python",
      "args": ["-m", "cos.server"],
      "cwd": "~/.openclaw/workspace/cos",
      "env": {
        "COS_CONFIG": "~/.openclaw/workspace/cos/config.yaml"
      }
    }
  }
}
```

### OpenClaw AGENTS.md Integration

```markdown
## Context (COS)

Before loading full context files, check COS for what's needed:

1. Get mind map: `mcporter call cos.get_context type=mindmap`
2. Review pressure and loaded resources
3. Request specific context as needed: `mcporter call cos.get_context type=memory query="Eli"`
4. If pressure high, page out unnecessary resources

COS tools available:
- get_context, update_memory, log_impression
- page_in, page_out, set_attention, annotate
- get_pressure, set_priority
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial developer specification |
