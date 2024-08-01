import inspect
# Thanks:
# https://gist.github.com/medecau/971aaaef3985a8cd4f43d1c721181640#file-interpret-py-L22
# https://docs.python.org/3/reference/datamodel.html#emulating-callable-objects

class NameSpacer():
    """
    kills namespaces dead

    usage:

    from namespacer import NameSpacer  # WARNING: must have "NameSpacer" identifier.
    NameSpacer("ns")
    ns(foo = "bar")
    print(foo)
    foo = "__bar__"
    #--> "bar"
    ns.set("ns2")
    ns(foo = "quux")
    print(foo)
    #--> "quux"
    ns.set("defaultNamespace")
    print(foo)
    #--> "bar" #<-- note it is not "__bar__" if you want changes to persist use ns(...)
      
    """

    def __init__(self, who_am_i, __called_by_nser__ = False, _dbg_=False):

        self._who_am_i = who_am_i
        self._dbg_ = _dbg_

        if __called_by_nser__:
            self.namespaces = {}
            self.namespace = "defaultNamespace"
        else:
            # I am on the doomed timeline ~
            self.__interpret(f"{who_am_i} = NameSpacer('{who_am_i}', __called_by_nser__=True, _dbg_={_dbg_})\n", _dbg_=_dbg_)

    def set(self, ns_name):

        # set cur namespace
        self.namespace = ns_name

        # make sure current namespace exists in dict
        if not self.namespace in self.namespaces:
            self.namespaces[self.namespace] = {}

        # put namespace in locals
        for k in self.namespaces[self.namespace]:

            self.__interpret(f"{k} = {self._who_am_i}.namespaces['{self.namespace}']['{k}']", _dbg_=self._dbg_)


    def __call__(self, **kwargs):

        # make sure current namespace exists in dict
        if not self.namespace in self.namespaces:
            self.namespaces[self.namespace] = {}

        # define new object(s) in namespace 
        for k,v in kwargs.items():
            self.namespaces[self.namespace][k] = v
        
            # also put object in caller locals ;^)
            self.__interpret(f"{k} = {self._who_am_i}.namespaces['{self.namespace}']['{k}']", _dbg_=self._dbg_)
        
        
    def __interpret(self, src, _dbg_=False):
        """Compile and execute provided code as if it was local to the caller"""

        if _dbg_:
            print(f"calling:\n{src}")

        # get a decent name
        try:
            name = __file__
        except NameError:
            name = __name__

        # attemt to access callers frame
        frame = inspect.currentframe()
        if frame.f_back:
          frame = frame.f_back
          if frame.f_back:
            frame = frame.f_back

        # get the locals
        _locals = frame.f_locals

        # compile and execute
        code = compile(src, name, "exec")
        exec(code, globals(), _locals)

       # else:
       #     raise RuntimeError( "Where is the caller frame??" )


    def __repr__(self):
        return( f"NameSpacer(\"{self._who_am_i}\")" )

