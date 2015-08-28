from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Blocks, Transactions, Inputs, Outputs
from .forms import SearchForm

def index(request):
	form = SearchForm(auto_id=False, initial={'refferer': 'block'})
	form.base_fields['search'].widget.attrs["placeholder"] = "Enter a block height or a block hash..."
	return render(request, 'spelunker/index.html', {'pageTitle': 'Peek Into The Blockchain',\
														'bigTitle': 'SPELUNKER',\
														'form': form,\
														'pageText' : 'Spelunker is spelunker is spelunker is spelunker is spelunker is spelunker is spelunker is spelunker is spelunker is spelunker...'})

def test(request):
	return render(request, 'spelunker/test.html')

def search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['refferer'] == 'transaction':
				return HttpResponseRedirect('/transaction'+ '/' + form.cleaned_data['search'])
			elif form.cleaned_data['refferer'] == 'input':
				return HttpResponseRedirect('/input'+ '/' + form.cleaned_data['search'])
			elif form.cleaned_data['refferer'] == 'output':
				return HttpResponseRedirect('/output'+ '/' + form.cleaned_data['search'])
			else:
				return HttpResponseRedirect('/block'+ '/' + form.cleaned_data['search'])
	return HttpResponseRedirect('/')

def block(request, blockHeigth):
	try:
		block = Blocks.objects.get(real_number = blockHeigth)
	except Blocks.DoesNotExist:
		raise Http404("Block does not exist")
	return render(request, 'spelunker/block.html', {'blocks': block})

def blockReview(request):
	form = SearchForm(auto_id=False, initial={'refferer': 'block'})
	form.base_fields['search'].widget.attrs["placeholder"] = "Enter a block height or a block hash..."
	return render(request, 'spelunker/overview.html', {'pageTitle': 'Block Overview',\
														'bigTitle': 'BLOCK',\
														'form': form,\
														'pageImage': 'spelunker/images/block.png',\
														'pageText' : 'Each block contains the data about bitcoin transactions. Altogether, these blocks form what is called the Blockchain.'})

def transactionHash(request, transactionHash):
	try:
		transaction = Transactions.objects.get(transaction_hash = transactionHash)
	except Transactions.DoesNotExist:
		raise Http404("Transaction does not exist")
	return render(request, 'spelunker/transaction.html', {'transaction': transaction})

def transactionId(request, transactionId):
	try:
		transaction = Transactions.objects.get(id = transactionId)
	except Transactions.DoesNotExist:
		raise Http404("Transaction does not exist")
	return render(request, 'spelunker/transaction.html', {'transaction': transaction})

def transactionReview(request):
	form = SearchForm(auto_id=False, initial={'refferer': 'transaction'})
	form.base_fields['search'].widget.attrs["placeholder"] = "Enter a transaction ID or a transaction hash..."
	return render(request, 'spelunker/overview.html', {'pageTitle': 'Transaction Overview',\
														'bigTitle': 'TRANSACTION',\
														'pageImage': 'spelunker/images/transaction.png',\
														'form': form,\
														'pageText' : 'Each transaction contains the data about who sent bitcoins to who. Trasactions are likely lines of a ledger.'})

def input_(request, inputId):
	try:
		input_ = Inputs.objects.get(id = inputId)
	except Inputs.DoesNotExist:
		raise Http404("Input does not exist")
	return render(request, 'spelunker/input.html', {'input': input_})

def inputReview(request):
	form = SearchForm(auto_id=False, initial={'refferer': 'input'})
	form.base_fields['search'].widget.attrs["placeholder"] = "Enter a specific input ID..."
	return render(request, 'spelunker/overview.html', {'pageTitle': 'Input Overview',\
														'bigTitle': 'INPUT',\
														'pageImage': 'spelunker/images/input.png',\
														'form': form,\
														'pageText' : 'Each input contains the data about a previous output. This allows to chain and retrace former payments.'})

def output(request, outputId):
	try:
		output = Outputs.objects.get(id = outputId)
	except Outputs.DoesNotExist:
		raise Http404("Output does not exist")
	return render(request, 'spelunker/output.html', {'output': output})

def outputReview(request):
	form = SearchForm(auto_id=False, initial={'refferer': 'output'})
	form.base_fields['search'].widget.attrs["placeholder"] = "Enter a specific output ID..."
	return render(request, 'spelunker/overview.html', {'pageTitle': 'Output Overview',\
														'bigTitle': 'OUTPUT',\
														'pageImage': 'spelunker/images/output.png',\
														'form': form,\
														'pageText' : 'Each output contains the data about a value received by a wallet.'})