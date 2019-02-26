from django.contrib.contenttypes.models import ContentType
from django.views.generic.detail import DetailView
from .models import NoteItem, Note
from django.shortcuts import redirect


class NoteViewMixin(DetailView):
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type_obj = ContentType.objects.get_for_model(self.model)
        context['notes'] = NoteItem.objects.select_related('note').filter(content_type=content_type_obj,
                                                                          object_id=self.get_object().id)
        return context

    def post(self, request, *args, **kwargs):
        note = Note(description=request.POST['description'])
        note.save()
        NoteItem(note=note, content_object=self.get_object()).save()
        return redirect('testing_app:' + self.model._meta.verbose_name, self.get_object().id)
