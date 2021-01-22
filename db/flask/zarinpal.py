# -*- coding: utf-8 -*-

# Sample Flask ZarinPal WebGate with SOAP

__author__ = 'Mohammad Reza Kamalifard, Hamid Feizabadi'
__url__ = 'reyhoonsoft.ir , rsdn.ir'
__license__ = "GPL 2.0 http://www.gnu.org/licenses/gpl-2.0.html"

from flask import Flask, url_for, redirect, request

from suds.client import Client


app = Flask(__name__)

MMERCHANT_ID = '42c34098-8c9d-48ea-ab6b-87feed5ee295'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 2000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش urge'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09102107081'  # Optional


@app.route('/request/')
def send_request():
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           str(url_for('verify', _external=True)))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error'


@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    amount)
        if result.Status == 100:
            return 'Transaction success. RefID: ' + str(result.RefID)
        elif result.Status == 101:
            return 'Transaction submitted : ' + str(result.Status)
        else:
            return 'Transaction failed. Status: ' + str(result.Status)
    else:
        return 'Transaction failed or canceled by user'


if __name__ == '__main__':
    app.run(debug=True, port=1221)
