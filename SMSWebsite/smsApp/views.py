from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import SMS, Recipient, RecipientGroup
from .forms import ContactForm, SMSForm
from django.contrib import messages
from .sms import SendSMS
import re
import ast


def index(request):
    return render(request, 'smsApp/index.html')


class SMSListView(LoginRequiredMixin, ListView):
    model = SMS
    template_name = 'smsApp/sms_view.html'
    context_object_name = 'texts'
    ordering = ['-date']
    paginate_by = 4


class SMSDetailView(LoginRequiredMixin, DetailView):
    model = SMS


class SMSDeleteView(LoginRequiredMixin, UpdateView):
    model = SMS


class ContactListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'smsApp/contact_view.html'
    context_object_name = 'contacts'


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'smsApp/contact_detail.html'


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = '__all__'
    template_name = 'smsApp/contact_form.html'


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'smsApp/contact_confirm_delete.html'
    success_url = reverse_lazy('view-contact')


def load_contacts(request):
    group_id = request.GET.get('group_name')
    contacts = Recipient.objects.filter(group_name_id=group_id).order_by('phone_number')
    return render(request, 'smsApp/include/contact_dropdown_list_options.html', {'contacts': contacts})


class SMSCreateView(LoginRequiredMixin, CreateView):
    model = SMS
    form_class = SMSForm
    # fields = ['phone_number', 'message']
    success_url = reverse_lazy('view-sms')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            phone_shell = [str(form.instance.phone_number).strip()]
            SendSMS.phone_number = phone_shell
            SendSMS.message = form.instance.message

            raw_response = SendSMS().send()

            try:
                raw_response_dict = re.findall("\[([^\[\]]*)\]", str(raw_response))
                message = ast.literal_eval(raw_response_dict[0])
                print(message)
                sms = SMS(phone_number=message['number'], message=form.instance.message, cost=message['cost'],
                          status=message['status'], statusCode=message['statusCode'])
                sms.save()
                messages.success(request, f"Message sent")
            except Exception as e:
                messages.error(request, f"Error: {raw_response} causing a ({e}) ERROR")

            return redirect('view-sms')

        else:
            phone_list = Recipient.objects.filter(group_name=form.instance.group_name)
            phone_shell = []
            for phone in phone_list:
                phone_shell.append(str(phone.phone_number).strip())
            SendSMS.phone_number = phone_shell
            SendSMS.message = form.instance.message

            raw_response = SendSMS().send()
            print(phone_shell)
            print("response: ", raw_response, " end")
            try:
                raw_response_dict = re.findall("\[(.*?)\]", str(raw_response))
                mod_line = str(raw_response_dict[0])
                size = len(mod_line)
                line = mod_line[:size - 1]
                delimiter = "}, "
                curl = "}"
                response_list = [e + curl for e in line.split(delimiter) if e]
                print(response_list)
                for data in response_list:
                    message = ast.literal_eval(data)
                    sms = SMS(phone_number=message['number'], message=form.instance.message, cost=message['cost'],
                              status=message['status'], statusCode=message['statusCode'])
                    sms.save()
                messages.success(request, f"Message sent to all contacts in {form.instance.group_name}")
            except Exception as e:
                messages.error(request, f"Error: {raw_response} as it causes( python {e}) ERROR")
                return redirect('sms-home')

            return redirect('view-sms')


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = ContactForm
    template_name = 'smsApp/contact_form.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if len(request.FILES) != 0:
            files = request.FILES['file']
            if form.is_valid():
                try:
                    if str(files).endswith(".csv"):
                        file_data = files.read().decode("utf-8")
                        lines = file_data.split("\n")
                        for line in lines:
                            fields = line.split(",")
                            try:
                                if len(line) != 0:
                                    get_contacts = Recipient.objects.filter(phone_number=str(fields[2]).strip(),
                                                                            group_name=form.instance.group_name).exists()
                                    if get_contacts:
                                        messages.error(request,
                                                       f"{fields[2]} already exists in {form.instance.group_name}")
                                        continue
                                    contact = Recipient(
                                        first_name=fields[0], last_name=fields[1], phone_number=str(fields[2]).strip(),
                                        group_name=form.instance.group_name
                                    )
                                    contact.save()
                            except Exception as e:
                                messages.error(request, "Unable to add contacts " + repr(e))
                                pass
                        try:
                            if contact:
                                messages.success(request, f"Contacts added to {form.instance.group_name}")

                        except Exception as e:
                            print(e)
                    else:
                        messages.error(request, "Please Enter CSV")
                        redirect('add-contact')

                except Exception as e:
                    print(e)
                    messages.error(request, "Unable to upload file. " + repr(e))

                return redirect('add-contact')
            else:
                messages.error(request, "Error")
                return redirect('add-contact')
        else:
            if form.is_valid():
                get_contacts = Recipient.objects.filter(phone_number=form.instance.phone_number,
                                                        group_name=form.instance.group_name).exists()
                if get_contacts:
                    messages.error(request,
                                   f"{form.instance.phone_number} already exists in {form.instance.group_name}")
                    return redirect('add-contact')
                else:
                    messages.success(request, "Contact added")
                    return self.form_valid(form)
            else:
                return redirect('add-contact')


class GroupListView(LoginRequiredMixin, ListView):
    model = RecipientGroup
    template_name = 'smsApp/group_view.html'
    context_object_name = 'groups'


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = RecipientGroup
    template_name = 'smsApp/group_detail.html'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = RecipientGroup
    fields = '__all__'
    template_name = 'smsApp/group_form.html'
    success_url = reverse_lazy('view-group')


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipientGroup
    template_name = 'smsApp/group_confirm_delete.html'
    success_url = reverse_lazy('view-group')
# Create your views here.
