from pathlib import Path


def load_skill(skill_name: str) -> str:
        skill_file = Path(__file__).parent / "skills" / skill_name / "SKILL.md"

        if not skill_file.exists():
            raise FileNotFoundError(
                f"Skill '{skill_name}' not found: {skill_file}"
            )

        content = skill_file.read_text(encoding="utf-8")
        return f"""
===== Begin Skill: {skill_name} =====
{content}
===== End Skill: {skill_name} =====

"""
