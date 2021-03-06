from django.forms import ModelChoiceField
from django.utils.encoding import force_text

from linkit.types.contracts import TypeForm, LinkType


class ModelTypeForm(TypeForm):
    def __init__(self, *args, **kwargs):
        """ Set the queryset and label dynamically based on the properties defined on the link type. """
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = self.link_type.queryset()
        self.fields['model'].label = force_text(self.link_type.model._meta.verbose_name)

    model = ModelChoiceField(queryset=None)


class ModelLinkType(LinkType):
    model = None
    form_class = ModelTypeForm

    def real_value(self):
        if isinstance(self.link.data('value').get('model'), int):
            return self.model.objects.filter(pk=self.link.data('value').get('model')).first()
        else:
            return self.model.objects.filter(pk=self.link.data('value').get('model').pk).first()

    @property
    def href(self):
        real_value = self.real_value()
        if real_value:
            return real_value.get_absolute_url()

        return False

    @property
    def label(self):
        real_value = self.real_value()
        if real_value:
            return str(real_value)

        return False

    def queryset(self):
        return self.model.objects.all()
