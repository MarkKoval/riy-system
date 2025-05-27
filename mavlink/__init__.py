"""
mavlink — Пакет для взаємодії з автопілотом через MAVLink-протокол.
"""

from .mavlink_interface import MavlinkInterface
from .command_sender import CommandSender
from .telemetry_parser import TelemetryParser

__all__ = ["MavlinkInterface", "CommandSender", "TelemetryParser"]
