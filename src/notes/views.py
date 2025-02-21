from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note, Tag
from .forms import NoteForm, TagForm
from django.db.models import Q

# 📌 Вивід усіх нотаток
class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        tag = self.request.GET.get("tag")  # Фільтр за тегом
        search_query = self.request.GET.get("q")  # Пошуковий запит

        queryset = Note.objects.all()  # Всі нотатки без обмежень

        if tag:
            queryset = queryset.filter(tags__name=tag)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["search_query"] = self.request.GET.get("q", "")  # Передача пошуку в шаблон
        return context

# 📌 Детальний перегляд нотатки
class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

# 📌 Додавання нової нотатки
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note-list')

# 📌 Оновлення нотатки
class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note-list')

# 📌 Видалення нотатки
class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note-list')

# 📌 Вивід усіх тегів
class TagListView(ListView):
    model = Tag
    template_name = 'notes/tag_list.html'
    context_object_name = 'tags'

# 📌 Додавання тегу
class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'notes/tag_form.html'
    success_url = reverse_lazy('notes:tag-list')

# 📌 Видалення тегу
class TagDeleteView(DeleteView):
    model = Tag
    template_name = "notes/tag_confirm_delete.html"
    success_url = reverse_lazy("notes:tag-list")