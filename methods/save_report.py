
import json, logging, pathlib

def generate_markdown(json_file_path, output_md_path):

    current_dir = pathlib.Path(__file__).parent.resolve()
    root = current_dir.parent
    target_dir = root / "examples" / "jsons"
    file_path_in = target_dir / json_file_path

    try:
        with open(file_path_in, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.info(f"Error: File {json_file_path} not found.")
        return

    try:

        md_lines = []

        md_lines.append(f"# {output_md_path[:-3].replace("_", " ")}")
        md_lines.append(f"**Generated at:** {data.get('generated_at', 'N/A')}\n")

        quality = data.get('quality', {})
        consistent = data.get('consistent', {})
        md_lines.append(f"## Quality Score: {quality.get('quality_score', 'N/A')}/100     Consistent Score: {consistent}")
        md_lines.append(f"{quality.get('short_explaination_of_quality', '')}\n")

        md_lines.append(f"## Market Trend: {data.get('market_trend', '').capitalize()}")
        md_lines.append(f"{data.get('short_explaination_of_market_trend', '')}\n")

        companies = ", ".join(data.get("top_companies_for_these_skills", []))
        md_lines.append(f"**Top Companies hiring for these skills:** {companies}\n")

        md_lines.append("## Soft Skills")
        md_lines.append("| Skill | Demand | Trend |")
        md_lines.append("|---|---|---|")
        for skill in data.get("soft_skills", []):
            md_lines.append(f"| {skill.get('soft_skill')} | {skill.get('demand')} | {skill.get('trend')} |")
        md_lines.append("\n")

        md_lines.append("## Hard Skills")

        if data.get("hard_skills"):
            hard_skills = data["hard_skills"][0]
            
            md_lines.append("### Languages")
            for lang in hard_skills.get("languages", []):
                md_lines.append(f"* **{lang.get('programming_language')}** (Demand: {lang.get('demand')}, Trend: {lang.get('trend')})")

            md_lines.append("\n### Frameworks")
            for fw in hard_skills.get("frameworks", []):
                md_lines.append(f"* **{fw.get('framework_for_programming_language')}** (Demand: {fw.get('demand')}, Trend: {fw.get('trend')})")

            md_lines.append("\n### Infrastructure")
            for inf in hard_skills.get("infrastructures", []):
                md_lines.append(f"* **{inf.get('infrastructure')}** (Demand: {inf.get('demand')}, Trend: {inf.get('trend')})")
        md_lines.append("\n")

        md_lines.append("## Salary Insights")
        md_lines.append("| Level | Location | Min | Avg | Max |")
        md_lines.append("|---|---|---|---|---|")
        grades = data.get("grades", {})
        for level, locations in grades.items():
            lvl_name = level.replace('_salaries', '').capitalize()
            for loc, salaries in locations.items():
                loc_name = loc.replace('_salaries', '').replace('_', ' ').capitalize()
                min_s = salaries.get('minimum_salary')
                avg_s = salaries.get('average_salary')
                max_s = salaries.get('maximum_salary')
                md_lines.append(f"| **{lvl_name}** | {loc_name} | {min_s} | {avg_s} | {max_s} |")
        md_lines.append("\n")

        md_lines.append("## Learning Path")
        learning = data.get("learning", {})
        for stage, content in learning.items():
            md_lines.append(f"### {stage.capitalize()}")
            md_lines.append("**Themes:**")
            for theme in content.get("themes_list", []):
                md_lines.append(f"* {theme.get('theme')}")
            md_lines.append("\n**Resources:**")
            for res in content.get("information_resources", []):
                md_lines.append(f"* {res.get('resource')} *(Type: {res.get('resource_type')})*")
            md_lines.append("\n")

        md_lines.append("## Gap Analysis")
        gaps = data.get("gap_analysis", {})
        md_lines.append("### Quick Wins")
        for qw in gaps.get("quick_wins", []):
            md_lines.append(f"* {qw.get('hard_skill')}")
        md_lines.append("\n### Long Term")
        for lt in gaps.get("long_term", []):
            md_lines.append(f"* {lt.get('hard_skill')}")
        md_lines.append("\n")

        project = data.get("portfolio_project", {})
        md_lines.append("## Recommended Portfolio Project")
        md_lines.append(f"### {project.get('project_name')}\n")
        md_lines.append(f"{project.get('project_description')}\n")
        
        tech_list = [t.get("hard_skill_name") for t in project.get("list_of_technologies", [])]
        md_lines.append(f"**Technologies to use:** {', '.join(tech_list)}\n")

        current_dir = pathlib.Path(__file__).parent.resolve()
        root = current_dir.parent
        target_dir = root / "examples" / "reports"
        file_path_out = target_dir / output_md_path

        with open(file_path_out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))

        logging.info(f"File {output_md_path} was currently created")

    except Exception as e:
        logging.error(f"some went wrong when {output_md_path} was creating")
