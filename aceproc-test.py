
from aceproc.aceproc import AceProc, AceProcDataMsg

'''
Have your object Inherit the AceProc object and implement the
process function:

The Process function is called whenever a message is received,
any data dependant processing should occur within it.

Later in the program we will call the built-in .stop() function
to halt the thread's execution.
'''



class MyParallelObject(AceProc):
    def __init__(self, name):
        # Optionally set a name, used in print statements
        super(MyParallelObject, self).__init__(name)

    def process(self, msg):
        print("Handling a message: %s" % msg)


'''
Implement the AceProcDataMsg Object describing the data you wish
to pass between threads
'''


class MyParallelData(AceProcDataMsg):
    def __init__(self, desc="Default Desc for MyParallelData"):
        # Optionally set a description to describe your data
        super(MyParallelData, self).__init__(desc)


'''
Write a main function which creates several of your threaded objects
and pass messages between them
'''


def main():
    aceprocs = list()

    # Create 10 MemoThreads
    for i in range(0, 10):
        aceprocs.append(MyParallelObject("AceProcs %s" % i))

    # Send your data between the various Memothreads
    aceprocs[0].sendMsg(aceprocs[1], MyParallelData("Message from 00 to 01"))
    aceprocs[2].sendMsg(aceprocs[3], MyParallelData("Message from 02 to 03"))
    aceprocs[4].sendMsg(aceprocs[5], MyParallelData("Message from 04 to 05"))

    # To Stop your concurrent object, simply call .stop()
    print("Stopping AceProcs")
    for i in range(0, 10):
        print("stopping %s" % i)
        #aceprocs[i].stop()


if __name__ == "__main__":
    main()

'''
Please check out aceproc-test.py within the git repo for another example! Have fun!
'''



