"""
This module defines a detector for log atoms not matching any allowlisted rule.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from aminer.input.InputInterfaces import AtomHandlerInterface
from aminer.AminerConfig import CONFIG_KEY_LOG_LINE_PREFIX, DEFAULT_LOG_LINE_PREFIX, DEBUG_LOG_NAME
from aminer import AminerConfig
from aminer.analysis.Rules import MatchRule


class AllowlistViolationDetector(AtomHandlerInterface):
    """
    Objects of this class handle a list of allowlist rules.
    They ensure, that each received log-atom is at least covered by a single allowlist rule. To avoid traversing the complete rule tree
    more than once, the allowlist rules may have match actions attached that set off an alarm by themselves.
    """

    def __init__(self, aminer_config, allowlist_rules, anomaly_event_handlers, output_logline=True):
        """
        Initialize the detector.
        @param allowlist_rules list of rules executed until the first rule matches.
        """
        super().__init__(aminer_config=aminer_config, anomaly_event_handlers=anomaly_event_handlers, output_logline=output_logline,
                         allowlist_rules=allowlist_rules)
        if allowlist_rules is None:
            msg = "allowlist_rules must not be empty."
            logging.getLogger(DEBUG_LOG_NAME).error(msg)
            raise TypeError(msg)
        for path in self.allowlist_rules:
            if not isinstance(path, MatchRule):
                msg = "allowlist_rules values must be of the type MatchRule."
                logging.getLogger(DEBUG_LOG_NAME).error(msg)
                raise TypeError(msg)

    def receive_atom(self, log_atom):
        """
        Receive a parsed atom and the information about the parser match.
        @param log_atom atom with parsed data to check
        @return a boolean value if the log atom matches one of the rules.
        """
        self.log_total += 1
        event_data = {}
        for rule in self.allowlist_rules:
            if rule.match(log_atom):
                self.log_success += 1
                return True
        original_log_line_prefix = self.aminer_config.config_properties.get(CONFIG_KEY_LOG_LINE_PREFIX, DEFAULT_LOG_LINE_PREFIX)
        try:
            data = log_atom.raw_data.decode(AminerConfig.ENCODING)
        except UnicodeError:
            data = repr(log_atom.raw_data)
        analysis_component = {"AffectedLogAtomPaths": list(log_atom.parser_match.get_match_dictionary()), "AffectedLogAtomValues": [data]}
        sorted_log_lines = [original_log_line_prefix + data]
        event_data["AnalysisComponent"] = analysis_component
        for listener in self.anomaly_event_handlers:
            listener.receive_event(f"Analysis.{self.__class__.__name__}", "No allowlisting for current atom", sorted_log_lines,
                                   event_data, log_atom, self)
        return False

    def log_statistics(self, component_name):
        """
        Log statistics of an AtomHandler. Override this method for more sophisticated statistics output of the AtomHandler.
        @param component_name the name of the component which is printed in the log line.
        """
        super().log_statistics(component_name)
        for i, rule in enumerate(self.allowlist_rules):
            rule.log_statistics(component_name + "." + rule.__class__.__name__ + str(i))
