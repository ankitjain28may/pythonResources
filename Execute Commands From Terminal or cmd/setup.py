import subprocess

# Include your commands to run
installs = [
        "pip install bs4",
        "pip install requests",
        "pip install validators"
    ]


print("Wait for the installations, Its in progress..!!!")

# Run all the commands one by one
for install in installs:
    query = install.split()
    proc = subprocess.Popen(query, stdout=subprocess.PIPE, shell=True)
    output, error = proc.communicate() # Show error and output of the commands
    if output!=None:
        print(output.decode('utf-8'))
    elif error!=None:
        print(error.decode('utf-8'))


# proc = subprocess.Popen(['pip', 'install','ScrapeAmazon'],stdout=subprocess.PIPE, shell=True)
# # out = check_output(["pip", "list"])
# # print(out.decode('utf-8'))
# print(proc.communicate()[0].decode('utf-8'))