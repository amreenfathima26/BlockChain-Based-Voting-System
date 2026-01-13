from .models import SiteConfiguration

def site_configuration(request):
    """
    Exposes the singleton SiteConfiguration object to all templates.
    Access it via {{ site_config.variable_name }}
    """
    return {'site_config': SiteConfiguration.get_solo()}
