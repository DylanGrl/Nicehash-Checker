import sys
import time
import datetime
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main(args):
    if(len(args) != 6):
        print("Usage : python nicehash.py <BITCOIN_ADDRESS> <NUMBER OF RIGS> <EMAIL RECEIVER> <EMAIL SENDER (gmail_addr)> <PASSWORD FROM SENDER>")
        sys.exit(1)
    else:     
        BITCOIN_ADDR = args[1]
        str_NB_RIGS =  args[2]
        NB_RIGS = int(str_NB_RIGS)
        MAIL_RECEIVER = args[3]
        MAIL_SENDER = args[4]
        MAIL_SENDER_PASSWD = args[5]
        print("Your Bitcoin wallet : "+BITCOIN_ADDR)
        print("Number of unique miner(s): "+str(NB_RIGS))
        print("Mail from "+MAIL_SENDER+" to "+MAIL_RECEIVER)

        
        while True:
            r = requests.get("https://api.nicehash.com/api?method=stats.provider.workers&addr="+BITCOIN_ADDR)
            
            #print(r.json())
            json_res = r.json()
            NB_TOTAL_WORKER = len(json_res["result"]["workers"]);
            #print(len(json_res["result"]["workers"]))
            
            if(NB_TOTAL_WORKER == 0):
                now = datetime.datetime.now()
                print(str(now.hour)+"h"+str(now.minute)+" - No miner(s) is/are running !")
                fromaddr = MAIL_SENDER
                toaddr = MAIL_RECEIVER
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                SUBJECT = "All workers are down - "+str(now.hour)+"h"+str(now.minute)+" "+str(now.day)+"/"+str(now.month)+"/"+str(now.year)
                msg['Subject'] = SUBJECT
                 
                body = ""
                msg.attach(MIMEText(body, 'plain'))
                 
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr, MAIL_SENDER_PASSWD)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                time.sleep(60*60)
            else:
                now = datetime.datetime.now()
                print(str(now.hour)+"h"+str(now.minute)+" - Miner(s) is/are working !")
                	#print(NB_TOTAL_WORKER)
                	#print(json_res["result"]["workers"][0][0])
                LIST_NAME_WORKER = []
                for i in range(0,NB_TOTAL_WORKER):
                	        LIST_NAME_WORKER.append(json_res["result"]["workers"][i][0])
                		#print(json_res["result"]["workers"][i][0])
                	#print(LIST_NAME_WORKER)	
                	#print(set(LIST_NAME_WORKER))
            NB_UNIQUE_MINER = len(set(LIST_NAME_WORKER))
            if(NB_UNIQUE_MINER < NB_RIGS):
                now = datetime.datetime.now()
                print(str(now.hour)+"h"+str(now.minute)+" - All of your miner(s) are not working ! : "+str(NB_UNIQUE_MINER)+"/"+str(NB_RIGS))
                fromaddr = MAIL_SENDER
                toaddr = MAIL_RECEIVER
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                SUBJECT = "All of your miner(s) are not working - "+str(now.hour)+"h"+str(now.minute)+" "+str(now.day)+"/"+str(now.month)+"/"+str(now.year)
                msg['Subject'] = SUBJECT
                 
                body = "Only "+str(NB_UNIQUE_MINER)+" is/are running over "+str(NB_RIGS)+" normally"
                msg.attach(MIMEText(body, 'plain'))
                 
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(fromaddr,MAIL_SENDER_PASSWD)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                
            time.sleep(60*10)

if __name__ == '__main__':
    main(sys.argv)
	