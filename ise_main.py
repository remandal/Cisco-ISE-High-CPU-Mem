#!/usr/bin/env python

"""Main Program"""

import paramiko
import netmiko
import time
import datetime
import socket
import sys
import smtplib
import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

try:
    import env
except (SyntaxError, ModuleNotFoundError):
    print("Invalid input detected in the env file. Please fill all the fields in a correct format.")
    sys.exit(1)


try:
    ise_address = env.ise_address
    ise_username = env.ise_username
    ise_password = env.ise_password

    probe_address = env.probe_address
    probe_username = env.probe_username
    probe_password = env.probe_password

    sender_email = env.sender_email
    sender_password = env.sender_password
    recipient_email = env.recipient_email
    smtp_server = env.smtp_server
    smtp_server_port = env.smtp_server_port

except (NameError, KeyError):
    print("Invalid input detected in the env file. Please fill all the fields in a correct format.")
    sys.exit(1)


def restart_ise(ise_address, ise_username, ise_password, ise_port):
    #Method to restart ISE services
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print("%s: Connecting to ISE..." % str(datetime.datetime.now()))
        ssh.connect(ise_address, port=ise_port, username=ise_username,
                    password=ise_password, look_for_keys=False, allow_agent=False)
    except socket.error:
        print("%s: ISE seems to be unreachable. Please verify connectivity to ISE and re-run this program."
              % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.AuthenticationException:
        print("%s: Unable to log in to ISE. Please verify the username/password set and re-run this program." % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("%s: ISE seems to be unreachable. Please verify connectivity to ISE and re-run this program."
              % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.SSHException:
        print("%s: Unable to log in to ISE. Please verify reachability to ISE, and correct username/password is set and re-run this program." % str(datetime.datetime.now()))
        sys.exit(1)
    print("%s: Successfully logged in to ISE..." % str(datetime.datetime.now()))
    # timers here were set based on response times during lab tests:
    remote_conn = ssh.invoke_shell()
    remote_conn.send("\n")
    time.sleep(2)
    remote_conn.send("\n")
    time.sleep(2)
    print("%s: Proceeding to stop ISE services..." % str(datetime.datetime.now()))
    remote_conn.send("application stop ise\n")
    time.sleep(300)
    print("%s: ISE services have been terminated..." %
          str(datetime.datetime.now()))
    remote_conn.send("application start ise\n")
    print("%s: Proceeding to restart ISE services..." %
          str(datetime.datetime.now()))
    time.sleep(300)
    print("%s: ISE services are are being restarted..." %
          str(datetime.datetime.now()))
    time.sleep(300)
    print("%s: ISE services have been restarted successfully..." %
          str(datetime.datetime.now()))
    ssh.close()


def send_email(from_email, from_email_password, to_email, smtp_email_server_address, smtp_email_server_port):
    #Method to notify users via email
    
    email_server = smtplib.SMTP(
        smtp_email_server_address, smtp_email_server_port)
    email_server.ehlo()
    email_server.starttls()
    email_server.ehlo()
    email_server.login(from_email, from_email_password)
    from_address = from_email
    to_address = to_email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ', '.join(to_address)
    msg['Subject'] = "ATTENTION: Cisco ISE application services were restarted!"
    body = "ISE application services were restarted at " + \
        str(datetime.datetime.now())
    msg.attach(MIMEText(body, 'plain'))
    email_text = msg.as_string()
    email_server.sendmail(from_address, to_address, email_text)
    print("%s: A notification email was sent to " + ", ".join(str(i) for i in to_email) %
          str(datetime.datetime.now()))


def main():

    
    while True:
        print("%s: Starting the ISE monitoring program using probe to %s." % (
            str(datetime.datetime.now()), probe_address))

        failure_count = 0
        while failure_count < 3:
            try:
                probe = paramiko.SSHClient()
                probe.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                probe.connect(probe_address, port=22,
                              username=probe_username, password=probe_password)
                time.sleep(30)
                probe.close()
                print("%s: Monitoring probe is reachable. No actions needed." %
                      str(datetime.datetime.now()))
                failure_count = 0
            except socket.error:
                print("%s: Monitor probe is unreachable. Please verify IP connectivity to the probe"
                      " and rerun the script." str(datetime.datetime.now()))
                sys.exit(1)
            except paramiko.ssh_exception.AuthenticationException:
                failure_count += 1
                print("%s: Authentication failed %s time(s)." % (str(datetime.datetime.now())),
                      str(failure_count))
                time.sleep(60)
            except paramiko.ssh_exception.NoValidConnectionsError:
                print("%s: Monitor probe is unreachable. Please verify IP connectivity to the probe"
                      " and then rerun the script." % str(datetime.datetime.now()))
                sys.exit(1)
            except paramiko.ssh_exception.SSHException:
                print("%s: Invalid credentials for the probe. Please set proper username/password "
                      "and rerun the script." % str(datetime.datetime.now()))
                sys.exit(1)
        print("%s: Authentication to probe unavailable. We will proceed "
              "with the ise restart to recover." % str(datetime.datetime.now()))
        restart_ise(ise_address, ise_username, ise_password, 22)
        send_email(sender_email, Email_password, recipient_email,
                   smtp_server, smtp_server_port)
        time.sleep(600)


if __name__ == '__main__':
main()
