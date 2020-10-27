# Turn off all logging for modules in this libary.
import logging
logging.disable(logging.CRITICAL)

# System imports
import      os
import      json
import      pathlib
from        argparse            import  Namespace

# Project specific imports
import      pfmisc
from        pfmisc._colors      import  Colors
from        pfmisc              import  other
from        pfmisc              import  error

from        mgz2imgslices     import  mgz2imgslices
import      pfdo

import      pudb
import      pftree

class pfdo_mgz2image(pfdo.pfdo):
    """

    A class for navigating down a dir tree and providing
    hooks for some (subclass) analysis

    """

    _dictErr = {
        'outputDirFail'   : {
            'action'        : 'trying to check on the output directory, ',
            'error'         : 'directory not specified. This is a *required* input.',
            'exitCode'      : 1},
        'outputFileExists'   : {
            'action'        : 'attempting to write an output file, ',
            'error'         : 'it seems a file already exists. Please run with --overwrite to force overwrite.',
            'exitCode'      : 2}
        }


    def declare_selfvars(self):
        """
        A block to declare self variables
        """

        #
        # Object desc block
        #
        self.str_desc                   = ''
        self.__name__                   = "pfdo_mgz2image"

    def __init__(self, *args, **kwargs):
        """
        Constructor for pfdo_mgz2image.

        This basically just calls the parent constructor and
        adds some child-specific data.
        """

        super().__init__(*args, **kwargs)

        pfdo_mgz2image.declare_selfvars(self)

    def inputReadCallback(self, *args, **kwargs):
        """
        This method does not actually read in any files, but
        exists to preserve the list of files associated with a
        given input directory. 

        By preserving and returning this file list, the next
        callback function in this pipeline is able to receive an
        input path and a list of files in that path.
        """
        str_path        : str       = ''
        l_fileProbed    : list      = []
        b_status        : bool      = True
        filesProbed     : int       = 0
        str_outputWorkingDir: str       = ""

        if len(args):
            at_data         = args[0]
            str_path        = at_data[0]
            l_fileProbed    = at_data[1]

        # Need to create the output dir appropriately here!
        str_outputWorkingDir    = str_path.replace(
                                        self.args['inputDir'],
                                        self.args['outputDir']
        )
        self.dp.qprint("mkdir %s" % str_outputWorkingDir,
                        level = 3)
        other.mkdir(str_outputWorkingDir)

        if not len(l_fileProbed): b_status = False

        return {
            'status':           b_status,
            'l_fileProbed':     l_fileProbed,
            'str_path':         str_path,
            'filesProbed':      filesProbed
        }

    def inputAnalyzeCallback(self, *args, **kwargs):
        """
        Callback stub for doing actual work. Since the `mgz2imgslices`
        is a mostly stand-apart module, the inputRead and outputWrite
        callbacks are not applicable here, since calling the
        `mgz2imgslices` module appropriately reads an input and saves
        an output.
        """
        b_status            : bool  = False
        l_fileProbed        : list  = []
        d_inputReadCallback : dict  = {}
        d_convert           : dict  = {}
        

        for k, v in kwargs.items():
            if k == 'path':         str_path    = v

        if len(args):
            at_data             = args[0]
            str_path            = at_data[0]
            d_inputReadCallback = at_data[1]

        # pudb.set_trace()
        mgz2image_args                  = self.args.copy()
        mgz2image_args['inputDir']      = str_path
        mgz2image_args['inputFile']     = d_inputReadCallback['l_fileProbed'][0]
        mgz2image_args['outputDir']     = str_path.replace(
                                            self.args['inputDir'], 
                                            self.args['outputDir']
                                        )
        mgz2image_args['saveImages']    = self.args['saveImages']  
        mgz2image_args['skipAllLabels'] = self.args['skipAllLabels']  
        
        mgz2image_ns    = Namespace(**mgz2image_args)
        imgConverter    = mgz2imgslices.object_factoryCreate(mgz2image_ns).C_convert

        # At time of dev, the `imgConverter.run()` does not return anything.
        imgConverter.run()

        return {
            'status':           b_status,
            'str_path':         str_path,
            'l_fileProbed':     l_fileProbed,
            'd_convert':        d_convert
        }

    def filelist_prune(self, at_data, *args, **kwargs) -> dict:
        """
        Given a list of files, possibly prune list by
        interal self.args['filter'].
        """

        b_status    : bool      = True
        l_file      : list      = []
        str_path    : str       = at_data[0]
        al_file     : list      = at_data[1]

        if len(self.args['filter']):
            al_file = [x for x in al_file if self.args['filter'] in x]

        if len(al_file):
            al_file.sort()
            l_file      = al_file
            b_status    = True
        else:
            self.dp.qprint( "No valid files to analyze found in path %s!" %
                            str_path, comms = 'warn', level = 5)
            l_file      = None
            b_status    = False
        return {
            'status':   b_status,
            'l_file':   l_file
        }

    def mgz2image(self) -> dict:
        """
        The main entry point for connecting methods of this class
        to the appropriate callbacks of the `pftree.tree_process()`.
        Note that the return json of each callback is available to
        the next callback in the queue as the second tuple value in
        the first argument passed to the callback.
        """
        d_mgz2image     : dict    = {}

        other.mkdir(self.args['outputDir'])
        d_mgz2image     = self.pf_tree.tree_process(
                            inputReadCallback       = self.inputReadCallback,
                            analysisCallback        = self.inputAnalyzeCallback,
                            outputWriteCallback     = None,
                            persistAnalysisResults  = False
        )
        return d_mgz2image

    def run(self, *args, **kwargs) -> dict:
        """
        This base run method should be called by any descendent classes
        since this contains the calls to the first `pftree` prove as well
        as any (overloaded) file filtering.
        """

        # pudb.set_trace()
        b_status        : bool  = False
        b_timerStart    : bool  = False
        d_pfdo          : dict  = {}
        d_mgz2image     : dict  = {}

        self.dp.qprint(
                "Starting pfdo_mgz2image run... (please be patient while running)",
                level = 1
        )

        for k, v in kwargs.items():
            if k == 'timerStart':   b_timerStart    = bool(v)

        if b_timerStart:    other.tic()

        d_pfdo          = super().run(
                            JSONprint   = False,
                            timerStart  = False
        )

        if d_pfdo['status']:
            d_mgz2image     = self.mgz2image()

        d_ret = {
            'status':           b_status,
            'd_pfdo':           d_pfdo,
            'd_mgz2image':      d_mgz2image,
            'runTime':          other.toc()
        }

        if self.args['json']:
            self.ret_dump(d_ret, **kwargs)
        else:
            self.dp.qprint('Returning from pfdo_mgz2image class run...', level = 1)

        return d_ret