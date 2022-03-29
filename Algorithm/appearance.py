


# For illustration purposes only (sourced code)

# Create a banner for the project
def banner():
    logo = print ( """\n
*********************************************************************************
*                                                                               *
*  █████╗ ██╗██████╗     ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗  *
* ██╔══██╗██║██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║  *
* ███████║██║██║  ██║    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║  *
* ██╔══██║██║██║  ██║    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║  *
* ██║  ██║██║██████╔╝    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║  *
* ╚═╝  ╚═╝╚═╝╚═════╝     ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝  *                                                                          
* Airspace Infringement Detection System - Version. 1.0                         *
* Coded by Harris Hollevas                                                      *
*                                                                               *
*                                                                               *
* FYP, University of Liverpool © 2021                                           *
*********************************************************************************\n\n""")
    return banner

# PROGRESS BAR
# credits to Diogo and Greenstick for creating this function - progress bar
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()