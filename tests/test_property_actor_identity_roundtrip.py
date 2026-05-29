"""Property test: ActorIdentity Round-Trip Serialization.

**Property 3: ActorIdentity Round-Trip Serialization**
**Validates: Requirements 33.6**

Tests that for any valid ActorIdentity (all 7 ActorType values, arbitrary
actor_id strings, arbitrary context dicts, both is_fallback values),
to_dict() then from_dict() produces an equivalent object.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from governance.actor_identity import ActorType, ActorIdentity


# Strategy for generating valid ActorType values
actor_type_strategy = st.sampled_from(list(ActorType))

# Strategy for generating arbitrary but reasonable actor_id strings
actor_id_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "P", "S")),
    min_size=1,
    max_size=100,
)

# Strategy for generating context dicts with string keys and string values
context_strategy = st.dictionaries(
    keys=st.text(
        alphabet=st.characters(whitelist_categories=("L", "N")),
        min_size=1,
        max_size=30,
    ),
    values=st.text(min_size=0, max_size=100),
    max_size=10,
)

# Strategy for is_fallback boolean
is_fallback_strategy = st.booleans()


@given(
    actor_type=actor_type_strategy,
    actor_id=actor_id_strategy,
    context=context_strategy,
    is_fallback=is_fallback_strategy,
)
@settings(max_examples=100)
def test_actor_identity_roundtrip_serialization(
    actor_type: ActorType,
    actor_id: str,
    context: dict,
    is_fallback: bool,
) -> None:
    """For any valid ActorIdentity, to_dict() then from_dict() produces an equivalent object."""
    original = ActorIdentity(
        actor_type=actor_type,
        actor_id=actor_id,
        context=context,
        is_fallback=is_fallback,
    )

    serialized = original.to_dict()
    deserialized = ActorIdentity.from_dict(serialized)

    assert deserialized.actor_type == original.actor_type
    assert deserialized.actor_id == original.actor_id
    assert deserialized.context == original.context
    assert deserialized.is_fallback == original.is_fallback


@given(
    actor_type=actor_type_strategy,
    actor_id=actor_id_strategy,
    context=context_strategy,
    is_fallback=is_fallback_strategy,
)
@settings(max_examples=100)
def test_actor_identity_double_roundtrip(
    actor_type: ActorType,
    actor_id: str,
    context: dict,
    is_fallback: bool,
) -> None:
    """Double round-trip produces the same dict representation."""
    original = ActorIdentity(
        actor_type=actor_type,
        actor_id=actor_id,
        context=context,
        is_fallback=is_fallback,
    )

    dict1 = original.to_dict()
    restored1 = ActorIdentity.from_dict(dict1)
    dict2 = restored1.to_dict()

    assert dict1 == dict2
