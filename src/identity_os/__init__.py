"""
Identity Operating System
~~~~~~~~~~~~~~~~~~~~~~~~~

An open framework for agentic AI collaboration built on identity as the
foundational primitive.

Basic usage::

    from identity_os import Platform
    from identity_os.identity import Identity, IdentityKind
    from identity_os.agents import Agent

    platform = Platform()
    human = Identity(name="Alice", kind=IdentityKind.HUMAN)
    agent = Agent(name="research-agent", owner=human)

    platform.enrol(human)
    platform.enrol(agent)

    session = platform.create_session(participants=[human, agent], goal="Research task")
"""

from identity_os.platform import Platform

__all__ = ["Platform"]
__version__ = "0.1.0"
