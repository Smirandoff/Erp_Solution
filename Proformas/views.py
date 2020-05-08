from django.shortcuts import render
from .models import Commande,Commande_Designation,Modalite,Facture
from django.shortcuts import redirect
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views.generic import View
from django.http import JsonResponse
from Client_Section.models import Client_Data
import datetime
import threading
from .forms import Commande_Form,Commande_D_Form,Modalite_Form,validat,Commande_Form2,Facture_Form
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.forms import modelformset_factory,formset_factory
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
import weasyprint
from django.template.loader import render_to_string
from weasyprint import HTML

from django.utils.html import strip_tags
# Create your views here.

def save_facture_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        print(request.method=='POST')
        if form.is_valid():

            form.save()

            data['form_is_valid'] = True
            f = Facture.objects.all()
            data['html_book_list'] = render_to_string('Proformas/facture/partial/partial_facture.html', {
                'facture': f
            })
        else:
            print(form.errors)

            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def facture_update(request,pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = Facture_Form(request.POST, instance=facture)

    else:
        form = Facture_Form(instance=facture)


    return save_facture_form(request, form,'Proformas/facture/partial/partial_update.html')



def facture_delete(request,pk):
    facture = get_object_or_404(Facture, pk=pk)
    print(facture)
    data = dict()
    if request.method == 'POST':
        facture.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        f = Facture.objects.all()
        data['html_book_list'] = render_to_string('Proformas/facture/partial/partial_facture.html', {
            'facture': f
        })
    else:
        context = {'facture': facture,'id':pk}
        data['html_form'] = render_to_string('Proformas/facture/partial/partial_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def facture_view(request):
    factur = Facture.objects.all()
    return render(request,'Proformas/facture/partial_view.html',{'facture':factur})

def Facture_create(request,pk):
    command = get_object_or_404(Commande,pk=pk)
    # payemnt = Payements.objects.all().values_list('files_id', flat=True)

    if request.method == 'POST':
        form = Facture_Form(request.POST or None)

        ttc = command.Montant_TTC

        if float(form.data['Montant_TTC']) > float(ttc):
            error =  "le montant_ttc est superieur que le montant HT de la commande "
            return render(request, 'Proformas/facture/facture_form.html', {'form': form,'errors':error})


        if form.is_valid():
            form.save()
            return redirect('commande')
        print(form.errors)
    else:

        form = Facture_Form()
    return render(request, 'Proformas/facture/facture_form.html',{'form':form})




def commande_deletee(request,pk):
        commande = get_object_or_404(Commande, pk=pk)
        data = dict()
        if request.method == 'POST':
            commande.delete()
            data['form_is_valid'] = True  # This is just to play along with the existing code
            com = Commande.objects.all()
            data['html_book_list'] = render_to_string('Proformas/partial/partial_proformas.html', {
                'c': com
            })
        else:
            context = {'obj': commande}
            data['html_form'] = render_to_string('Proformas/partial/parital_delete.html',
                                                 context,
                                                 request=request,
                                                 )
        return JsonResponse(data)


def dat_val(request,pk):
    commande = get_object_or_404(Commande,pk=pk)
    if request.method == 'POST':
      form = Commande_Form2(request.POST, instance=commande)
    else:
        form = Commande_Form2(instance=commande)

    return valid_save(request, form, pk, 'Proformas/partial/partial_valid.html')

def valid_save(request, form,pk, template_name):
        commande = Commande.objects.filter(id=pk)
        data = dict()
        if request.method == 'POST':
            if form.is_valid():
                dat = form.data['Date_validation']
                achh = Commande.objects.filter(id=pk).update(Date_validation=dat, validation=True)
                data['form_is_valid'] = True
                command = Commande.objects.all()
                data['html_book_list'] = render_to_string('Proformas/partial/partial_proformas.html', {
                'c': command
            })
            else:
                print(form.errors)
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string('Proformas/partial/partial_valid.html',context,
                                             request=request,
                                             )
        return JsonResponse(data)


# def dat_val(request,pk):
#     # commande = Commande.objects.filter(id=pk)
#     if request.method == 'POST':
#         form = validat(request.POST)
#         if form.is_valid():
#             dat = form.data['Validate_date']
#             achh = Commande.objects.filter(id=pk).update(Date_validation=dat,validation=True)
#             return redirect('commande')
#
#     else:
#         form = validat()
#     return render(request,'Proformas/valid.html',{'form':form})
#


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.attach_file('/tmp/Facture.pdf')
        msg.content_subtype = "html"  # Main content is now text/html
        msg.encoding = 'utf-8'
        msg.send()


def nadjib(subject, html_content, recipient_list, sender):
        EmailThread(subject, html_content, recipient_list, sender).start()



def send_mail(request):
    html_nadjib = render_to_string('Proformas/msg.html')
    to_emails = ['attignadjib@outlook.com']
    subject = "SH INFOR FACTURE"
    nadjib(subject, html_nadjib, to_emails, 'attignadjib@gmail.com')
    # email = EmailMessage(subject, html_nadjib, from_email='attignadjib@gmail.com', to=to_emails)
    # email.attach_file('/tmp/Facture.pdf')
    # email.content_subtype = "html"  # Main content is now text/html
    # email.encoding = 'utf-8'
    # email.send()

    return HttpResponse('SENT')



def html_to_pdf_view(request,pk):
        com = get_object_or_404(Commande,pk=pk)
        if Commande_Designation.objects.filter(Command=pk):
            design = Commande_Designation.objects.filter(Command=com).values_list('Designation', flat=True)
            prix = Commande_Designation.objects.filter(Command=com).values_list('Prix_Unitaire', flat=True)
            qua = Commande_Designation.objects.filter(Command=com).values_list('Quantite', flat=True)
            ht = Commande_Designation.objects.filter(Command=com).values_list('Montant_HT', flat=True)
            tva = Commande_Designation.objects.filter(Command=com).values_list('Montant_TVA', flat=True)
            ttc = Commande_Designation.objects.filter(Command=com).values_list('Montant_TTC', flat=True)
        else :
           design = ""
           prix = ""
           qua = ""
           ht = ""
           tva = ""
           ttc = ""

        Designation = ''
        for x in design:

            print(x)
            Designation = Designation + " " +  x

        Prix_Uni = 0
        for x in prix:
            Prix_Uni = Prix_Uni + x

        Quantite = 0
        for x in qua:
            Quantite = Quantite + x

        Montant_HT= 0
        for x in ht:
            Montant_HT =Montant_HT +x

        Montant_TVA = 0
        for x in tva:
            Montant_TVA = Montant_TVA +x

        Montant_TTC = 0
        for x in ttc:
                Montant_TTC = Montant_TTC +x




        if Modalite.objects.filter(Command=com.id).exists():
            mod = Modalite.objects.get(Command=com.id)
            modalite_payement = mod.modalite_payement
            print(modalite_payement)
            Arret_Facture = mod.Arret_Facture
            Formation = mod.Formation
            Period_Réalisation = mod.Period_Réalisation
            Echéancier_payement = mod.Echéancier_payement
            Debut_realsiation = mod.Debut_realsiation
            Garantie = mod.Garantie
        else:
            modalite_payement  = ''
            print(modalite_payement)
            Arret_Facture = ''
            Formation = ''
            Period_Réalisation = ''
            Echéancier_payement = ''
            Debut_realsiation = ''
            Garantie = ''

        Numero_com  = com.Numero_commande
        client = com.Client
        client_data = Client_Data.objects.get(id=client.id)
        adresse = client_data.adresse
        NIF = client_data.NIF
        NIS = client_data.NIS
        raison_social = client_data.Raison_social


        context = {
        'Designation': Designation,
        'Prix_Uni': Prix_Uni,
        'Quantite': Quantite,
        'Montant_HT': Montant_HT,
        'Montant_TVA': Montant_TVA,
        'Montant_TTC': Montant_TTC,
        'Numero_com': Numero_com,
        'adresse': adresse,
        'NIF': NIF,
        'NIS': NIS,
        'raison_social': raison_social,
        'Date': datetime.date.today(),
        'modalite_payement':modalite_payement,
        'Arret_Facture':Arret_Facture,
        'Formation': Formation,
        'Echéancier_payement':Echéancier_payement,
        'Period_Réalisation':Period_Réalisation,
        'Debut_realsiation':Debut_realsiation,
        'Garantie':Garantie,

        }
        html_string = render_to_string('Proformas/command.html',context)

        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/Facture.pdf');
        html_nadjib = render_to_string('Proformas/msg.html', context)
        fs = FileSystemStorage('/tmp')
        with fs.open('Facture.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="Facture.pdf"'
            # to_emails = ['attignadjib@outlook.com']
            # subject = "SH INFOR FACTURE"
            # email = EmailMessage(subject, html_nadjib, from_email='attignadjib@gmail.com', to=to_emails)
            # email.attach_file('/tmp/Facture.pdf')
            # email.content_subtype = "html"  # Main content is now text/html
            # email.encoding = 'utf-8'
            # email.send()
        return response





def Commande_view(request):
    command = Commande.objects.all()
    return render(request, 'Proformas/command_view.html', {'c': command})


def step3(request):
    if request.method == 'POST':
        form = Modalite_Form(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('commande')
        print(form.errors)
    else:

        form = Modalite_Form()
    return render(request, 'Proformas/steps/step3.html', {'form': form})


def step1(request):
    if request.method == 'POST':
        form = Commande_Form(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('step2')
        print(form.errors)
    else:

        form = Commande_Form()
    return render(request, 'Proformas/steps/step1.html', {'form': form})


def step2(request):
    if request.method == 'POST':
        nadjib = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5, can_delete=True)
        form = nadjib(request.POST)

        if form.is_valid():
            form.save()

            return redirect('step3')
        else:
            print(form.errors)
            return render(request, 'Proformas/steps/step2.html', {'formset': form, 'error': form.errors})

    else:
      ss = modelformset_factory(Commande_Designation, form=Commande_D_Form, extra=5)
      formset = ss(queryset=Commande.objects.none())
    return render(request, 'Proformas/steps/step2.html', {'formset': formset})

