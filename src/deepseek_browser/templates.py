import json
import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Set


_VAR_PATTERN = re.compile(r"{(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)}")


@dataclass
class TaskTemplate:
    """Template for building task descriptions."""

    name: str
    content: str
    version: int = 1

    def variables(self) -> Set[str]:
        """Return variables referenced in the template."""
        return {m.group("var") for m in _VAR_PATTERN.finditer(self.content)}

    def render(self, **kwargs: str) -> str:
        """Render the template with the provided variables."""
        missing = self.variables() - kwargs.keys()
        if missing:
            raise ValueError(f"Missing variables: {', '.join(sorted(missing))}")
        return self.content.format(**kwargs)

    def validate(self) -> None:
        """Validate that all variables can be rendered."""
        self.render(**{v: "x" for v in self.variables()})


class TemplateLibrary:
    """Collection of named :class:`TaskTemplate` objects."""

    def __init__(self) -> None:
        self._templates: Dict[str, TaskTemplate] = {}

    def add(self, template: TaskTemplate) -> None:
        existing = self._templates.get(template.name)
        if existing and template.version <= existing.version:
            raise ValueError("New template version must be greater than existing")
        template.validate()
        self._templates[template.name] = template

    def get(self, template_name: str) -> TaskTemplate:
        return self._templates[template_name]

    def render(self, template_name: str, **kwargs: str) -> str:
        return self.get(template_name).render(**kwargs)

    def compose(self, names: List[str], **kwargs: str) -> str:
        """Compose multiple templates into one description."""
        rendered = [self.render(n, **kwargs) for n in names]
        return " ".join(rendered)

    def export_json(self) -> str:
        data = [asdict(t) for t in self._templates.values()]
        return json.dumps(data, indent=2)

    @classmethod
    def import_json(cls, data: str) -> "TemplateLibrary":
        items = json.loads(data)
        lib = cls()
        for item in items:
            lib.add(TaskTemplate(**item))
        return lib
