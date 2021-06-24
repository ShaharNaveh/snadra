import os

from hypothesis import Verbosity, settings

hypothesis_profile = os.getenv("HYPOTHESIS_PROFILE", "default").lower()

settings.register_profile("ci", max_examples=1_000)
settings.register_profile("dev", max_examples=10)
settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)

settings.load_profile(hypothesis_profile)
