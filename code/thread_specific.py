import re

from thread_category_patterns import THREAD_CATEGORY_PATTERNS, SUBCATEGORIES




CUSTOM_CALL_PREFIXES = (
    "com.crossjoin",
    "pt.crossjoin",
    "com.company",
     "com.crossjointest."
)

def get_thread_subcategory_from_name(
    thread_name: str,
    thread_category: str,
) -> str:
    """
    Returns the thread subcategory.

    If no subcategory matches, returns the category itself.
    """

    if thread_name is None or thread_category is None:
        return None

    patterns = SUBCATEGORIES.get(thread_category)

    if patterns is None:
        return thread_category

    for pattern, subcategory in patterns:
        if re.match(pattern, thread_name):
            return subcategory

    return thread_category


def interpret_single_thread_info(current_csv, current_info, thread_dump_specific_text : str) -> dict:
    '''
    Returns a row for the thread text received
    '''

    info = current_info

    match = re.search(r'^"([^"]+)"', thread_dump_specific_text)

    match = re.search(
        r'^"([^"]+)"\s+#(\d+)',
        thread_dump_specific_text
    )
    
    if match:
        info["thread_name"] = match.group(1)
        info["thread_id"] = int(match.group(2))
    else:
        info["thread_name"] = None
        info["thread_id"] = None
    
    info["thread_category"] = get_thread_category_from_name(
        info["thread_name"]
    )

    info["thread_subcategory"] = get_thread_subcategory_from_name(
        info["thread_name"],
        info["thread_category"],
    )

    match = re.search(
        r"java\.lang\.Thread\.State:\s+([A-Z_]+)",
        thread_dump_specific_text
    )

    info["status"] = (
        match.group(1)
        if match
        else "NON_COMPUTABLE"
    )

    match = re.search(
        r"\bcpu=(\d+(?:\.\d+)?)ms",
        thread_dump_specific_text
    )

    info["cpu_ms"] = (
        float(match.group(1))
        if match
        else None
    )

    match = re.search(
        r"\belapsed=(\d+(?:\.\d+)?)s",
        thread_dump_specific_text
    )

    if match:
        info["time_elapsed_s"] = int(
            float(match.group(1)) * 1000
        )
    else:
        info["time_elapsed_s"] = None

    # Stack trace
    stack = re.findall( # this matches every line with at ...
        r'^\s+at\s+([^\s(]+)',
        thread_dump_specific_text,
        re.MULTILINE
    )

    # Last call
    info["last_call"] = (
        stack[0]
        if stack
        else None
    )

    # Last custom call
    info["last_custom_call"] = None

    for call in stack:

        if is_custom_call(call):
            info["last_custom_call"] = call
            break

    return info

def is_custom_call(function_name: str) -> bool:
    """
    Returns True if any package, class or method component
    contains the word 'tuxedo' (case-insensitive).
    """

    return function_name.startswith(CUSTOM_CALL_PREFIXES) or any(
        "tuxedo" in part.lower()
        for part in function_name.split(".")
    )


def get_thread_category_from_name(thread_name: str) -> str:
    if thread_name is None:
        return None

    for pattern, category in THREAD_CATEGORY_PATTERNS:
        if re.match(pattern, thread_name):
            return category

    return thread_name