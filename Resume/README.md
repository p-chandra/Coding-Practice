# Website on Raspberry Pi 4
This not a very detailed hold your hand tutorial. This is meant for anyone that doesn't mind doing a little reseach to fill in their gaps. 
Also this requires no money for any of the servies that we will be using today, though you will need a raspberry pi so...

We will not be installing PHP(backend) or using Javascript/Node.js (frontend/backend). Because there are many frameworks to choose from, it is much easier just to get some html up and going first and then you can do the research on which framework works the best for you.


## Step 1 Setup Raspberry Pi
Setup your raspberry pi. There are 1000s of videos on youtube made by 13 year-olds teaching you how to do this. If you perfer to read, then here https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2 
Make sure your SSH is enabled

## Step 2 Download Apache2
Install apache2 using the command below. 

- sudo apt install apache2

Your web browser should open after the installation but if not then just open your web browser and type in your pi's ip address at the search/address bar. What you should be seeing is a default apache site and this is what you going to be modifying.
 

## Step 3 Edit local website
You need to now access your local website. On your pi change directory to  /var/www/html/ and give yourself the ownership of the index.html file by using to command below

- cd /var/www/html/ 
- sudo chown pi: index.html

Open the index.html file and delete everything in it. Now put your own html code, save and then close. If you go to your localhost (pi's ip address in the web browser) you should see your new local website that you just made changes too. 


## Step 3 Make website public
Congrats on making it this far. Now you want to show your imaginary friends your new "amazing" website but there is a problem. You most likely don't have a static ip address and the DHCP will make sure that your ip address changes every now and then. You can either call your internet service provider(ISP) and ask for a static IP address and if that doesn't work then sign up for https://www.noip.com/ and create a hostname under dynamic dns (DDNS). Now sign into your ISP domain and mess with the settings. You will need too 

- set up port forwarding tcp/udp 80 (80 is default for HTTP)
- set up port forwarding tcp/udp 22 (22 is default for SSH if you want to remote into your pi from anywhere)
- Enable DDNS (This is where your NoIP host name goes)

Step 3 in a video https://www.youtube.com/watch?v=DGix3gtZ7ew


## You are done with all the basics. 
Now you can explore other stuff and build up like what does hostgator do and godaddy. There are types of web hosting such as shared, reseller, vps, dedicated, cloud, and managed wordpress. They all have pros and cons so look into that. Things to consider; how much traffic are you planning to get, what kind of website are you trying to make, which servies are you willing to pay for etc. All this you can find on youtube or google and just keep reading. 

Cheers
