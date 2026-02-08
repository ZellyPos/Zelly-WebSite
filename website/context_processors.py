from .models import WebsiteSetting

def website_settings(request):
    settings_dict = {}
    for setting in WebsiteSetting.objects.all():
        settings_dict[setting.key] = setting.value
    return {'site_settings': settings_dict}
