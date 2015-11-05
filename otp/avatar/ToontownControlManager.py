from direct.directnotify import DirectNotifyGlobal
from direct.controls.ControlManager import ControlManager
from direct.showbase.InputStateGlobal import inputState

class ToontownControlManager(ControlManager):
    '''
    The Toontown Control Manager. This is coded for WASD support
    in mind primarily. Some functions had to be overridden in
    order to fix Panda3D's crude WASD support and fine-tune
    it for Toontown.
    '''
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownControlManager')

    # This is so we can get wantWASD from ToonBase, instead of checking Config.prc.
    wantWASD = base.wantWASD

    def __init__(self, enable=True, passMessagesThrough = False):
        self.passMessagesThrough = passMessagesThrough
        self.inputStateTokens = []
        self.WASDTurnTokens = []
        self.__WASDTurn = True
        self.controls = {}
        self.currentControls = None
        self.currentControlsName = None
        self.isEnabled = 0
        self.forceAvJumpToken = None
        self.inputToDisable = []
        self.forceTokens = None
        self.istWASD = []
        self.istNormal = []
        if enable:
            self.enable()

    def enable(self):
        if self.isEnabled:
            assert self.notify.debug('already isEnabled')
            return
        self.isEnabled = 1

        # Let's keep track of what we do on the inputState so that we can undo it later on.
        ist = self.inputStateTokens
        ist.append(inputState.watch("run", 'runningEvent', "running-on", "running-off"))
        ist.append(inputState.watch("forward", "force-forward", "force-forward-stop"))
        ist.append(inputState.watchWithModifiers("reverse", "mouse4", inputSource=inputState.Mouse))
        if self.wantWASD:
            self.istWASD.append(inputState.watch("turnLeft", "mouse-look_left", "mouse-look_left-done"))
            self.istWASD.append(inputState.watch("turnLeft", "force-turnLeft", "force-turnLeft-stop"))
            self.istWASD.append(inputState.watch("turnRight", "mouse-look_right", "mouse-look_right-done"))
            self.istWASD.append(inputState.watch("turnRight", "force-turnRight", "force-turnRight-stop"))
            self.istWASD.append(inputState.watchWithModifiers("forward", "w", inputSource=inputState.WASD))
            self.istWASD.append(inputState.watchWithModifiers("reverse", "s", inputSource=inputState.WASD))
            self.setWASDTurn(self.__WASDTurn)
        else:
            self.istNormal.append(inputState.watchWithModifiers("forward", "arrow_up", inputSource=inputState.ArrowKeys))
            self.istNormal.append(inputState.watchWithModifiers("reverse", "arrow_down", inputSource=inputState.ArrowKeys))
            self.istNormal.append(inputState.watchWithModifiers("turnLeft", "arrow_left", inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch("turnLeft", "mouse-look_left", "mouse-look_left-done"))
            ist.append(inputState.watch("turnLeft", "force-turnLeft", "force-turnLeft-stop"))
            self.istNormal.append(inputState.watchWithModifiers("turnRight", "arrow_right", inputSource=inputState.ArrowKeys))
            ist.append(inputState.watch("turnRight", "mouse-look_right", "mouse-look_right-done"))
            ist.append(inputState.watch("turnRight", "force-turnRight", "force-turnRight-stop"))

        # Jump controls
        if self.wantWASD:
            jumpKey = config.GetString('WASD-jump-key', 'space')
            self.istWASD.append(inputState.watchWithModifiers("jump", jumpKey))
        else:
            self.istNormal.append(inputState.watch("jump", "control", "control-up"))
        if self.currentControls:
            self.currentControls.enableAvatarControls()

    def setWASDTurn(self, turn):
        self.__WASDTurn = turn
        if not self.isEnabled:
            return

        turnLeftWASDSet = inputState.isSet("turnLeft", inputSource=inputState.WASD)
        turnRightWASDSet = inputState.isSet("turnRight", inputSource=inputState.WASD)
        slideLeftWASDSet = inputState.isSet("slideLeft", inputSource=inputState.WASD)
        slideRightWASDSet = inputState.isSet("slideRight", inputSource=inputState.WASD)

        for token in self.WASDTurnTokens:
            token.release()

        # If we want Toons to be able to turn instead of sliding left to right:
        if turn:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("turnLeft", "a", inputSource=inputState.WASD),
                inputState.watchWithModifiers("turnRight", "d", inputSource=inputState.WASD),
                )
            inputState.set("turnLeft", slideLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("turnRight", slideRightWASDSet, inputSource=inputState.WASD)
            inputState.set("slideLeft", False, inputSource=inputState.WASD)
            inputState.set("slideRight", False, inputSource=inputState.WASD)
        else:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("slideLeft", "a", inputSource=inputState.WASD),
                inputState.watchWithModifiers("slideRight", "d", inputSource=inputState.WASD),
                )
            inputState.set("slideLeft", turnLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("slideRight", turnRightWASDSet, inputSource=inputState.WASD)
            inputState.set("turnLeft", False, inputSource=inputState.WASD)
            inputState.set("turnRight", False, inputSource=inputState.WASD)

    def disable(self):
        self.isEnabled = 0

        for token in self.inputStateTokens:
            token.release()
        self.inputStateTokens = []

        for token in self.WASDTurnTokens:
            token.release()
        self.WASDTurnTokens = []

        if self.currentControls:
            self.currentControls.disableAvatarControls()

        # This is so we don't break Toontown...
        if self.passMessagesThrough:
            if self.wantWASD:
                self.istWASD.append(inputState.watchWithModifiers("forward", "w", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("reverse", "s", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("turnLeft", "a", inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers("turnRight", "d", inputSource=inputState.WASD))
            else:
                self.istNormal.append(inputState.watchWithModifiers("forward", "arrow_up", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("reverse", "arrow_down", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("turnLeft", "arrow_left", inputSource=inputState.ArrowKeys))
                self.istNormal.append(inputState.watchWithModifiers("turnRight", "arrow_right", inputSource=inputState.ArrowKeys))

    # Disables WASD for when chat is open.
    def disableWASD(self):
        if self.wantWASD:
            # Forces all keys to return 0. This won't affect chat input.
            self.forceTokens=[
                inputState.force(
                  "jump", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "forward", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "turnLeft", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "slideLeft", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "reverse", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "turnRight", 0, 'ControlManager.disableWASD'),
                inputState.force(
                  "slideRight", 0, 'ControlManager.disableWASD')
            ]

    # Enables WASD after chat is closed.
    def enableWASD(self):
        if self.wantWASD:
            if self.forceTokens:
                # Release all the forced keys we added earlier.
                for token in self.forceTokens:
                    token.release()
                self.forceTokens = []

    # Called to reload the ControlManager in-game.
    def reload(self):
        # Reload wantWASD if it was recently changed.
        self.wantWASD = base.wantWASD
        if self.wantWASD:
            for token in self.istNormal:
                # Release arrow key input.
                token.release()
            self.istNormal = []
            self.inputStateTokens = []
            self.disable()
            self.enable()
        else:
            for token in self.WASDTurnTokens:
                token.release()
            for token in self.istWASD:
                token.release()
            self.istWASD = []
            self.WASDTurnTokens = []
            self.disable()
            self.enable()
