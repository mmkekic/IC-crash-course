"""
-----------------------------------------------------------------------
                             City name
-----------------------------------------------------------------------

City description

"""
import numpy  as np
import tables as tb

from .. types.ic_types import minmax
from .. database       import load_db

from .. reco                  import tbl_functions        as tbl
from .. reco                  import  peak_functions      as pkf
from .. core.random_sampling  import NoiseSampler         as SiPMsNoiseSampler
from .. io  .        pmaps_io import          pmap_writer
from .. io.        mcinfo_io  import       mc_info_writer
from .. io  .run_and_event_io import run_and_event_writer
from .. io  .trigger_io       import       trigger_writer
from .. io  .event_filter_io  import  event_filter_writer

from .. dataflow            import dataflow as fl
from .. dataflow.dataflow   import push
from .. dataflow.dataflow   import pipe
from .. dataflow.dataflow   import sink

from .  components import city
from .  components import print_every
from .  components import deconv_pmt
from .  components import calibrate_pmts
from .  components import calibrate_sipms
from .  components import zero_suppress_wfs
from .  components import WfType
from .  components import wf_from_files


class Datatype(AutoEnumBase):
    rd    = auto()
    rwf   = auto()
    pmaps = auto()
    kdst  = auto()
    hdst  = auto()
    cdst  = auto()


READERS = {
Datatype.rd    =  partial( wfs_from_files, wf_type = WfType.mcrd),
Datatype.rwf   =  partial( wfs_from_files, wf_type = WfType.rwf ),
Datatype.pmaps =          pmap_from_files,
Datatype.kdst  =          kdst_from_files,
Datatype.hdst  = hits_and_kdst_from_files,
Datatype.cdst  =          cdst_from_files,
}


WRITERS = {
Datatype.rd    =  rwf_writer,
Datatype.rwf   =  rwf_writer,
Datatype.pmaps = pmap_writer,
Datatype.kdst  = kdst_writer,
Datatype.hdst  = hdst_writer,
Datatype.cdst  = cdst_writer,
}


def get_reader(datatype):
    if datatype in READERS:
        return READERS[datatype]

    raise ValueError(f"Undefined datatype {datatype}")

def get_writer(datatype):
    if datatype in WRITERS:
        return WRITERS[datatype]

    raise ValueError(f"Undefined datatype {datatype}")

def change_label(x):
    if ""
    x["event"] =

@city
def selection(files_in, file_out, datatype, compression, arguments):
    datatype     = getattr(Datatype, datatype)
    event_reader = get_reader(datatype)
    event_writer = get_writer(datatype)
    relabel      =
    with tb.open_file(file_out, "w", filters = tbl.filters(compression)) as h5out:
        # Define writers...
        write_event_info_   = run_and_event_writer(h5out)
        write_mc_           = mc_info_writer      (h5out) if run_number <= 0 else (lambda *_: None)
        write_kdst_         = kdst_from_df_writer (h5out)

        # ... and make them sinks
        write_event_info   = fl.sink(write_event_info_  , args=(   "run_number",     "event_number", "timestamp"   ))
        write_mc           = fl.sink(write_mc_          , args=(           "mc",     "event_number"                ))
        write_event        = fl.sink(write_event_       , args=         "event"                                     )
        write_kdst_table   = fl.sink(write_kdst_        , args="kdst"               )

        return push(source = event_reader(files_in),
                    pipe   = pipe(fl.slice(*event_range, close_all=True),
                                  print_every(print_mod),
                                  event_count_in.spy,
                                  event_filter.filter,
                                  event_count_out.spy,
                                  fl.fork(write_mc,
                                          write_event_info)),
                    result = dict(events_in  = event_count_in .future,
                                  events_out = event_count_out.future,))
