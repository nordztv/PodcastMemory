"""Mac recording has been retired (Scott's choice, 20 Oct 2026). If an older copy of the Mac recorder calls this,
it switches the Mac's schedule off (record_at_home.sh) and stops that recorder, so nothing is recorded on the Mac."""
import os, signal, subprocess

here = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["/bin/bash", os.path.join(here, "record_at_home.sh")])
try:
    os.kill(os.getppid(), signal.SIGTERM)  # the old recorder script that called this
except OSError:
    pass
raise SystemExit(1)
