from workflows.analysis.hexmaps.election_2025.p_npp.__main__ import (
    main as p_npp,
)

from workflows.analysis.hexmaps.election_2025.npp_seats.__main__ import (
    main as npp_seats,
)

from workflows.analysis.hexmaps.election_2025.p_rejected.__main__ import (
    main as p_rejected,
)
from workflows.analysis.hexmaps.election_2025.p_sjb.__main__ import (
    main as p_sjb,
)
from workflows.analysis.hexmaps.election_2025.p_turnout.__main__ import (
    main as p_turnout,
)
from workflows.analysis.hexmaps.election_2025.seats.__main__ import (
    main as seats,
)

from workflows.analysis.hexmaps.election_2025.seats_and_votes_odd.__main__ import (
    main as seats_and_votes_odd,
)

from workflows.analysis.hexmaps.election_2025.seats_gen_elec.__main__ import (
    main as seats_gen_elec,
)

from workflows.analysis.hexmaps.election_2025.seats_ties.__main__ import (
    main as seats_ties,
)
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    main as votes,
)
from workflows.analysis.hexmaps.election_2025.votes_2nd.__main__ import (
    main as votes_2nd,
)
from workflows.analysis.hexmaps.lg_types.__main__ import main as lg_types
from workflows.analysis.hexmaps.provinces.__main__ import main as provinces

import os
from utils import Log
import shutil

log = Log("hexmaps")


def copy_and_cleanup():
    for dirpath, dirnames, filenames in os.walk(
        os.path.join("workflows", "analysis", "hexmaps")
    ):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.endswith(".py"):
                continue
            if filename.startswith("hexbin-") and filename.endswith(".png"):
                shutil.move(file_path, os.path.join("images", filename))
                log.info(f'Moved "{file_path}" to images')
                continue
            os.remove(file_path)
            log.warning(f'Removed "{file_path}"')

        for dirname in dirnames:
            dir_path = os.path.join(dirpath, dirname)
            if dirname == "__pycache__":
                shutil.rmtree(dir_path)
                log.warning(f'Removed "{dir_path}"')


# provinces()
# lg_types()
# votes()
# votes_2nd()

# seats()

# p_turnout()
# p_rejected()

# seats_gen_elec()
# seats_and_votes_odd()
# seats_ties()

# p_npp()
# p_sjb()

# npp_seats()

copy_and_cleanup()
