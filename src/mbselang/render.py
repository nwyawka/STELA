from __future__ import annotations

from .model import Model


def render_mermaid(model: Model) -> str:
    lines = ["flowchart LR"]
    root = model.components.get(model.name)
    if root is None:
        for component in model.components.values():
            lines.append(f'    {component.name}["{component.name}"]')
        return "\n".join(lines) + "\n"
    for part in root.parts.values():
        lines.append(f'    {part.name}["{part.name}: {part.component_type}"]')
    for connection in root.connections:
        source_part, source_port = connection.source.split(".", 1)
        target_part, target_port = connection.target.split(".", 1)
        lines.append(f"    {source_part} -- {source_port} to {target_port} --> {target_part}")
    return "\n".join(lines) + "\n"

