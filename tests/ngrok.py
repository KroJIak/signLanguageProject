from pyngrok import ngrok, conf

conf.get_default().auth_token = '2S9BIUTkcnzQQm1wVecmSUwS8VU_3azTKb9Gsbh2PbQpbtQiM'
conf.get_default().region = 'eu'

ngrokPort = 8080

def mainNgrok():
    global ngrokTunnel
    ngrokTunnel = ngrok.connect(ngrokPort, 'tcp')
    print(ngrokTunnel.public_url)
    try:
        while True: pass
    except:
        print('Closed')

if __name__ == '__main__':
    mainNgrok()