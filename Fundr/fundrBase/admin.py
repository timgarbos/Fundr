from django.contrib import admin
from Fundr.fundrBase.models import Project
from Fundr.fundrBase.models import ProjectAccess
from Fundr.fundrBase.models import Feature
from Fundr.fundrBase.models import FeatureStatusEntry
from Fundr.fundrBase.models import Donation

class ProjectAdmin(admin.ModelAdmin):
    pass
class ProjectAccessAdmin(admin.ModelAdmin):
    pass
class FeatureAdmin(admin.ModelAdmin):
    pass
class FeatureStatusEntryAdmin(admin.ModelAdmin):
    pass
class DonationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAccess, ProjectAccessAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeatureStatusEntry, FeatureStatusEntryAdmin)
admin.site.register(Donation, DonationAdmin)
