from flask import (Flask, request, render_template, make_response,
                   session, jsonify, g, url_for, send_from_directory, redirect)
from bson import Code
from urllib import unquote_plus, quote_plus
from flask_cors import cross_origin
import lxml.html
import pymongo
import StringIO
import oursql
import urllib2
import json
app = Flask(__name__)


@app.route('/open')
def open():
	return render_template('open.html')
@app.route('/')
def start_page():
        d = {}
        page_data=""
        d['foruri'] = request.args['foruri']
        myhandler1 = urllib2.Request(d['foruri'],
                                     headers={'User-Agent':
                                              "Mozilla/5.0 (X11; " +
                                              "Linux x86_64; rv:25.0)" +
                                              "Gecko/20100101 Firefox/25.0)"})
        a=urllib2.urlopen(myhandler1)
    # A fix to send user-agents, so that sites render properly.
        try:
            a = urllib2.urlopen(myhandler1)
            if a.geturl() != d['foruri']:
                return ("There was a server redirect".format(quote_plus(a.geturl())))
            else:
                page = a.read()
                a.close()
        except ValueError:
            return ("The link is malformed".format(
                        quote_plus(unquote_plus(d['foruri'].encode('utf-8'))),
                        request.args['lang']))
        except urllib2.URLError:
            return render_template('error.html')
        try:
            page = unicode(page, 'utf-8')
        except UnicodeDecodeError:
            pass
        try:
            g.root = lxml.html.parse(StringIO.StringIO(page)).getroot()
        except ValueError:
            g.root = lxml.html.parse(d['foruri']).getroot()
        g.root.make_links_absolute(d['foruri'],
                                       resolve_base_href=True)
        for i in g.root.iterlinks():
        	if i[1] == 'href' and i[0].tag != 'link':
        		try:
        			i[0].attrib['href'] = 'http://{0}?foruri={1}'.format(
        				"http://127.0.0.1:5010/", quote_plus(i[0].attrib['href']))
        		except KeyError:
					i[0].attrib['href'] = '{0}?foruri={1}'.format(
						"http://127.0.0.1:5010/", quote_plus(
							i[0].attrib['href'].encode('utf-8')))
		print g.root
        page_data = lxml.html.tostring(g.root)
        k=page_data.index('head')
        k2=page_data.index('</head>')
        head_data=page_data[k+5:k2]
        print head_data
        k=page_data.index('<body')
        k2=page_data.index('</body>')
        body_data=page_data[k+5:k2]
        print body_data
        print type(page_data)
        return render_template('get_data.html',head_data=head_data,body_data=body_data)
        #print response.data
		
	
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
@app.route('/showeditor',methods=['GET'])
def showeditor():
    return render_template('show.html')

@app.route('/highlight')
def highlight():
    return render_template('highlight.html')
    
@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/publish', methods=['POST'])
def publish():
    sweet()
    reply = make_response()
    return reply

@app.route('/authenticate')
def redirect_uri():
    auth_tok = None
    if request.args.get('code'):
        payload = {
            'scopes': 'email sweet',
            'client_secret': 'ZbWMeGeLoTQlDB5fDCWsaljsRaBUdCHxrB6ivqKBGpw2jW5T5V',
            'code': request.args.get('code'),
            'redirect_uri': 'http://localhost:5001/authenticate',
            'grant_type': 'authorization_code',
            'client_id': 'fCoiGhwljFpYRPYSKdoYxpCwcekaWUSTpMYazLSn'
        }
        # token exchange endpoint
        oauth_token_x_endpoint = 'http://localhost:5001/oauth/token'
        resp = requests.post(oauth_token_x_endpoint, data=payload)
        auth_tok = json.loads(resp.text)

        if 'error' in auth_tok:
            print auth_tok['error']
            return make_response(auth_tok['error'], 200)

        session['auth_tok'] = auth_tok

        username_request = requests.get('http://localhost:5001/api/users/me?access_token=' +
                                        session['auth_tok']['access_token'])
        session['username'] = username_request.json()['username']
    if 'auth_tok' in session:
        auth_tok = session['auth_tok']
    else:
        auth_tok = {'access_token': '', 'refresh_token': ''}

    print auth_tok
    return render_template('index1.html', username=session['username'])


def sweet():
    """ A function to sweet the data that is inserted.
    Accepts a <list of dicts>. """
    
    sweetmaker.sweet(conf.SWEET_STORE_ADD[0] +
                     "?access_token=" + session['auth_tok']
                      ['access_token'],
                      [{"what": 'nptel',
                      "who": 'saigo',
                      "where":i['about'],
                      "how":"hgf"}])
    return True
        # data = json.dumps(data)
    # req = requests.api.post(conf.SWEETURL[0]+"/add",{'data':data})
    # if req.status_code == 200:
    #     reply = make_response()
    #     return reply      
if __name__ == "__main__":
	app.run(debug=False, host='127.0.0.1',port='5010')
