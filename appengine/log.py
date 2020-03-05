#!/usr/bin/env python

from google.cloud.logging.handlers import AppEngineHandler

_TRACE_ID_LABEL = "appengine.googleapis.com/trace_id"


class FastAPILoggingHandler(AppEngineHandler):
    """Handles logging for Fast API based apps."""

    def __init__(self, *args, **kwargs):
        self.current_request = None
        super().__init__(*args, **kwargs)

    def get_trace_id_from_fastapi(self):
        """Get trace_id from fast api request headers."""
        if self.current_request is None:
            return None

        header = self.current_request.headers.get('x-cloud-trace-context')
        if header is None:
            return None

        trace_id = header.split("/", 1)[0]

        return trace_id

    def get_gae_labels(self):
        """Return the labels for GAE app.
        If the trace ID can be detected, it will be included as a label.
        Currently, no other labels are included.
        :rtype: dict
        :returns: Labels for GAE app.
        """
        gae_labels = {}

        trace_id = self.get_trace_id_from_fastapi()
        if trace_id is not None:
            gae_labels[_TRACE_ID_LABEL] = trace_id

        return gae_labels
