
from hypothesis import settings, Phase, HealthCheck
settings.register_profile("fast", max_examples=5, phases=[Phase.explicit, Phase.generate], suppress_health_check=[HealthCheck.too_slow], deadline=None)
settings.load_profile("fast")
