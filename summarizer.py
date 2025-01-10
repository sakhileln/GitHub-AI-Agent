from langchain_core.tools import tool


@tool
def note_tool(note):
    """
    Save a note to a local file

    Args:
        note: the text note to save
    """
    with open("summary.txt", "a") as f:
        f.write(note + "\n")
