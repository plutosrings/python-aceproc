#import threading
from multiprocessing import Queue, Process
from threading import Timer

from .grxe_common import GrxeObject


'''
    Python MemoThread by GRXE
        Python Threads with Native Message Passing
'''
class AceProc(GrxeObject):


    def schedule(self, schedule, msg=None):
        # need to make this a thread protected variable
        if self.enabled:
            if msg is None:
                msg = AceProcScheduleMsg("Schedule Message", schedule)

            Timer(schedule, self.process_schedule, msg )

    def __process_schedule(self, msg):
        assert isinstance(msg, AceProcScheduleMsg)

        self.process_schedule(msg)

        # Offset the scheduling of this message by the time .process_schedule took
        self.schedule(msg.schedule, msg)

    def process_schedule(self, msg):
        self.say("Generic Scheduled Message Processing")

    #    def __unicode__(self):
    #         return self.name

    def __str__(self):
        return self.name

    def __init__(self, name, schedule=None, concurrent=True, wait=False):

        self.msgbox = Queue()

        self.name       = name
        self.alive      = True
        self.enabled    = True
        self.concurrent = concurrent
        self.wait       = wait

    def launch(self):

        if self.concurrent:
            self.debug(self.name, "Creating New AceProc")

            self.thread = Process(target=self.exec)

            if not self.wait:
                self.thread.start()

        else:
            # Consume the main thread, still process messages
            self.exec()

    def coinit(self):
        print("Default co-initialization function")

    def recvMsg(self, msg):
        assert isinstance(msg, AceProcMsg)

        self.msgbox.put(msg)

    def sendMsg(self, to, msg):

        assert isinstance(to, AceProc)
        assert isinstance(msg, AceProcMsg)

        #to.recvMsg(msg)
        print("Sending to: %s" % to)
        to.msgbox.put(msg)

    def stop(self):
        self.sendMsg(self, AceProcCtrlMsgStop())

    def pause(self):
        self.sendMsg(self, AceProcCtrlMsgPause())

    def resume(self):
        self.sendMsg(self, AceProcCtrlMsgResume())

    def exec(self):
        self.debug(self.name, "Starting Exec")

        self.coinit()

        while self.alive:
            self.debug(self.name, "Waiting for Msg")
            msg = self.msgbox.get(block=True)
            self.debug(self.name, "Got a Msg: %s" % msg)

            if self.enabled and isinstance(msg, AceProcDataMsg):
                self.debug(self.name, "Got a User-Data Msg: %s" % msg)
                self.process(msg)

                #if result and isinstance(result, AceProcDataMsg):
                #self.sendMsg(result.sendto, result)
                #   pass

            elif isinstance(msg, AceProcCtrlMsg):
                self.debug(self.name, "Got a Control Msg: %s" % msg)

                self.__process_cmd(msg)

            else:
                self.say(self.name, "Unknown Message Type provided! Skipping...: %s" % msg)

        # Exited Main Loop
        self.say(self.name, "Thread: %s Exiting" % self.name)

    def __process_cmd(self, msg):
        self.say(self.name, "Processing Cmd: %s" % msg)

        if isinstance(msg, AceProcCtrlMsgStop):
            # Received Command to Stop Operation and Exit
            self.say(self.name, "Stopping Thread... Will now close: ")
            self.enabled    = False
            self.alive      = False

        elif isinstance(msg, AceProcCtrlMsgPause):
            self.say(self.name, "Pausing Thread... Ignoring Data Messages. Will only respond to Ctrl Messages")
            self.enabled = False

        elif isinstance(msg, AceProcCtrlMsgResume):
            self.say(self.name, "Resuming Thread... Will now respond to User-Data Messages")
            self.enabled = True

        elif isinstance(msg,AceProcCtrlMsgDump):
            self.say(self.name, "Dumping all User Data Messages")

        else:
            self.debug(self.name, "Received Unknown Control Message")

    def process(self, msg):
        self.debug(self.name, "Base/Empty Process Method: %s" % msg)


''' ---------------------------------------------------------------
    AceThread Message Classes 
        Used to pass Controls/User-Specified Data between AceThread Objects
    ---------------------------------------------------------------
    ---------------------------------------------------------------
'''
'''
    Class: AceThreadMsg:
        Base/Root class for all MemoThread Messages (Control & User-Specified)
'''


class AceProcMsg(GrxeObject):
    def __init__(self, desc="Default Description for Base AceProcMsg"):
        self.desc = desc



    def __str__(self):
        return "AceThreadMsg: %s" % self.desc


'''
    Class: AceThreadDataMsg:
        Base class for User-Specified Data Messages
'''
class AceProcDataMsg(AceProcMsg):
    def __init__(self, desc, send_to_aceproc=None):
        super(AceProcDataMsg, self).__init__(desc)
        print(send_to_aceproc)
        if send_to_aceproc:
            assert(send_to_aceproc, AceProc)
            self.__send_to_aceproc = send_to_aceproc
            pass
'''
    Class: AceProcScheduleMsg:
        Base class for User-Specified Schedule Messages
            These messages will trigger execution of the time-based function self.process_schedule()
'''
class AceProcScheduleMsg(AceProcMsg):
    def __init__(self, desc, schedule):
        super(AceProcScheduleMsg, self).__init__(desc)

        self.schedule = schedule

'''
    Class: AceProcCtrlMsg:
        MemoThread Control Messages used internally to control state
'''
class AceProcCtrlMsg(AceProcMsg):

    def __init__(self, desc="Default Description for Base AceProcCtrlMsg"):
        super(AceProcCtrlMsg, self).__init__(desc)

    def __str__(self):
        return "AceProcCtrlMsg - Type: %s" %  self.desc


class AceProcCtrlMsgStop(AceProcCtrlMsg):
    def __init__(self):
        super(AceProcCtrlMsgStop, self).__init__( "AceProc Ctrl: STOP")


class AceProcCtrlMsgPause(AceProcCtrlMsg):
    def __init__(self):
        super(AceProcCtrlMsgPause, self).__init__("AceProc Ctrl: PAUSE")


class AceProcCtrlMsgResume(AceProcCtrlMsg):
    def __init__(self):
        super(AceProcCtrlMsgResume, self).__init__("AceProc Ctrl: RESUME")


class AceProcCtrlMsgDump(AceProcCtrlMsg):
    def __init__(self):
        super(AceProcCtrlMsgResume, self).__init__("Ctrl: DUMP")


class AceProcCtrlMsgProcessFailed():
    """
        AceProcCtrlMsgProcessFailed
            Produced when a data message passed into the process() function failed for some reason
    """
    def __init__(self):
        super(AceProcCtrlMsgProcessFailed, self).__init__("Ctrl: DUMP")
