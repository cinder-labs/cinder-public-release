#####
# tinder.py
# Contains the internal dependencies for a cinder instance
# Created by: Carter Richard
# License GNU GPL v3
#####

# Import native dependencies
import os
import datetime

# Import external dependencies
import openai
from web3 import Web3

### LOCAL TEST host instance configuration
# This configuration is for untracked TESTING
# DO NOT USE THIS CONFIGURATION IN A PRODUCTION ENVIRONMENT
# DO NOT COMMIT THIS CONFIGURATION TO A REPOSITORY
# NEVER PUBLICLY EXPOSE YOUR API KEY
#platform = 'openai'
#model = 'gpt-3.5-turbo'
#paradigm = 'centralized'
#openai.api_key = ''
#assistant = 'cinder'
web3url = "HTTP://127.0.0.1:8545"

### Get host instance configuration
# Uncomment these lines and modify as needed to pull in environment variables
# If you are deploying cinder to a production environment OR
# building a container image for a specialized assistant,
# it is HIGHLY recommended that you set environment variables below.
platform = os.environ["CINDER_PLATFORM"]
model = os.environ["CINDER_MODEL"]
paradigm = os.environ["CINDER_PARADIGM"]
openai.api_key = os.environ["OPENAI_API_KEY"]
assistant = os.environ["CINDER_ASSISTANT"]


#AI platform configuration
if platform == 'openai':
    stop = None
    temperature = 0.5
else:
    print("Only OpenAI is currently supported. " + assistant + " will now shut down.")
    exit

#Misc
workdir = assistant + '/'
web3 = Web3(Web3.HTTPProvider(web3url))

##### Cinder Class #####
# These low-level functions provide basic filesystem operations for cinder 
# as well as the ability to build and execute console commands

class cinder:
    def __init__(self, workdir=workdir):
        self.workdir = workdir

        return

    # Print an activity status to the console.
    def status(self, activity, target=""):

        time = datetime.datetime.now()
        status = "          " + assistant.capitalize() + " is " + str(activity) + " " + str(target) + "\n           at " + str(time)
        print(str(status))

        return

    # Pass a command to the console
    def execute(self):
        
        self.status("executing the following command: ", self.command)
        os.system(self.command)

        return
    
    # Build a command from prefixes, arguments
    def build(self, prefix, argument=""):

        self.status("building a command with " + str(prefix) + " " + str(argument))
        self.command = str(prefix + " " + argument)
        self.execute()

        return
    
    # Create a directory
    def mkdir(self, targets=[], workdir = workdir):

        for directory in targets:
            self.status("warming up", str(workdir + directory))
            self.build("mkdir", workdir + directory)

        return

    # Remove a directory (and its children)
    def rmdir(self, targets=[], workdir = workdir):

        for directory in targets:
            self.status("cooling down", str(workdir + directory))
            self.build("rm -r", workdir + directory)

        return

    # Make a file
    def mkfile(self, destination, filename="unnamed.txt"):
        self.status("making file: ", filename)
        self.build("touch", str(self.workdir + destination + "/" + filename))

        return

    # Copy a file to a destination
    def cpfile(self, target, destination="."):
        self.status("copying file: ", target + " to " + destination)

        self.build("cp -r", target + " " + destination)

        return

    # Read a file and return its contents
    def rdfile(self, target, workdir = workdir):
        self.status("reading file: ", target)

        file = open(workdir + target, "r").readlines()

        for i, line in enumerate(file):
            file[i] = line.strip('\n\r')

        print("\n File contents: ")
        print("\n" + str(file))
        print("\n")

        return file

    # Write a file
    def wrfile(self, target, content):
        self.status("writing to the following file: ", target)

        file = open(self.workdir + target, "w")
        for item in content: 
            file.write(item + "\n")
            file.close
        
        return

    def clear(self):
        if os.name =="nt":
            self.build("cls")
        else:
            self.build("clear")

        return


    # This method uses the above to build a cinder instance
    def spark(self):

        # Wipe existing directory
        self.rmdir([""]) 

        # Clear the console
        self.clear()
        
        #Start the environment build
        self.status("building the local environment")

        # Establish filesystem
        self.mkdir([workdir], "")
        self.mkdir(self.rdfile('spark/resources/misc/directories.txt', ""))

        # Create a test file
        self.mkfile('resources/misc', 'helloworld.txt')

        # Write to test file
        self.wrfile('resources/misc/helloworld.txt', ['hello ' + str(assistant) + '!'])

        # Populate environment with native contexts
        self.cpfile('spark/resources', self.workdir)

        # Send a console message when the spark process is complete
        self.status('ready for tasking')

        return


##### Message Class #####

class message:
    def __init___(self, sender, content, transaction="", auth=False):
        self.sender = sender
        self.content = content
        self.transaction = transaction
        self.auth = auth

        return self

    def authenticate(self):

        if paradigm == 'decentralized' and self.transaction != '':
            receipt = receipt = web3.eth.get_transaction_receipt(self.transaction)
            if receipt['status'] == 1:
                self.auth=True
            else:
                self.auth=False
        elif paradigm == 'centralized':
            self.auth=True
        else:
            self.auth=False
        return self


##### Session Class #####

class session:
    def __init__(self, instance, baseline='conversational', sender='', content='', contentCache = '', root='', task='', chain='', context='', inputFlag=False, contextFlag=False, chainFlag = False, runFlag=False, messageThread=[]):
        self.instance = instance
        self.baseline = baseline
        self.sender = sender
        self.content = content
        self.contentCache = contentCache
        self.root = root
        self.task = task
        self.chain = chain
        self.context = context
        self.inputFlag = inputFlag
        self.contextFlag = contextFlag
        self.chainFlag = chainFlag
        self.runFlag = runFlag
        self.messageThread = messageThread

        return

    def summaryPrint(self):

        print("\n   *********************START SUMMARY*********************")
        print("\n   Session flags:")
        print("     Input flag: ", self.inputFlag)
        print("     Context flag: ", self.contextFlag)
        print("     Chain flag: ", self.chainFlag)
        print("     Run flag: ", self.runFlag)
        print("\n   Session content:")
        print("     root: ", self.root)
        print("     task: ", self.task)
        print("     chain: ", self.chain)
        print("\n   content: \n", self.content)
        print("\n   contentCache: \n", self.contentCache)
        print("\n   context: \n", self.context)
        print("\n   messageThread: ")
        for message in self.messageThread:
            print(str(message) + "\n    ")
        print("\n   *********************END SUMMARY***********************\n")

        return

    def inputClassify(self, userMessage, instance):

        messageSplit = str(userMessage.content).split()
        knownTasks = os.listdir(workdir + "resources/tasks")

        if len(messageSplit) == 1:
            if messageSplit[0] == "spark":
                self.instance.status("sparking...")
                self.instance.spark()
                self.instance.status("done.")
                self.sender = "system"
                self.content = assistant.capitalize() + " sparked."

            elif messageSplit[0] == "library":
                self.instance.status("providing task list to user.")
                self.sender = "system"
                self.content = "Known tasks: " + str(knownTasks)

            elif messageSplit[0] in knownTasks:
                self.instance.status("interpreting message as a task request with known context.")

                self.task = messageSplit[0]
                self.sender = "system"
                self.content = "Context provided, provide input."
                self.inputFlag = True

            else:
                self.instance.status("rejecting an unknown task and responding with baseline context.")
                self.inputFlag = False
                self.chainFlag = False
                self.task = self.baseline
                self.sender = assistant
                self.content = userMessage.content
                self.messageThread=[]

        elif messageSplit[0] == "run":
            if os.path.exists(workdir + "resources/tasks/" + messageSplit[1] + "/chain.txt"):
                self.instance.status("interpreting message as request to run automation chain.")
                self.runFlag = True

            else: 
                self.instance.status("reaching the end of an automation chain.")
                self.runFlag = False
                self.chain = ''

            self.task = messageSplit[1]
            messageSplit.pop(0)
            userMessage.content = ' '.join(messageSplit)
            self.inputClassify(userMessage, instance)

        elif messageSplit[0] == "chain":
            self.instance.status("interpreting message as a chained task")
            self.chainFlag = True
            self.root = self.task
            if messageSplit[1] in knownTasks: 
                self.inputFlag = False
                self.task = messageSplit[1]
                self.sender = assistant
                self.content = self.messageThread[-1]['content']
            else:
                messageSplit.pop(0)
                userMessage.content = ' '.join(messageSplit)
                self.inputClassify(userMessage, instance)

        elif messageSplit[0] == "task":
            self.instance.status("interpreting message as new task and expecting context.")
            self.contextFlag = True
            self.task = messageSplit[1]
            messageSplit.pop(0)
            self.sender = "system"
            self.content = "Creating task; provide context."

        elif self.contextFlag == True:
            self.instance.status("interpreting message as new context.")
            self.contextFlag = False

            self.content = userMessage.content
            self.instance.mkdir(['resources/tasks/' + self.task])
            self.instance.mkdir(instance.rdfile('spark/resources/misc/directories.txt', ""), workdir + 'resources/tasks/' + self.task + '/')
            self.instance.wrfile('resources/tasks/' + self.task + '/con.txt', [self.content])

            if self.chainFlag == True:
                self.chainFlag = False
                self.inputFlag = False

                self.instance.status("chaining previous task output to new task input.")
                self.sender = assistant
                self.content = self.messageThread[-1]['content']
            else:
                self.inputFlag = True
                self.instance.status("expecting input.")
                self.sender = "system"
                self.content = "Context saved, provide task input."

        elif self.inputFlag == True:
            self.instance.status("interpreting message as task input.")
            self.inputFlag = False

            self.sender = assistant
            self.content = userMessage.content

        else: 
            self.instance.status("interpreting as baseline input")
            self.chainFlag = False
            self.task = self.baseline
            self.sender = assistant
            self.content = userMessage.content
            self.root = ''
            self.messageThread = []

        return

    def threadMessage(self, role, content):
        self.messageThread.append({'role': role, 'content': content})

        return self

    def sendMessage(self, platform):
        self.instance.status("calling model...")

        if platform == "openai":
            response = openai.ChatCompletion.create(
                model = model,
                messages = self.messageThread,
                stop = stop,
                temperature = temperature
            )
            output = response.choices[0].message.content
        else:
            output = "Only OpenAI is supported for now."

        self.instance.status("finished.")
        return output

    def interactionCycle(self, userMessage, instance):

        print("\n   *********************START INTERACTION CYCLE***********\n")

        self.instance = cinder()
        response = message()

        self.inputClassify(userMessage, instance)

        if self.sender == "system":
            response.sender = self.sender
            response.content = self.content

        else:
            self.context = instance.rdfile("resources/tasks/" + self.task + "/con.txt", instance.workdir)[0]

            self.threadMessage("user", self.content)
            self.threadMessage("system", self.context)

            self.content = self.sendMessage(platform)

            self.threadMessage("assistant", self.content)

            if self.root != '' and self.runFlag == False:
                instance.wrfile("resources/tasks/" + self.root + "/chain.txt", [self.task])

            if self.runFlag == True:
                self.runFlag = False
                self.chain = instance.rdfile("resources/tasks/" + self.task + "/chain.txt")[0].strip('\n\r')
                self.chain.strip('\n\r')
                self.contentCache = self.content
                userMessage.content = "run " + self.chain
                self.interactionCycle(userMessage, instance)
                userMessage.content = self.contentCache
                response = self.interactionCycle(userMessage, instance)
            else:
                response.sender = assistant
                response.content = self.content

        self.summaryPrint()

        print("\n   *********************END INTERACTION CYCLE*************\n")

        return response
        
