from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import mixins


class AdminRequiredMixin(mixins.LoginRequiredMixin):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return staff_member_required(view)

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)