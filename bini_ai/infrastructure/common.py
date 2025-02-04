from bini_ai.infrastructure.colors import Colors


def format_friendly_message(output: str, model: str, version: str, tokens: callable) -> str:
    colors = Colors()
    message = output.split('Final result:')[0].strip()
    result = output.split('Final result:')[1].strip()

    # Apply color coding to the result
    if 'Failed' in result:
        result = f"{colors.RED}Result: {result}{colors.RESET}"
    else:
        result = f"{colors.GREEN}Result: {result}{colors.RESET}"

    # Create a formatted header and footer
    header_footer = f"{colors.CYAN}{'#' * 50}{colors.RESET}"

    # Combine everything into a final formatted message
    final = f"""
    {header_footer}
    {colors.CYAN}✔️ Bini AI Successfully Generated
    {colors.CYAN}✔️ Model: {model}
    {colors.CYAN}✔️ Version: {version}
    {colors.CYAN}✔️ Tokens: {tokens}
    {colors.CYAN}✔️ Output:\n
    {colors.YELLOW}{message}\n
    {result}
    {header_footer}
    """

    print(final)
    return final
