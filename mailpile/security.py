"""
Global Mailpile crypto/privacy/security policy

This module attempts to collect in one place all of the different
security related decisions made by the app, in order to facilitate
review and testing.

"""
from mailpile.i18n import gettext as _
from mailpile.i18n import ngettext as _n


##[ These are the sys.lockdown restrictions ]#################################

def _lockdown_basic(command_obj):
    if command_obj.session.config.sys.lockdown:
        return _('In lockdown, doing nothing.')
    return False


def _lockdown_strict(command_obj):
    if (command_obj.session.config.sys.lockdown or 0) > 1:
        return _('In lockdown, doing nothing.')
    return False


CC_ACCESS_FILESYSTEM  = [_lockdown_basic]
CC_CHANGE_CONFIG      = [_lockdown_basic]
CC_CHANGE_CONTACTS    = [_lockdown_basic]
CC_CHANGE_GNUPG       = [_lockdown_basic]
CC_CHANGE_FILTERS     = [_lockdown_strict]
CC_CHANGE_TAGS        = [_lockdown_strict]
CC_COMPOSE_EMAIL      = [_lockdown_strict]
CC_CPU_INTENSIVE      = [_lockdown_basic]
CC_LIST_PRIVATE_DATA  = [_lockdown_basic]
CC_TAG_EMAIL          = [_lockdown_strict]
CC_QUIT               = [_lockdown_basic]


def forbid_command(command_obj, cc_list=None):
    """
    Determine whether to block a command or not.
    """
    if cc_list is None:
        cc_list = command_obj.COMMAND_SECURITY
    if cc_list:
        for cc in cc_list:
            forbid = cc(command_obj)
            if forbid:
                return forbid
    return False


##[ Common web-server security code ]#################################

def http_content_security_policy(http_server):
    """
    Calculate the default Content Security Policy string.

    This provides an important line of defense against malicious
    Javascript being injected into our web user-interface.
    """
    # FIXME: Allow deviations in config, for integration purposes
    # FIXME: Clean up Javascript and then make this more strict
    return ("default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "img-src 'self' data://*")
