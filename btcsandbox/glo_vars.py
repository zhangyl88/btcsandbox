from account.models import Account

emails                          = [i.email for i in Account.objects.all()]
usernames                       = [i.username for i in Account.objects.all()]

# emails                            = []
# usernames                         = []