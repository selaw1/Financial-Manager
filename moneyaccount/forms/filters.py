from django import forms


class TransactionFilterForm(forms.Form):

    filter = forms.CharField(max_length=15, required=False)
    search = forms.CharField(max_length=255, required=False)

    class Meta:
        fields = ("filter", "search")

    def clean(self):
        super().clean()

        choices = ["month", "week", 'today']
        initial_errors = self.errors.as_data()

        if "filter" not in initial_errors:
            filter = self.cleaned_data["filter"]
            if filter not in choices and filter:
                self.add_error("filter", "Invalid Choice")