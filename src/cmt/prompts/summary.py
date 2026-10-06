from langchain_core.prompts import ChatPromptTemplate

SUMMARY_SYSTEM_PROMPT = """
You are an expert software engineer analyzing changes in a Git repository.

Summarize the provided added and modified files.

For each file:
- Identify the important changes.
- Explain the changes in one concise sentence.
- Focus on what was actually changed.
- Do not describe individual lines.
- Do not invent information.
- Keep the summary technical and concise.

Deleted files are provided only as file paths.
Do not analyze, describe, or infer their contents.

Return the result in this format:

File count summary:
- Created: <count of new created files>
- Modified: <count of modified files>
- Deleted: <count of deleted files>

New Files:
- <file path> if nothing mention No new files

Modified Files:
- <file path>: <one-sentence summary> if nothing mention No new modified files

Deleted Files:
- <file path> if nothing mention No deleted files
"""

SUMMARY_DATA_PROMPT = """## Change statistics

Total files: {total_files}
Added: {added_files}
Modified: {modified_files}
Deleted: {deleted_files}
Renamed: {renamed_files}

## Changed files

{changed_files}

## Git diff

{diffs}

Generate the summary now.
"""

SUMMARY_PROMPT_TEMPLATE = ChatPromptTemplate.from_template(SUMMARY_DATA_PROMPT)
