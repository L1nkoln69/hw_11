from .forms import AuthorForm
from .models import Author


class AllFormObjects:
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SeeObjects:
    paginate_by = 70
    model = None
    template_name = None
