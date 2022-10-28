from coc_utilities import coc_api as ca

def handle_help() -> str:
    return """```The commands available with Royal Champion are listed below:    
  > !help - displays this help message
  > !war - lists the clan members that have opted into the war and their strikes
  > !strike [[give|take|reset] <member>|list]
\t> !strike give <member> - gives a strike to provided member
\t> !strike take <member> - takes a strike from provided member
\t> !strike reset <member> - resets member's strikes back to zero
\t> !strike list - lists all members with strikes and how many they have
```"""

def handle_war() -> str:
    war_party = ca.get_members_for_war()
    strikes = ca.get_strikes()
    msg = '```War Party:\n'
    for index, warrior in enumerate(war_party):
        strike_count = 0
        if warrior in strikes.keys():
            strike_count = strikes[warrior]['strikes']
        msg += f'  {index+1}. {warrior} -> strikes: {strike_count}\n'
    msg += '```'

    return msg

def handle_strike(tokens: list) -> str:
    strikes = {}

    if tokens[0].lower() == 'list':
        strikes = ca.get_strikes()
        member_count = 0
        msg = '```Strikes:\n'
        for member in strikes.keys():
            if strikes[member]['strikes'] != 0:
                msg += f"  > {member}: {strikes[member]['strikes']}\n"
                member_count += 1
        msg += '```'

        if member_count != 0:
            return msg
        else:
            return '`There are currently no members with strikes.`'

    member = ' '.join(tokens[1:])
    if tokens[0].lower() == 'give':
        strikes = ca.update_strikes(member, True)
        strike_count = strikes[member]['strikes']
        if strike_count < 3:
            return f"`{member} has {strike_count} {'strike' if strike_count == 1 else 'strikes'} now.`"
        else:
            return f"`{member} has 3 strikes, action may be needed to remove member from clan.`"
    elif tokens[0].lower() == 'take':
        strikes = ca.update_strikes(member, False)
        strike_count = strikes[member]['strikes']
        if strike_count > 0:
            return f"`{member} has {strike_count} {'strike' if strike_count == 1 else 'strikes'} now.`"
        else:
            return f"`{member} no longer has any strikes.`"
    elif tokens[0].lower() == 'reset':
        strikes = ca.update_strikes(member, False, reset=True)
        return f"`{member} no longer has any strikes.`"
    else:
        return '`!strike subcommand not recognized.`\n\n' + handle_help()

def handle_command(message: str) -> str:
    tokens = message.split()

    if tokens[0].lower() == '!help':
        return handle_help()
    elif tokens[0].lower() == '!war':
        return handle_war()
    elif tokens[0].lower() == '!strike':
        return handle_strike(tokens[1:])
    else:
        return '`Command not recognized.`\n\n' + handle_help()