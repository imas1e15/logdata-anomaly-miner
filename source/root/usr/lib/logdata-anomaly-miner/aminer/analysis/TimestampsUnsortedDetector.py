"""This module defines a detector for unsorted timestamps."""

import os

from aminer.events import EventSourceInterface
from aminer.input import AtomHandlerInterface
from datetime import datetime
from aminer.analysis import CONFIG_KEY_LOG_LINE_PREFIX


class TimestampsUnsortedDetector(AtomHandlerInterface, EventSourceInterface):
  """This class creates events when unsorted timestamps are detected.
  This is useful mostly to detect algorithm malfunction or configuration
  errors, e.g. invalid timezone configuration."""

  def __init__(self, aminer_config, anomaly_event_handlers, exit_on_error_flag=False, output_log_line=True):
    """Initialize the detector."""
    self.anomaly_event_handlers = anomaly_event_handlers
    self.last_timestamp = 0
    self.exit_on_error_flag = exit_on_error_flag
    self.output_log_line = output_log_line
    self.aminer_config = aminer_config

  def receive_atom(self, log_atom):
    """Receive on parsed atom and the information about the parser
    match.
    @param log_atom the parsed log atom
    @return True if this handler was really able to handle and
    process the match. Depending on this information, the caller
    may decide if it makes sense passing the parsed atom also
    to other handlers."""
    if log_atom.get_timestamp() is None:
      return False
    if log_atom.get_timestamp() < self.last_timestamp:
      original_log_line_prefix = self.aminer_config.config_properties.get(CONFIG_KEY_LOG_LINE_PREFIX)
      if original_log_line_prefix is None:
        original_log_line_prefix = ''
      if self.output_log_line:
        sorted_log_lines = [log_atom.parser_match.match_element.annotate_match('') + os.linesep +
                            original_log_line_prefix + repr(log_atom.raw_data)]
      else:
        sorted_log_lines = [original_log_line_prefix + repr(log_atom.raw_data)]
      analysis_component = {'LastTimestamp': self.last_timestamp}
      event_data = {'AnalysisComponent': analysis_component}
      for listener in self.anomaly_event_handlers:
        listener.receive_event('Analysis.%s' % self.__class__.__name__, \
            'Timestamp %s below %s' % (datetime.fromtimestamp(log_atom.get_timestamp()).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.fromtimestamp(self.last_timestamp).strftime("%Y-%m-%d %H:%M:%S")),
                               sorted_log_lines, event_data, log_atom, self)
      if self.exit_on_error_flag:
        import sys
        sys.exit(1)
    self.last_timestamp = log_atom.get_timestamp()
    return True


  def whitelist_event(self, event_type, sorted_log_lines, event_data,
                      whitelisting_data):
    """Whitelist an event generated by this source using the information
    emitted when generating the event.
    @return a message with information about whitelisting
    @throws Exception when whitelisting of this special event
    using given whitelistingData was not possible."""
    if event_type != 'Analysis.%s' % self.__class__.__name__:
      raise Exception('Event not from this source')
    raise Exception('No whitelisting for algorithm malfunction or configuration errors')
