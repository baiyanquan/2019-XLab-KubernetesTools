#!/usr/bin/expect
set timeout 10
set username [lindex $argv 0]
set password [lindex $argv 1]
set hostname [lindex $argv 2]
set port [lindex $argv 3]
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub -p $port $username@$hostname
expect {
    #first connect, no public key in ~/.ssh/known_hosts
    "Are you sure you want to continue connecting (yes/no)?" {
        send "yes\r"
        expect {
            "password:"{send "$password\r"}
            eof {send_user "eof\n"}
            }
        }
    #already has public key in ~/.ssh/known_hosts
    "password:" {
        send "$password\r"
        except eof
        }
    "Now try logging into the machine" {
        #it has authorized, do nothing!
        except eof
        }
    }
