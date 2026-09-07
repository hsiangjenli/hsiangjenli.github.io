"""Load and validate resume data stored in the existing TOML schema."""

from dataclasses import dataclass
from pathlib import Path

import toml

from core.component import SkillTomlFile, TomlFile


@dataclass(frozen=True)
class ResumeData:
    """Validated data made available to resume templates."""

    education: list
    experience_groups: list
    skills: dict
    awards: list
    projects: list
    pull_requests: dict


def load_resume_data(config_dir: Path) -> ResumeData:
    """Load all resume TOML files while retaining their current schema."""
    experience_file = TomlFile.load(config_dir / "_experience.toml")
    pull_requests = toml.load(config_dir / "_open_source.toml")
    return ResumeData(
        education=TomlFile.load(config_dir / "_education.toml").entries,
        experience_groups=experience_file.grouped_entries,
        skills=SkillTomlFile.load(config_dir / "_skill.toml").entries,
        awards=TomlFile.load(config_dir / "_award.toml").entries,
        projects=TomlFile.load(config_dir / "_project.toml").entries,
        pull_requests=pull_requests,
    )
