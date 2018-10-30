import machine, utime, os
from microWebSrv import MicroWebSrv

if 'config.py' in os.listdir('/flash'):
    print('ok')

# ----------------------------------------------------------------------------

@MicroWebSrv.route('', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    devadd = formData["devadd"]
    nwskey = formData["nwskey"]
    appkey = formData["appkey"]
    content = """\
    <!DOCTYPE html>
    <html lang=en>
	<head>
		<meta charset="UTF-8" />
		<title>AlphaX MHM Configuration Page</title>
		<link rel="stylesheet" href="style.css" />
	</head>
	<body style="min-width: 480px;text-align: center">
		<div style="text-align: center;padding-top: 10px">
			<img src="ax_logo.png" />
			<h1>MHM4 LoRaWAN ABP Configuration</h1>
		</div><br>
        <div style="max-width:480px;padding:10px;margin: auto;text-align: center">
	    <form action="" method="post" accept-charset="ISO-8859-1">
		<div style="padding:10px;text-align: center">
			<label style="font-size:11px">Device Address: </label>
			<input type="text" name="devadd" style="color:#fff" value="%s" disabled>
		</div>
           <div width="480px" style="padding:10px;text-align: center">
			<label style="font-size:11px">Network Session Key: </label>
			<input type="text" name="nwskey" style="color:#fff" value="%s" disabled>
		</div>
		<div  style="padding:10px;text-align: center">
			<label style="font-size:11px">App Session KEY: </label>
			<input type="text" name="appkey" style="color:#fff" value="%s" disabled>
		</div>
		<div  style="padding:10px;">
			<h5 style="color:green">Success. Device will reboot Now.</h5> 
		</div>	
	</form>
	<br>
		<p style="font-size:9px">If you wish to connect via ABP (which is the recommended method) the network will provide you with a Device ID, Network Key and Application Key. The former identifies what application your device is connecting to, the latter is a shared secret key unique to your device to generate the session keys that prove its identity on the network. </p>
		<br />
	</div>
	</body>
    </html>
    """ % ( MicroWebSrv.HTMLEscape(devadd),
            MicroWebSrv.HTMLEscape(nwskey),
            MicroWebSrv.HTMLEscape(appkey) )
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )

    f = open('/flash/config.py', 'w')
    f.write('#############################################\n')
    f.write('####### sys generated file do not edit ######\n')
    f.write('#############################################\n')
    f.write('devadd = "'+str(devadd)+'"\n')
    f.write('nwskey = "'+str(nwskey)+'"\n')
    f.write('appkey = "'+str(appkey)+'"\n')
    f.close()

    machine.reset()

srv = MicroWebSrv(webPath='www/')
srv.Start(threaded=False)

# ----------------------------------------------------------------------------